import mimetypes
import math
import re
import asyncio
import time

async def get_client_msg(client, chat_id, msg_id):
    """Cache Telegram messages and coalesce simultaneous metadata requests."""
    key = (id(client), chat_id, int(msg_id))
    cached = CLIENT_MSG_CACHE.get(key)
    if cached is not None:
        return cached
    lock = CLIENT_MSG_LOCKS[key]
    async with lock:
        cached = CLIENT_MSG_CACHE.get(key)
        if cached is not None:
            return cached
        msg = await client.get_messages(chat_id, msg_id)
        if getattr(msg, "empty", True) or not (msg.document or msg.video or msg.audio):
            raise ValueError(f"Empty Message for client {getattr(client, 'name', 'Unknown')}")
        CLIENT_MSG_CACHE[key] = msg
        if len(CLIENT_MSG_CACHE) > CLIENT_MSG_CACHE_MAX:
            try:
                CLIENT_MSG_CACHE.pop(next(iter(CLIENT_MSG_CACHE)))
            except Exception:
                pass
        return msg

async def fetch_single_chunk(client, chat_id, msg_id, offset, limit):
    """Fetches a chunk continuously. Translates raw bytes into Pyrogram Chunk Indexes."""
    import math
    import asyncio
    CHUNK_SIZE = 1048576
    
    # 🟢 CRITICAL FIX: Pyrogram offset expects CHUNK INDEX, not raw bytes!
    chunk_index = offset // CHUNK_SIZE
    skip_bytes = offset % CHUNK_SIZE
    
    target_bytes = limit
    # Calculate how many 1MB chunks we need to fetch to satisfy the request
    total_bytes_to_fetch = skip_bytes + target_bytes
    chunk_limit = math.ceil(total_bytes_to_fetch / CHUNK_SIZE)
    
    for attempt in range(6): 
        if not getattr(client, "is_connected", False):
            try: await client.connect()
            except Exception: pass

        current_skip = skip_bytes
        try:
            msg = await get_client_msg(client, chat_id, msg_id)
            data = bytearray()
            
            async def fetch_continuous():
                nonlocal current_skip
                # 🟢 Pass the correct Chunk Index (e.g. 1) and Chunk Limit (e.g. 4)
                async for chunk in client.stream_media(msg, offset=chunk_index, limit=chunk_limit):
                    if current_skip > 0:
                        if len(chunk) <= current_skip:
                            current_skip -= len(chunk)
                            continue
                        else:
                            chunk = chunk[current_skip:]
                            current_skip = 0
                            
                    data.extend(chunk)
                    if len(data) >= target_bytes:
                        break
                        
            # 🟢 FIX: Vastly reduced timeout threshold so hung streams die fast and retry instead of freezing
            dynamic_timeout = max(5.0, (target_bytes / 1024 / 1024) * 2.0)
            try:
                await asyncio.wait_for(fetch_continuous(), timeout=dynamic_timeout)
            except asyncio.TimeoutError:
                raise TimeoutError("Chunk fetch timed out during transfer")
                    
            if not data: 
                raise ValueError("EOF Reached or Empty Chunk")
            return bytes(data[:target_bytes])
            
        except FloodWait as e:
            await asyncio.sleep(e.value + 1)
        except (TimeoutError, asyncio.TimeoutError):
            logger.debug(f"Chunk timeout on {getattr(client, 'name', 'bot')}, retrying...")
            await asyncio.sleep(0.5)
        except Exception as e:
            if "Connection closed" in str(e):
                logger.debug(f"Connection dropped by Telegram. Retrying...")
            if attempt == 5: raise e
            await asyncio.sleep(1.0 + attempt) 
            
    raise TimeoutError("Exceeded max retries for chunk")

async def parallel_stream_generator(fallback_client, chat_id, msg_parts, start_byte, total_length, chunk_size=1 * 1024 * 1024, concurrency=None):
    """Fast Telegram range generator with 1MB sweet-spot chunks to prevent server drops."""
    if total_length <= 0:
        return

    working_pool = []
    user_id = 0
    if fallback_client in USER_CLIENTS.values():
        for uid, candidate in USER_CLIENTS.items():
            if candidate is fallback_client:
                user_id = uid; break

    # 🟢 FIX: Updated to match your new Split Worker Bot architecture
    user_worker_bots = list(USER_STREAM_BOTS.get(user_id, []))
    for c in user_worker_bots:
        try:
            if getattr(c, "is_connected", False): working_pool.append(c)
        except Exception: pass
            
    if fallback_client:
        try:
            if getattr(fallback_client, "is_connected", False): working_pool.append(fallback_client)
        except Exception: pass

    if not working_pool:
        working_pool = [app]
    
    safe_concurrency = len(working_pool)
    if concurrency is not None:
        safe_concurrency = min(concurrency, safe_concurrency)
    safe_concurrency = max(1, safe_concurrency)

    # 🟢 Locked back to 1MB. This is the exact size that avoids "upload.GetFile" rate limits.
    actual_chunk_size = 1 * 1024 * 1024

    range_start = int(start_byte)
    range_end = range_start + int(total_length)
    units = []
    
    for part in msg_parts:
        p_start = int(part["start"])
        p_end = int(part["end"])
        if p_end <= range_start or p_start >= range_end:
            continue
        cursor = max(range_start, p_start)
        limit_end = min(range_end, p_end)
        while cursor < limit_end:
            take = min(int(actual_chunk_size), limit_end - cursor)
            units.append((part, cursor - p_start, take))
            cursor += take

    if not units:
        return

    if safe_concurrency == 1:
        client = working_pool[0]
        for part, internal_offset, internal_limit in units:
            try:
                yield await fetch_single_chunk(client, chat_id, part["msg_id"], internal_offset, internal_limit)
            except Exception:
                raise
        return

    # 🟢 Multi-Bot Parallel Path with Ghost Task Kill Switch
    cursor_idx = 0
    tasks = []
    import asyncio # Ensure asyncio is loaded for create_task
    
    try:
        while cursor_idx < len(units):
            batch = units[cursor_idx:cursor_idx + safe_concurrency]

            async def _fetch_with_failover(unit_idx, unit):
                part, internal_offset, internal_limit = unit
                preferred = working_pool[unit_idx % len(working_pool)]
                candidates = [preferred] + [c for c in working_pool if c is not preferred]
                last_exc = None
                for client in candidates:
                    try:
                        return await fetch_single_chunk(client, chat_id, part["msg_id"], internal_offset, internal_limit)
                    except Exception as exc:
                        last_exc = exc
                        # 🟢 Re-added the invalidate call here correctly!
                        await _invalidate_tg_access(user_id, chat_id, part["msg_id"], client)
                raise last_exc or RuntimeError("Telegram chunk fetch failed across all bots")

            tasks = [asyncio.create_task(_fetch_with_failover(i, unit)) for i, unit in enumerate(batch)]
            
            for task in tasks:
                result = await task
                if result:
                    yield result
                    
            cursor_idx += len(batch)
            tasks.clear()
            
    finally:
        # 🟢 Clean and simple! No duplicated logic.
        for task in tasks:
            if not task.done():
                task.cancel()

async def _api_tg_stream_handler(request):
    """High-speed Telegram Range proxy with multi-bot routing, user fallback, split files and ZIP extraction."""
    try:
        user_id = int(request.query.get("user_id", 0))
    except Exception:
        user_id = 0

    link = request.query.get("link")
    logger.info(f"🌐 [TG STREAM] Native Byte-Range Request | User: {user_id} | Link: {str(link)[:60]}...")
    msg_range = None
    if link:
        parsed = _parse_source_link(link)
        chat_id = parsed.get("chat_id")
        msg_id = parsed.get("msg_id")
        msg_range = parsed.get("msg_range")
    else:
        chat_id = request.query.get("chat_id")
        msg_id = request.query.get("msg_id")
        range_spec = request.query.get("range", "")
        if range_spec:
            rm = re.match(r"^(\d+)-(\d+)$", range_spec)
            if rm: msg_range = (int(rm.group(1)), int(rm.group(2)))

    if chat_id is None or msg_id is None:
        return web.Response(status=400, text="Missing chat_id/msg_id or link")

    msg_id = int(msg_id)
    chat_id = int(chat_id) if str(chat_id).lstrip('-').isdigit() else chat_id

    response = None
    temp_client = None
    try:
        working_pool, using_user_session = await _get_working_tg_pool(user_id, chat_id, msg_id)
        if not working_pool:
            return web.Response(status=403, text="Telegram file is not accessible")
        primary_client = working_pool[0]

        msg = await get_client_msg(primary_client, chat_id, msg_id)
        media = msg.document or msg.video or msg.audio
        if not media:
            return web.Response(status=404)

        filename = str(getattr(media, "file_name", "") or "").lower()
        mime_type = getattr(media, "mime_type", "application/octet-stream") or "application/octet-stream"

        parts_map = []
        global_offset = 0

        # 🟢 FIX: Directly utilize the perfectly parsed msg_range for seamless multi-part chunking!
        if msg_range:
            start_id, end_id = msg_range[0], msg_range[1]
            for mid in range(start_id, end_id + 1):
                try:
                    m = await get_client_msg(primary_client, chat_id, mid)
                    doc = m.document or m.video or m.audio
                    if doc:
                        psz = int(doc.file_size or 0)
                        if psz > 0:
                            parts_map.append({"msg_id": m.id, "start": global_offset, "end": global_offset + psz, "size": psz})
                            global_offset += psz
                except Exception:
                    continue
        else:
            match = re.search(r'\.(\d{2,3})$', filename)
            if match and int(match.group(1)) == 1:
                current_id = msg_id
                while True:
                    try:
                        m = await get_client_msg(primary_client, chat_id, current_id)
                        doc = m.document or m.video
                        if not doc:
                            break
                        psz = int(doc.file_size or 0)
                        parts_map.append({"msg_id": m.id, "start": global_offset, "end": global_offset + psz, "size": psz})
                        global_offset += psz
                        current_id += 1
                        next_m = await get_client_msg(primary_client, chat_id, current_id)
                        next_doc = next_m.document or next_m.video
                        if not next_doc or not re.search(r'\.\d{2,3}$', next_doc.file_name or ""):
                            break
                    except Exception:
                        break
            else:
                part_size = int(getattr(media, "file_size", 0) or 0)
                if part_size <= 0:
                    return web.Response(status=502, text="Telegram media has no usable file size")
                # 🟢 FIX: Restored the missing "msg_id" string literal!
                parts_map.append({"msg_id": msg_id, "start": 0, "end": part_size, "size": part_size})
                global_offset = part_size
        if not parts_map:
            return web.Response(status=404, text="No readable media parts")

        virtual_size = global_offset
        virtual_data_offset = 0
        zip_idx = request.query.get("zip_idx", "")
        
        # 🟢 FIX: Trigger your virtual concatenator perfectly for .zip AND .zip.001
        is_zip = bool(re.search(r'\.zip(\.\d{3})?$', filename.lower()))
        if is_zip:
            async def zip_read(off, length):
                buf = bytearray()
                async for chunk in parallel_stream_generator(primary_client, chat_id, parts_map, off, length):
                    buf.extend(chunk)
                    if len(buf) >= length:
                        break
                return bytes(buf[:length])

            try:
                # 🟢 FAST MAGIC NUMBER CHECK: Prevent 30-second timeouts on fake ZIPs!
                # If an uploader renamed an MKV to .zip.001 to bypass copyright, this detects it instantly.
                magic_bytes = await zip_read(0, 4)
                
                # 'PK' is the universal standard header for actual ZIP files
                if magic_bytes.startswith(b'PK'):
                    playlist = await get_zip_playlist(zip_read, virtual_size)
                    if playlist:
                        target_entry = playlist[0]
                        if zip_idx.isdigit():
                            for track in playlist:
                                if track["original_index"] == int(zip_idx):
                                    target_entry = track
                                    break
                        entry = await resolve_specific_zip_entry(zip_read, target_entry)
                        if entry:
                            # 🟢 CRITICAL SPEED FIX: Narrow scope to specific track bytes
                            virtual_size = entry["comp_size"]  
                            virtual_data_offset = entry["data_offset"] 
                            mime_type = mimetypes.guess_type(entry["name"])[0] or "application/octet-stream"
                            
                            # FORCE WEB-COMPATIBLE MIME TYPES
                            if entry["name"].lower().endswith('.mp3'): mime_type = "audio/mpeg"
                            elif entry["name"].lower().endswith(('.m4a', '.aac')): mime_type = "audio/mp4"
                            elif entry["name"].lower().endswith('.flac'): mime_type = "audio/flac"
                            elif entry["name"].lower().endswith('.ogg'): mime_type = "audio/ogg"
                            
                            filename = entry["name"]
                else:
                    logger.info("🎬 Fake ZIP detected (MKV/MP4 renamed to .zip.001). Bypassing ZIP Engine...")
                    
            except Exception as e:
                # 🟢 CATCH TIMEOUTS & BAD ZIPS: If Telegram rejects the ZIP probe, fallback gracefully!
                logger.warning(f"ZIP probe failed (Fallback to raw stream): {e}")

        if virtual_size <= 0:
            return web.Response(status=502, text="Invalid virtual media size")

        range_header = request.headers.get("Range", "")
        start_byte = 0
        end_byte = virtual_size - 1
        if range_header:
            match = re.match(r"bytes=(\d*)-(\d*)", range_header)
            if match:
                first, last = match.group(1), match.group(2)
                if first:
                    start_byte = int(first)
                    if last:
                        end_byte = min(int(last), virtual_size - 1)
                elif last:
                    suffix_len = int(last)
                    if suffix_len > 0:
                        start_byte = max(0, virtual_size - suffix_len)
                        end_byte = virtual_size - 1

        if start_byte < 0 or start_byte >= virtual_size or end_byte < start_byte:
            return web.Response(status=416, headers={"Content-Range": f"bytes */{virtual_size}"})

        chunk_len = end_byte - start_byte + 1
        
        if "GLOBAL_STREAM_TASKS" not in globals():
            global GLOBAL_STREAM_TASKS
            GLOBAL_STREAM_TASKS = {}
            
        # 🟢 FIX: Make the lock key unique with a UUID so simultaneous parallel requests 
        # from VLC or FFmpeg don't aggressively cancel each other out, 
        # while still allowing the Web UI "Stop" button to kill them cleanly!
        import uuid
        client_ip = request.remote or "unknown_ip"
        lock_key = f"{user_id}_{chat_id}_{msg_id}_{client_ip}_{uuid.uuid4().hex}"
        
        GLOBAL_STREAM_TASKS[lock_key] = asyncio.current_task()

        headers = {
            "Accept-Ranges": "bytes",
            "Content-Length": str(chunk_len),
            "Content-Type": mime_type,
            "Content-Range": f"bytes {start_byte}-{end_byte}/{virtual_size}",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Expose-Headers": "Content-Length, Content-Range, Accept-Ranges, Content-Type",
            "Cache-Control": "no-store",
        }

        if request.method == "HEAD":
            return web.Response(status=206 if range_header else 200, headers=headers)

        import aiohttp
        response = web.StreamResponse(status=206 if range_header else 200, headers=headers)
        
        adjusted_start = start_byte + virtual_data_offset
        gen = parallel_stream_generator(primary_client, chat_id, parts_map, adjusted_start, chunk_len)
        
        sid = _track_stream(request, filename, user_id)
        try:
            await response.prepare(request)
            async for chunk in gen:
                await response.write(chunk)
            await response.write_eof()
        except (ConnectionResetError, asyncio.CancelledError, aiohttp.client_exceptions.ClientConnectionResetError, BrokenPipeError, ConnectionAbortedError):
            pass # Normal browser disconnects ignored
        except Exception as exc:
            if "Connection closed" not in str(exc) and "BrokenPipeError" not in str(exc):
                logger.debug(f"Telegram stream disconnect/error: {exc}")
        finally:
            _untrack_stream(sid)
            if hasattr(gen, 'aclose'):
                try: 
                    await asyncio.wait_for(gen.aclose(), timeout=1.0)
                except Exception:
                    pass
            
        if not response.prepared:
            return web.Response(status=499, text="Client Closed Request")
        return response

    except asyncio.CancelledError:
        raise
    except Exception as exc:
        logger.exception(f"Telegram stream failed: {exc}")
        if response is None or not getattr(response, 'prepared', False):
            return web.Response(status=502, text="Telegram stream failed")
        return response
    finally:
        if temp_client is not None:
            try:
                await temp_client.disconnect()
            except Exception:
                pass

SUBTITLE_CACHE = {}
SUBTITLE_CACHE_TTL = 3600
SUBTITLE_LOCKS = defaultdict(asyncio.Lock)

async def _api_subtitles_handler(request):
    """Extract embedded subtitle once, cache the WebVTT, and serve it fast thereafter."""
    try:
        user_id = int(request.query.get("user_id", 0))
    except Exception:
        user_id = 0
    link = request.query.get("link", "").strip()
    
    # 🟢 CRITICAL FIX: Accept both 'sub_idx' and 'index' to ensure compatibility with all Javascript fetchers
    sub_idx = request.query.get("sub_idx", request.query.get("index", "0")).strip()
    
    zip_idx = request.query.get("zip_idx", "").strip()
    if not link or not sub_idx:
        return web.Response(status=400, text="Invalid Link or Subtitle Index")

    is_tg = _is_tg_link(link)
    logger.info(f"📝 [SUBTITLES] Extract Request | User: {user_id} | Is TG: {is_tg} | Sub_Idx: {sub_idx} | Link: {link[:60]}...")

    # 🟢 FIX: Include zip_idx in the cache key so different tracks in an album don't overwrite each other!
    cache_key = f"{user_id}:{link}:{sub_idx}:{zip_idx}"
    now = time.time()
    cached = SUBTITLE_CACHE.get(cache_key)
    if cached and cached[1] > now:
        body = cached[0]
        return web.Response(body=body, status=200, headers={
            "Content-Type": "text/vtt; charset=utf-8",
            "Content-Length": str(len(body)),
            "Access-Control-Allow-Origin": "*",
            "Cache-Control": "public, max-age=3600",
        })

    actual_url = link
    if is_tg:
        parsed = _parse_source_link(link)
        chat_id = parsed.get("chat_id")
        msg_id = parsed.get("msg_id")
        msg_range = parsed.get("msg_range") # 🟢 Extract range
        if chat_id is None or msg_id is None:
            return web.Response(status=400, text="Invalid Telegram link")
        actual_url = f"http://127.0.0.1:{PORT}/api/tg_stream?user_id={user_id}&chat_id={chat_id}&msg_id={msg_id}"
        if msg_range:
            actual_url += f"&range={msg_range[0]}-{msg_range[1]}" 
        if zip_idx:
            actual_url += f"&zip_idx={zip_idx}" 
    else:
        # 🟢 CRITICAL FIX: Route FFmpeg through internal proxy so subtitle extraction doesn't stall on CDNs
        from urllib.parse import quote
        if zip_idx:
            actual_url = f"http://127.0.0.1:{PORT}/api/direct_stream?user_id={user_id}&url={quote(link, safe='')}&zip_idx={zip_idx}"
        else:
            actual_url = f"http://127.0.0.1:{PORT}/api/direct_stream?user_id={user_id}&url={quote(link, safe='')}"

    # 🟢 FIX: Extract Embedded Metadata Lyrics directly using Bulletproof JSON!
    if sub_idx == "metadata_lyrics":
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format_tags:stream_tags",
            "-of", "json",
            actual_url
        ]
            
        try:
            proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.DEVNULL)
            stdout, _ = await proc.communicate()
            import json
            
            try:
                data = json.loads(stdout.decode('utf-8', errors='ignore') or '{}')
            except Exception:
                data = {}
                
            raw_text = ""
            
            # Combine format tags (Container) and stream tags (Audio Track)
            tags = data.get("format", {}).get("tags", {})
            for stream in data.get("streams", []):
                tags.update(stream.get("tags", {}))
                
            # Scan all keys to find standard and non-standard Lyrics identifiers
            for key, val in tags.items():
                k_upper = key.upper()
                if "LYRIC" in k_upper or k_upper in ["SYLT", "USLT", "UNSYNCEDLYRICS"]:
                    raw_text += str(val) + "\n"
            
            # Decode literal string newlines correctly
            raw_text = raw_text.replace('\\r\\n', '\n').replace('\\n', '\n')
            body = raw_text.encode('utf-8')
            
            if not body.strip():
                return web.Response(status=404, text="No lyrics found")
                
            SUBTITLE_CACHE[cache_key] = (bytes(body), time.time() + SUBTITLE_CACHE_TTL)
            return web.Response(body=body, status=200, headers={
                "Content-Type": "text/vtt; charset=utf-8",
                "Content-Length": str(len(body)),
                "Access-Control-Allow-Origin": "*",
                "Cache-Control": "public, max-age=3600",
            })
        except Exception as exc:
            return web.Response(status=502, text=str(exc))

    import sys
    
    # 🟢 FIX 1: Set 15MB probesize so files with 40+ tracks (like your 44-stream MKV) are completely indexed
    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error",
        "-user_agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36", 
        "-rw_timeout", "60000000", 
        "-reconnect", "1", "-reconnect_streamed", "1", "-reconnect_delay_max", "5",
        "-seekable", "1", "-multiple_requests", "1",
        "-probesize", "15000000", "-analyzeduration", "15000000",
        "-i", actual_url,
        "-map", f"0:{sub_idx}",
        "-vn", "-an",
        "-c:s", "webvtt",
        "-f", "webvtt",
        "pipe:1"
    ]

    try:
        # 🟢 FIX 2: Capture stderr so errors are visible in logs instead of silent failures
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await proc.communicate()
        stderr_msg = stderr.decode('utf-8', errors='ignore').strip()

        # 🟢 FIX 3: Explicit YES / NO log output with exact error reasons
        if proc.returncode != 0 or not stdout.strip():
            logger.error(f"❌ [SUBTITLES STATUS] Track #{sub_idx} | Loaded: NO | Error: {stderr_msg or 'Empty stream or unsupported codec'}")
            return web.Response(
                body=b"WEBVTT\n\nNOTE Empty or unsupported subtitle stream\n",
                status=200,
                headers={"Content-Type": "text/vtt; charset=utf-8", "Access-Control-Allow-Origin": "*"}
            )

        logger.info(f"✅ [SUBTITLES STATUS] Track #{sub_idx} | Loaded: YES | Bytes: {len(stdout)} | Status: READY")

        # Save to RAM cache for instant loads
        SUBTITLE_CACHE[cache_key] = (stdout, time.time() + SUBTITLE_CACHE_TTL)
        if len(SUBTITLE_CACHE) > 128:
            oldest = min(SUBTITLE_CACHE.items(), key=lambda kv: kv[1][1])[0]
            SUBTITLE_CACHE.pop(oldest, None)
            
        return web.Response(
            body=stdout, 
            status=200, 
            headers={
                "Content-Type": "text/vtt; charset=utf-8",
                "Content-Length": str(len(stdout)),
                "Access-Control-Allow-Origin": "*",
                "Cache-Control": "public, max-age=3600"
            }
        )
        
    except Exception as exc:
        try: proc.kill()
        except: pass
        logger.error(f"❌ [SUBTITLES STATUS] Track #{sub_idx} | Loaded: NO | Exception: {exc}")
        return web.Response(status=502, text=str(exc))
            
