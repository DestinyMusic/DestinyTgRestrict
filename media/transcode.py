import sys
async def _api_stream_handler(request):
    """Adaptive stream pipeline: native redirect first, minimal FFmpeg fallback."""
    try:
        user_id = int(request.query.get("user_id", 0))
    except Exception:
        user_id = 0
    link = request.query.get("link", "")
    quality = request.query.get("quality", "Original")
    audio_idx = request.query.get("audio_idx", None)
    audio_codec = request.query.get("audio_codec", "").lower().strip()
    start_time = request.query.get("start", None)
    force_transcode = request.query.get("transcode", "") in ("1", "true")
    force_x264 = request.query.get("force_x264", "") == "1" # 🟢 NEW FLAG
    if not link:
        return web.Response(status=400, text="No link provided")

    is_tg = _is_tg_link(link)
    logger.info(f"🎬 [TRANSCODE] Request | User: {user_id} | Is TG: {is_tg} | Link: {link[:100]}...")
    
    actual_url = link
    mime_type = "video/mp4"
    filename = "media"
    is_audio = False

    try:
        if is_tg:
            parsed = _parse_source_link(link)
            chat_id = parsed.get("chat_id")
            msg_id = parsed.get("msg_id")
            msg_range = parsed.get("msg_range") # 🟢 Extract range
            if chat_id is None or msg_id is None:
                return web.Response(status=400, text="Invalid Telegram link")
            pool, _ = await _get_working_tg_pool(user_id, chat_id, msg_id)
            if not pool:
                return web.Response(status=403, text="Telegram source is not accessible")
            msg = await get_client_msg(pool[0], chat_id, msg_id)
            media = msg.document or msg.video or msg.audio
            if not media:
                return web.Response(status=404, text="Media not found")
            filename = str(getattr(media, 'file_name', '') or '').lower()
            mime_type = getattr(media, 'mime_type', 'video/mp4') or 'video/mp4'
            actual_url = f"http://127.0.0.1:{PORT}/api/tg_stream?user_id={user_id}&chat_id={chat_id}&msg_id={msg_id}"
            if msg_range:
                actual_url += f"&range={msg_range[0]}-{msg_range[1]}" # 🟢 Send to stream backend
            is_audio = filename.endswith((".flac", ".mp3", ".m4a", ".ogg", ".wav", ".aac", ".wma", ".opus", ".dsf", ".ape", ".mka", ".alac")) or "audio" in mime_type
        else:
            actual_url = await resolve_direct_link(link)
            filename = _guess_filename_from_url(actual_url, "direct_media").lower()
            lower = actual_url.lower().split('?', 1)[0]
            is_audio = bool(re.search(r"\.(flac|mp3|m4a|ogg|wav|aac|wma|opus|dsf|ape|mka|alac)$", lower))
            
            # 🟢 FIX: Hard block to prevent FFmpeg from crashing on solid Archive files!
            if re.search(r'\.(7z|rar|tar|gz|iso|bin)(\.\d{3})?$', filename.lower()) or re.search(r'\.(part\d+|z\d+|r\d\d)$', filename.lower()):
                return web.Response(status=400, text="Cannot stream compressed solid archives.")
                
            mime_type = "audio/mpeg" if filename.endswith('.mp3') else (
                "audio/mp4" if filename.endswith(('.m4a','.aac')) else (
                    "audio/ogg" if filename.endswith('.ogg') else (
                        "audio/wav" if filename.endswith('.wav') else (
                            "audio/flac" if filename.endswith('.flac') else (
                                "audio/opus" if filename.endswith('.opus') else (
                                    "video/webm" if filename.endswith('.webm') else "video/mp4"
                                )
                            )
                        )
                    )
                )
            )
            # 🟢 CRITICAL FIX: Restore Loopback Proxy for FFmpeg!
            # FFmpeg's native HTTP client gets stuck when seeking direct links. Route through Python proxy!
            from urllib.parse import quote
            actual_url = f"http://127.0.0.1:{PORT}/api/direct_stream?user_id={user_id}&url={quote(link, safe='')}"
            logger.debug(f"🎬 [TRANSCODE] Using Local Proxy for FFmpeg: {actual_url[:100]}...")
    except Exception as exc:
        return web.Response(status=502, text=f"Source resolution failed: {exc}")

    # 🟢 [RESTORED & FIXED] ZIP TRACK HANDLING
    zip_idx = request.query.get("zip_idx", "")
    if zip_idx:
        # 🟢 CRITICAL FIX: Append zip_idx directly to actual_url so FFmpeg extracts the track!
        if "zip_idx=" not in actual_url: 
            actual_url += f"&zip_idx={zip_idx}"
            
        try:
            # 🟢 DYNAMIC INTERNAL ZIP PROBE: Safely detect if an internal ZIP file is an Audio Track!
            pdata = await _run_ffprobe_json(actual_url, fast=True, extract_tags=False)
            streams = pdata.get("streams", [])
            videos = [s for s in streams if s.get("codec_type") == "video" and s.get("codec_name") not in {"mjpeg", "png", "bmp", "webp"}]
            audios = [s for s in streams if s.get("codec_type") == "audio"]
            if audios and not videos:
                is_audio = True
                filename = "internal_track.mp3"
                mime_type = "audio/mpeg"
                logger.info(f"🎵 Dynamic Probe: Internal ZIP file confirmed as Audio-Only!")
        except Exception as e:
            logger.debug(f"Stream dynamic probe failed: {e}")

    # 1. Pull cached metadata FIRST
    # 🟢 FIX: Match the exact cache key generated by probe.py
    cache_key = _media_cache_key(user_id, link) + ":tags_False"
    cached_meta = MEDIA_META_CACHE.get(cache_key)
    video_codec = ""
    if cached_meta:
        meta = cached_meta[0]
        if not audio_codec:
            audio_codec = meta.get("audio_codec", "").lower()
        video_codec = meta.get("video_codec", "").lower()
        
        if not video_codec and audio_codec:
            is_audio = True
        elif video_codec:
            is_audio = False
            
        if meta.get("file_name") and meta.get("file_name").lower() not in ("unknown_media", "direct_stream_media", "download", "file", "media"):
            filename = meta.get("file_name").lower()

    # 2. Check container and codec compatibility
    is_mkv = filename.endswith((".mkv", ".mka", ".avi", ".wmv", ".flv", ".ts", ".m2ts"))
    
    # 🟢 EXPANDED: Catches HEVC, old MPEGs, Windows Media, Flash, RealVideo, and heavy editing codecs
    unsupported_web_codecs = {
        "hevc", "h265", "hvc1", "hev1", "x265", 
        "mpeg1video", "mpeg2video", "mpeg4", "msmpeg4", "msmpeg4v2", "msmpeg4v3", 
        "vc1", "wmv1", "wmv2", "wmv3", 
        "flv1", "rv10", "rv20", "rv30", "rv40", 
        "prores", "dnxhd", "theora", "mjpeg", "h263"
    }
    
    # 🟢 EXPANDED: Catches DTS, Dolby, Windows Audio, raw uncompressed PCM, and lossless non-web codecs
    bad_audio = {
        "dts", "dca", "dts-hd", "truehd", "mlp", "ac3", "eac3", 
        "wmav1", "wmav2", "wmapro", "wmavoice", 
        "pcm_s16le", "pcm_s16be", "pcm_s24le", "pcm_s32le", "pcm_f32le", "pcm_bluray", "pcm_dvd",
        "alac", "ape", "wavpack", "amr_nb", "amr_wb", "ra_144", "ra_288"
    }

    # File requires FFmpeg if it has incompatible codecs, is an unsupported container, or has explicit options set
    needs_transcode = (
        is_mkv
        or (video_codec in unsupported_web_codecs)
        or (audio_codec in bad_audio)
        or force_transcode
        or force_x264
        or quality != "Original"
        or (audio_idx is not None and str(audio_idx).strip() != "")
    )

    # 3. Allow external players to bypass transcode via a query flag (?external=1)
    is_external_player = request.query.get("external", "") == "1"

    # Only send direct byte-range if it's an external player OR 100% native web-compatible
    if (not needs_transcode) or is_external_player:
        from urllib.parse import quote
        if is_tg:
            raise web.HTTPFound(f"/api/tg_stream?user_id={user_id}&chat_id={quote(str(chat_id), safe='')}&msg_id={msg_id}")
        raise web.HTTPFound(f"/api/direct_stream?user_id={user_id}&url={quote(link, safe='')}")

    # 4. If incompatible, code execution continues down to FFmpeg transcode pipeline
    needs_video_transcode = video_codec in unsupported_web_codecs or force_x264 or quality != "Original" or is_mkv

    bad_audio = {"dts", "truehd", "ac3", "eac3"}
    # 🟢 FIX: If we are transcoding the video for web compatibility, we MUST also force the audio to transcode!
    # Browsers instantly crash or loop endlessly when fed 5.1/6-channel audio inside a fragmented MP4!
    if audio_codec in bad_audio or needs_video_transcode:
        copy_audio = False
    else:
        copy_audio = audio_codec in {'aac', 'mp3', 'opus', 'flac'} or (audio_idx is None and not force_transcode)
        
    if video_codec in unsupported_web_codecs:
        copy_video = False
    else:
        copy_video = quality == "Original" and not force_x264 
        
    res_scale_map = {"4K":"3840:-2", "1080p":"1920:-2", "720p":"1280:-2", "480p":"854:-2", "360p":"640:-2"}
    scale_filter = res_scale_map.get(quality)

    # 1. 🟢 Base Command (Do NOT use -copyts, and do NOT put -ss here)
    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error",
        "-user_agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36", 
        "-rw_timeout", "120000000", 
        "-reconnect", "1", "-reconnect_streamed", "1", "-reconnect_delay_max", "5",
        "-reconnect_at_eof", "1", "-reconnect_on_network_error", "1", 
        "-seekable", "1", 
        "-probesize", "5M", "-analyzeduration", "5M", 
        "-fflags", "+nobuffer+flush_packets+genpts"
    ]

    # 🟢 FAST INPUT SEEKING: Jump directly to the requested timestamp over HTTP
    if start_time is not None:
        try:
            start_float = max(0.0, float(start_time))
            if start_float > 0:
                cmd += ["-ss", f"{start_float:.3f}"]
        except Exception:
            pass

    cmd += ["-i", actual_url]

    if is_audio:
        if audio_idx is not None and str(audio_idx).strip():
            cmd += ["-map", f"0:{audio_idx}"]
        else:
            cmd += ["-map", "0:a:0?"]
        cmd += ["-vn", "-sn"]
        
        # 🟢 FIX: Never use MP4 container for audio-only streams. Browsers wait for video frames and hang.
        # Also, explicitly map compatible codecs to their native containers to prevent FFmpeg crashes.
        if copy_audio and audio_codec == "mp3":
            cmd += ["-c:a", "copy", "-f", "mp3", "pipe:1"]
            mime_type = "audio/mpeg"
        elif copy_audio and audio_codec in {"opus", "vorbis", "ogg"}:
            cmd += ["-c:a", "copy", "-f", "ogg", "pipe:1"]
            mime_type = "audio/ogg"
        elif copy_audio and audio_codec == "flac":
            cmd += ["-c:a", "copy", "-f", "flac", "pipe:1"]
            mime_type = "audio/flac"
        elif copy_audio and audio_codec == "aac":
            cmd += ["-c:a", "copy", "-f", "adts", "pipe:1"]
            mime_type = "audio/aac"
        else:
            # 🟢 ULTIMATE FALLBACK: Transcode EVERYTHING else (ALAC, WAV, DTS, Atmos, DSF, MKA, etc.) to AAC!
            cmd += ["-c:a", "aac", "-b:a", "256k", "-ac", "2", "-af", "aresample=async=1", "-f", "adts", "pipe:1"]
            mime_type = "audio/aac"
    else:
        cmd += ["-map", "0:v:0?"]
        if audio_idx is not None and str(audio_idx).strip():
            cmd += ["-map", f"0:{audio_idx}"]
        else:
            cmd += ["-map", "0:a:0?"]
        cmd += ["-sn"]

        if copy_video and not scale_filter:
            cmd += ["-c:v", "copy"]
            if video_codec in {"hevc", "h265", "hvc1"}:
                cmd += ["-tag:v", "hvc1"]
            elif video_codec in {"vp9", "vp8", "av1"}:
                cmd += ["-strict", "experimental"]
        else:
            cmd += [
                "-vf", f"scale={scale_filter or 'trunc(iw/2)*2:trunc(ih/2)*2'}",
                "-c:v", "libx264", "-preset", "ultrafast", "-tune", "zerolatency",
                "-pix_fmt", "yuv420p", "-threads", "0",
            ]

        if copy_audio:
            cmd += ["-c:a", "copy"]
        else:
            # 4. 🟢 HARD SYNC FIX: Force audio to stretch perfectly to the video frame
            cmd += ["-c:a", "aac", "-b:a", "192k", "-ac", "2", "-af", "aresample=async=1000:min_hard_comp=0.100000:first_pts=0"]

        # 5. 🟢 Align PTS to 0 and mux immediately for zero-latency browser streaming
        cmd += [
            "-avoid_negative_ts", "make_zero",
            "-max_muxing_queue_size", "9999",
            "-movflags", "frag_keyframe+empty_moov+default_base_moof",
            "-muxdelay", "0",
            "-f", "mp4", "pipe:1"
        ]

    logger.info(f"🎬 [STREAMING] User: {user_id} | File: {filename} | Quality: {quality} | AudioIdx: {audio_idx} | StartTime: {start_time}")
    logger.info(f"🎬 [FFMPEG CMD] {' '.join(cmd)}")

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=sys.stderr, # 🟢 Prints FFmpeg crash reports directly to the console/logs!
    )
    import aiohttp
    
    # 🟢 FIX: Separate HTTP Header logic strictly for iOS/Apple devices!
    user_agent = request.headers.get("User-Agent", "").lower()
    is_apple = ("safari" in user_agent and "chrome" not in user_agent and "android" not in user_agent) or "applecoremedia" in user_agent or "macintosh" in user_agent or "iphone" in user_agent or "ipad" in user_agent

    stream_headers = {
        "Content-Type": mime_type if is_audio else "video/mp4",
        "Access-Control-Allow-Origin": "*",
        "Cache-Control": "no-store",
    }

    apple_target_length = None
    if is_apple:
        stream_headers["Accept-Ranges"] = "bytes"
        client_range = request.headers.get("Range", "")
        if client_range:
            start_byte = 0
            end_byte = 2147483647 # Fake 2GB Maximum
            
            match = re.match(r"bytes=(\d*)-(\d*)", client_range.strip())
            if match:
                if match.group(1): start_byte = int(match.group(1))
                if match.group(2): end_byte = int(match.group(2))
                
            fake_total = 2147483648
            end_byte = min(end_byte, fake_total - 1)
            
            # Mathematical compliance for Safari's strict AVPlayer parser
            stream_headers["Content-Range"] = f"bytes {start_byte}-{end_byte}/{fake_total}"
            
            apple_target_length = end_byte - start_byte + 1
            stream_headers["Content-Length"] = str(apple_target_length)
            status_code = 206
        else:
            stream_headers["Content-Length"] = "2147483648"
            status_code = 200
    else:
        # ULTRA-STABLE 200 OK RESPONSE FOR CHROME, ANDROID, WINDOWS
        stream_headers["Accept-Ranges"] = "none"
        status_code = 200

    response = web.StreamResponse(status=status_code, headers=stream_headers)
    sid = _track_stream(request, filename, user_id)
    try:
        await response.prepare(request)
        bytes_sent = 0
        while True:
            buf = await proc.stdout.read(262144) 
            if not buf:
                break
                
            # 🟢 FIX: If Safari only asked for a specific chunk size (e.g., 2 bytes for a probe),
            # we MUST forcefully truncate the data and close the stream. 
            # If we send more data than we promised in the Content-Length, Safari instantly kills playback!
            if is_apple and apple_target_length is not None:
                if bytes_sent + len(buf) >= apple_target_length:
                    buf = buf[:apple_target_length - bytes_sent]
                    await response.write(buf)
                    break
                    
            await response.write(buf)
            bytes_sent += len(buf)
            
        await response.write_eof()
    except (ConnectionResetError, asyncio.CancelledError, aiohttp.client_exceptions.ClientConnectionResetError):
        pass
    except Exception:
        pass
    finally:
        _untrack_stream(sid)
        try:
            proc.kill()
            await proc.wait()
        except Exception:
            pass
    return response

CLIENT_MSG_CACHE = {}
CLIENT_MSG_CACHE_MAX = 2048
CLIENT_MSG_LOCKS = defaultdict(asyncio.Lock)
