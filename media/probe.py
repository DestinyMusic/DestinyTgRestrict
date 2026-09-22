async def _run_ffprobe_json(input_url, fast=True, extract_tags=False):
    """Fast probe first; retry with a larger probe only when the small probe fails."""
    probe_pairs = ((10 * 1024 * 1024, 5 * 1024 * 1024), (50 * 1024 * 1024, 25 * 1024 * 1024)) if fast else ((50 * 1024 * 1024, 25 * 1024 * 1024),)
    last_error = None
    
    # 🟢 Only scan for global tags if requested (prevents lag on MKV files in Theater)
    format_str = "format=duration,tags" if extract_tags else "format=duration"
    
    for probesize, analyzeduration in probe_pairs:
        cmd = [
            "ffprobe", "-v", "error", "-hide_banner",
            "-user_agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36", 
            "-rw_timeout", "120000000", 
            "-probesize", str(probesize),
            "-analyzeduration", str(analyzeduration),
            "-show_entries",
            f"{format_str}:stream=index,codec_type,codec_name,width,height,channels,channel_layout:"
            "stream_tags=language,title,handler_name:stream_disposition=default,forced",
            "-of", "json", input_url,
        ]
        try:
            proc = await asyncio.create_subprocess_exec(
                cmd[0], *cmd[1:],
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await proc.communicate()
            if proc.returncode == 0 and stdout:
                return json.loads(stdout.decode('utf-8', errors='ignore') or '{}')
            last_error = stderr.decode('utf-8', errors='ignore').strip() or 'ffprobe failed'
        except Exception as exc:
            last_error = str(exc)
    raise RuntimeError(last_error or 'ffprobe failed')

# ------------------------------------------------------------------------------
# Telegram access/pool cache. This avoids probing every bot for every Range
# request while still allowing automatic fallback to the logged-in user session.
# ------------------------------------------------------------------------------
TG_ACCESS_CACHE = {}
TG_ACCESS_CACHE_TTL = 120
TG_ACCESS_LOCKS = defaultdict(asyncio.Lock)


def _tg_client_cache_name(client):
    return str(getattr(client, "name", None) or id(client))


async def _get_user_stream_client(user_id):
    """Return the single persistent user session used as Telegram streaming fallback."""
    uclient = USER_CLIENTS.get(user_id)
    if uclient and getattr(uclient, "is_connected", False):
        return uclient, False

    session_str = await db.get_session(user_id)
    if not session_str:
        return None, False
    api_id = await db.get_api_id(user_id) or API_ID
    api_hash = await db.get_api_hash(user_id) or API_HASH
    try:
        uclient = Client(
            f"User_{user_id}",
            session_string=session_str,
            api_id=api_id,
            api_hash=api_hash,
            workers=100, # 🟢 FIX: Massive worker pool to instantly clear background channel noise
            no_updates=False, 
            ipv6=False,
        )
        await uclient.start()
        USER_CLIENTS[user_id] = uclient
        return uclient, False
    except Exception as exc:
        logger.warning(f"User streaming session start failed: {exc}")
        return None, False


async def _probe_tg_client(client, chat_id, msg_id):
    try:
        await get_client_msg(client, chat_id, msg_id)
        return client
    except Exception as e:
        err_str = str(e).lower()
        
        # 🟢 FIX: Handle missing peers safely. Use resolve_peer for usernames, and dialog scans for missing IDs.
        if any(err in err_str for err in ["peer_id_invalid", "channel_invalid", "channel_private", "keyerror"]):
            try:
                logger.debug(f"Client {getattr(client, 'name', 'session')} missing peer {chat_id}. Attempting resolution...")
                
                if isinstance(chat_id, str) and not chat_id.lstrip('-').isdigit():
                    await client.resolve_peer(chat_id)
                    
                async for _ in client.get_dialogs(limit=20):
                    pass
                    
                await get_client_msg(client, chat_id, msg_id)
                logger.info(f"✅ Client {getattr(client, 'name', 'session')} successfully resolved {chat_id} after scan.")
                return client
            except Exception as inner_e:
                logger.debug(f"Client {getattr(client, 'name', 'session')} still failed after scan: {inner_e}")
                pass
        return None

async def _get_working_tg_pool(user_id, chat_id, msg_id, fallback_client=None, pool_type='stream'):
    """Return accessible bot clients with smart borrowing if the other pool is idle."""
    
    # 1. 🟢 Detect if the "other" side of the bot is currently busy doing work
    is_streaming_active = any(str(s.get("user_id", "")) == str(user_id) for s in GLOBAL_NETWORK_STATS.get("active", {}).values())
    is_tasks_active = len(ACTIVE_PROCESSES.get(user_id, {})) > 0
    
    can_borrow = False
    if pool_type == 'stream':
        can_borrow = not is_tasks_active # Stream can borrow if tasks are idle
    else:
        can_borrow = not is_streaming_active # Tasks can borrow if stream is idle

    # 2. 🟢 Add 'can_borrow' to the cache key! 
    # If a task suddenly starts, this key changes, instantly releasing the borrowed bots!
    key = (user_id, chat_id, int(msg_id), pool_type, can_borrow)
    cached = TG_ACCESS_CACHE.get(key)
    now = time.time()
    
    if cached and cached[1] > now:
        pool = [c for c in cached[0] if getattr(c, "is_connected", True)]
        if pool: return pool, False

    lock = TG_ACCESS_LOCKS[key]
    async with lock:
        cached = TG_ACCESS_CACHE.get(key)
        if cached and cached[1] > time.time():
            pool = [c for c in cached[0] if getattr(c, "is_connected", True)]
            if pool: return pool, False

        primary_pool = list(USER_STREAM_BOTS.get(user_id, [])) if pool_type == 'stream' else list(USER_TASK_BOTS.get(user_id, []))
        secondary_pool = list(USER_TASK_BOTS.get(user_id, [])) if pool_type == 'stream' else list(USER_STREAM_BOTS.get(user_id, []))
        
        candidates = []
        seen = set()
        
        # 3. 🟢 Always load your primary assigned bots first
        for client in primary_pool:
            if client is None: continue
            if not getattr(client, "is_connected", False):
                try: await client.connect()
                except Exception: continue
            marker = _tg_client_cache_name(client)
            if marker in seen: continue
            seen.add(marker)
            candidates.append(client)
            
        # 4. 🟢 ONLY load the secondary bots if they are completely free, OR if you have zero primary bots configured
        if can_borrow or len(primary_pool) == 0:
            for client in secondary_pool:
                if client is None: continue
                if not getattr(client, "is_connected", False):
                    try: await client.connect()
                    except Exception: continue
                marker = _tg_client_cache_name(client)
                if marker in seen: continue
                seen.add(marker)
                candidates.append(client)

        pool = []
        if candidates:
            results = await asyncio.gather(
                # 🟢 FIX: Increased timeout to 20s. If a bot needs to fetch dialogs, 
                # it needs enough time to finish before being marked as 'failed'.
                *[asyncio.wait_for(_probe_tg_client(c, chat_id, msg_id), timeout=20.0) for c in candidates],
                return_exceptions=True,
            )
            for result in results:
                if result is not None and not isinstance(result, Exception):
                    pool.append(result)

        if pool:
            TG_ACCESS_CACHE[key] = (pool, time.time() + TG_ACCESS_CACHE_TTL)
            return pool, False

        # 5. 🟢 Only block the User Session fallback if AT LEAST ONE bot pool was configured
        if primary_pool or secondary_pool:
             logger.warning(f"All worker bots failed to access {chat_id}. Blocking fallback to prevent User Session FloodWaits.")
             return [], False

        if fallback_client is not None and getattr(fallback_client, "is_connected", False):
            user_client = fallback_client
        else:
            user_client, _ = await _get_user_stream_client(user_id)

        if user_client is not None:
            if await _probe_tg_client(user_client, chat_id, msg_id):
                TG_ACCESS_CACHE[key] = ([user_client], time.time() + 30)
                return [user_client], True

        return [], False

async def _invalidate_tg_access(user_id, chat_id, msg_id, client=None):
    key = (user_id, chat_id, int(msg_id))
    cached = TG_ACCESS_CACHE.get(key)
    if not cached:
        return
    if client is None:
        TG_ACCESS_CACHE.pop(key, None)
        return
    pool = [c for c in cached[0] if c is not client]
    if pool:
        TG_ACCESS_CACHE[key] = (pool, time.time() + min(TG_ACCESS_CACHE_TTL, 30))
    else:
        TG_ACCESS_CACHE.pop(key, None)


async def _api_media_probe_handler(request):
    """Metadata probe with caching and fast native-path friendly fallbacks."""
    try:
        user_id = int(request.query.get("user_id", 0))
    except Exception:
        user_id = 0
    link = request.query.get("link", "").strip()
    if not link:
        return web.json_response({"status": "error", "message": "Link required"}, status=400)

    # 🟢 Check if the UI is specifically asking for deep tags (Editor)
    extract_tags_flag = request.query.get("extract_tags", "0") == "1"

    # Make cache key unique so Editor doesn't get Theater's tagless cache
    cache_key = _media_cache_key(user_id, link) + f":tags_{extract_tags_flag}"
    cached = MEDIA_META_CACHE.get(cache_key)
    if cached and cached[1] > time.time():
        return web.json_response(cached[0])

    lock = MEDIA_META_LOCKS[cache_key]
    async with lock:
        cached = MEDIA_META_CACHE.get(cache_key)
        if cached and cached[1] > time.time():
            return web.json_response(cached[0])

        is_tg = _is_tg_link(link)
        logger.info(f"🔎 [PROBE] Starting probe | User: {user_id} | Is TG: {is_tg} | Link: {link[:100]}...")
        
        actual_url = link
        real_file_name = "Unknown_Media"
        mime_type = "video/mp4"
        streams = []
        duration_val = 0.0
        pdata = {}  # 🟢 FIX: Initialize pdata here to prevent UnboundLocalError

        try:
            if is_tg:
                parsed = _parse_source_link(link)
                chat_id = parsed.get("chat_id")
                msg_id = parsed.get("msg_id")
                msg_range = parsed.get("msg_range") # 🟢 Extract range
                if chat_id is None or msg_id is None:
                    return web.json_response({"status": "error", "message": "Invalid Telegram link"}, status=400)
                pool, user_fallback = await _get_working_tg_pool(user_id, chat_id, msg_id)
                if not pool:
                    return web.json_response({"status": "error", "message": "Telegram file is not accessible"}, status=403)
                msg = await get_client_msg(pool[0], chat_id, msg_id)
                media = msg.document or msg.video or msg.audio
                if not media:
                    return web.json_response({"status": "error", "message": "No media found"}, status=404)
                real_file_name = getattr(media, "file_name", None) or getattr(media, "title", None) or f"Telegram_Media_{msg_id}"
                mime_type = getattr(media, "mime_type", None) or "video/mp4"
                actual_url = f"http://127.0.0.1:{PORT}/api/tg_stream?user_id={user_id}&chat_id={chat_id}&msg_id={msg_id}"
                if msg_range:
                    actual_url += f"&range={msg_range[0]}-{msg_range[1]}" # 🟢 Send to stream backend
            else:
                actual_url = await resolve_direct_link(link)
                real_file_name = _guess_filename_from_url(actual_url, _guess_filename_from_url(link, "Direct_Stream_Media"))
                cached_headers = DIRECT_HEADER_CACHE.get(link) or DIRECT_HEADER_CACHE.get(actual_url)
                if cached_headers:
                    mime_type = cached_headers.get("content_type") or mime_type
                    cd = cached_headers.get("content_disposition", "")
                    if cd:
                        m = re.search(r"filename\*=UTF-8''([^;]+)", cd, re.I) # 🟢 FIX: Better Regex for RFC 5987
                        if m:
                            real_file_name = unquote(m.group(1).strip().strip('"'))
                        else:
                            m = re.search(r'filename=["\']?([^"\';]+)', cd, re.I) # 🟢 FIX: Catches all standard filename headers
                            if m:
                                real_file_name = unquote(m.group(1).strip())

            probe_input = actual_url
            if not is_tg:
                # 🟢 Restoring Loopback for Direct Links to prevent strict 5XX server blocks
                probe_input = f"http://127.0.0.1:{PORT}/api/direct_stream?user_id={user_id}&url={quote(actual_url, safe='')}"
                logger.debug(f"🔎 [PROBE] Feeding Loopback Proxy to FFprobe: {probe_input[:100]}...")

            tg_duration = 0.0
            if is_tg and 'media' in locals() and media:
                tg_duration = float(getattr(media, "duration", 0) or 0)
                if tg_duration > 0:
                    duration_val = tg_duration
                    logger.info(f"🔎 [PROBE TG] Found Telegram native duration: {duration_val}s")

            try:
                pdata = await _run_ffprobe_json(probe_input, fast=True, extract_tags=extract_tags_flag)
                streams = pdata.get("streams", []) or []
                if duration_val <= 0:
                    try:
                        duration_val = float((pdata.get("format") or {}).get("duration", 0) or 0)
                    except Exception:
                        duration_val = 0.0
                        
                # 🟢 NEW FIX: Attempt to extract real title from ffprobe metadata if filename is generic
                if not is_tg and real_file_name in ("Direct_Stream_Media", "download", "video", "media", "file"):
                    format_tags = pdata.get("format", {}).get("tags", {})
                    title_tag = format_tags.get("title") or format_tags.get("TITLE")
                    if title_tag:
                        ext = ""
                        if "video" in mime_type: ext = ".mp4"
                        elif "audio" in mime_type: ext = ".mp3"
                        real_file_name = title_tag if "." in title_tag else title_tag + ext

                logger.info(f"🔎 [PROBE HTTP] Success! Streams found: {len(streams)}, Duration: {duration_val}s")
            except Exception as probe_exc:
                logger.warning(f"🔎 [PROBE HTTP] Loopback HTTP probe failed: {probe_exc}")
                streams = []
                pdata = {}  # 🟢 FIX: Ensure pdata exists even if probe fails

            # 🟢 MKV SPARSE PROBE FALLBACK: If HTTP probe returned no streams for a Telegram file,
            # sample the head & tail directly into a small temp file (just like /mediainfo)
            is_zip_or_archive = bool(re.search(r'\.(zip|7z|rar|tar|gz|iso|bin)(\.\d{3})?$', str(real_file_name).lower()))
            
            if not streams and is_tg and 'pool' in locals() and pool and 'msg' in locals() and msg and not is_zip_or_archive:
                logger.info("🔎 [PROBE TG] Falling back to fast local sparse-file probe for MKV/Telegram...")
                temp_probe = Path(f"./probe_{user_id}_{int(time.time())}.dat")
                temp_named = None
                try:
                    await partial_download_tg(pool[0], msg, temp_probe, limit_mb=8)
                    real_ext = Path(real_file_name).suffix or ".mkv"
                    temp_named = temp_probe.with_suffix(real_ext)
                    temp_probe.rename(temp_named)
                    pdata = await _run_ffprobe_json(str(temp_named), fast=False, extract_tags=extract_tags_flag)
                    streams = pdata.get("streams", []) or []
                    if duration_val <= 0:
                        duration_val = float((pdata.get("format") or {}).get("duration", 0) or 0)
                    logger.info(f"🔎 [PROBE TG] Local sparse probe succeeded: {len(streams)} streams found, Duration: {duration_val}s")
                except Exception as sparse_err:
                    logger.error(f"🔎 [PROBE TG] Local sparse probe failed: {sparse_err}", exc_info=True)
                finally:
                    for p in [temp_probe, temp_named]:
                        if p and p.exists():
                            try: os.remove(p)
                            except Exception: pass

            # 🟢 FIX: Strictly block solid archives (7z, rar) but PERFECTLY ALLOW .zip and media splits (.mkv.001)!
            filename_lower = str(real_file_name).lower()
            if re.search(r'\.(7z|rar|tar|gz|iso|bin)(\.\d{3})?$', filename_lower) or re.search(r'\.(part\d+|z\d+|r\d\d)$', filename_lower):
                return web.json_response({
                    "status": "error", 
                    "message": f"Solid archives ({Path(real_file_name).suffix}) cannot be streamed in the Media Theater. Please use the 'Downloads' tab."
                })

            # 🟢 Extract duration from stream DURATION tags if still not detected
            if duration_val <= 0:
                for s in streams:
                    tags = s.get("tags", {}) or {}
                    tag_dur = tags.get("DURATION") or tags.get("duration")
                    if tag_dur:
                        try:
                            parts = str(tag_dur).split(':')
                            if len(parts) >= 3:
                                h, m, sec = float(parts[0]), float(parts[1]), float(parts[2])
                                duration_val = (h * 3600) + (m * 60) + sec
                                if duration_val > 0:
                                    logger.info(f"🔎 [PROBE] Extracted duration from stream tag: {duration_val}s")
                                    break
                        except Exception: pass

            if duration_val <= 0 and tg_duration > 0:
                duration_val = tg_duration

            # 🟢 FIX: Separate Video streams from Cover Art streams!
            videos = [s for s in streams if s.get("codec_type") == "video" and s.get("codec_name") not in {"mjpeg", "png", "bmp", "webp"}]
            covers = [s for s in streams if s.get("codec_type") == "video" and s.get("codec_name") in {"mjpeg", "png", "bmp", "webp"}]
            audios = [s for s in streams if s.get("codec_type") == "audio"]
            
            # 🟢 CRITICAL FIX: Filter out image-based subtitles (PGS, VobSub) because FFmpeg cannot convert them!
            valid_sub_codecs = {"subrip", "ass", "ssa", "webvtt", "mov_text"}
            subs = [s for s in streams if s.get("codec_type") == "subtitle" and s.get("codec_name") in valid_sub_codecs]
            filename_lower = str(real_file_name).lower()
            is_audio = bool(audios and not videos) or filename_lower.endswith((
                ".mp3", ".m4a", ".aac", ".ogg", ".wav", ".flac", ".opus"
            ))

            qualities = ["Original"]
            if not is_audio:
                height = int((videos[0].get("height") or 0)) if videos else 0
                width = int((videos[0].get("width") or 0)) if videos else 0
                if height >= 2160 or width >= 3840:
                    qualities.extend(["4K", "1080p", "720p", "480p", "360p"])
                elif height >= 1080 or width >= 1920:
                    qualities.extend(["1080p", "720p", "480p", "360p"])
                elif height >= 720:
                    qualities.extend(["720p", "480p", "360p"])
                elif height >= 480:
                    qualities.extend(["480p", "360p"])
                else:
                    qualities.append("360p")

            audio_tracks = []
            for i, st in enumerate(audios):
                tags = st.get("tags", {}) or {}
                lang = tags.get("language") or tags.get("LANGUAGE")
                # Removed 'handler_name' fallback so it doesn't show 'SoundHandler'
                title = tags.get("title") or tags.get("TITLE")
                audio_tracks.append({
                    "index": st.get("index"),
                    "label": title or lang or f"Track {i+1}",
                    "language": lang or "",
                    "channels": st.get("channels") or 0,
                    "codec_name": st.get("codec_name") or "",
                })

            subtitles = []
            for i, st in enumerate(subs):
                tags = st.get("tags", {}) or {}
                lang = tags.get("language") or tags.get("LANGUAGE")
                # Removed 'handler_name' fallback so it doesn't show 'SubtitleHandler'
                title = tags.get("title") or tags.get("TITLE")
                subtitles.append({
                    "index": st.get("index"),
                    "label": title or lang or f"Subtitle {i+1}",
                    "language": lang or "",
                })

            video_codec = (videos[0].get("codec_name") if videos else "").lower()
            audio_codec = (audios[0].get("codec_name") if audios else "").lower()
            browser_compatible = _guess_browser_compatibility(mime_type, real_file_name, streams)
            if not streams:
                ext = Path(filename_lower).suffix
                mime_guess = mime_type.lower().split(';')[0]
                browser_compatible = (
                    ext in {".mp4", ".m4v", ".webm", ".mp3", ".m4a", ".aac", ".ogg", ".wav", ".flac", ".opus"}
                    or mime_guess in {
                        "video/mp4", "video/webm", "application/mp4", "audio/mpeg", "audio/mp4",
                        "audio/aac", "audio/ogg", "audio/webm", "audio/wav", "audio/flac", "audio/opus"
                    }
                )

            # 🟢 Extract global format tags (for the metadata editor)
            format_tags = pdata.get("format", {}).get("tags", {})

            result = {
                "status": "success",
                "file_name": real_file_name,
                "mime_type": mime_type,
                "requires_transcode": not browser_compatible,
                "format_tags": format_tags,
                "browser_compatible": browser_compatible,
                "has_cover": len(covers) > 0, # 🟢 NEW: Send flag to Javascript player
                "video_codec": video_codec,
                "audio_codec": audio_codec,
                "video_width": int(videos[0].get("width") or 0) if videos else 0,
                "video_height": int(videos[0].get("height") or 0) if videos else 0,
                "duration": duration_val,
                "qualities": list(OrderedDict.fromkeys(qualities)),
                "audio_tracks": audio_tracks,
                "subtitles": subtitles,
                "resolved_url": actual_url if not is_tg else "",
                "streams": streams,
            }
            MEDIA_META_CACHE[cache_key] = (result, time.time() + MEDIA_META_TTL)
            if len(MEDIA_META_CACHE) > 512:
                oldest = min(MEDIA_META_CACHE.items(), key=lambda kv: kv[1][1])[0]
                MEDIA_META_CACHE.pop(oldest, None)
            return web.json_response(result)
        except Exception as exc:
            logger.exception("Media probe failed")
            return web.json_response({"status": "error", "message": str(exc)}, status=502)

async def _api_cover_handler(request):
    """Extracts embedded Album Art/Cover Art from audio files on the fly."""
    try:
        user_id = int(request.query.get("user_id", 0))
    except:
        user_id = 0
    link = request.query.get("link", "").strip()
    if not link:
        return web.Response(status=400, text="No link provided")

    is_tg = _is_tg_link(link)
    actual_url = link

    try:
        if is_tg:
            parsed = _parse_source_link(link)
            chat_id = parsed.get("chat_id")
            msg_id = parsed.get("msg_id")
            actual_url = f"http://127.0.0.1:{PORT}/api/tg_stream?user_id={user_id}&chat_id={chat_id}&msg_id={msg_id}"
        else:
            actual_url = await resolve_direct_link(link)

        # Grabs the exact cover frame directly from the media container
        cmd = [
            "ffmpeg", "-hide_banner", "-loglevel", "error",
            "-i", actual_url,
            "-map", "0:v:0",
            "-vframes", "1", "-c:v", "mjpeg", "-f", "image2", "pipe:1"
        ]

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        
        if proc.returncode == 0 and stdout:
            return web.Response(body=stdout, content_type="image/jpeg", headers={"Cache-Control": "public, max-age=86400"})
        else:
            return web.Response(status=404, text="No cover found")
    except Exception as e:
        return web.Response(status=500, text=str(e))

