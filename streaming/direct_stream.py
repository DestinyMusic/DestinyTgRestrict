# ==============================================================================
# --- HIGH-PERFORMANCE STREAMING, TRANSCODING & PROBE ENGINE ---
# ==============================================================================

def _is_tg_link(link):
    """Strictly separate Telegram Links from Direct Links to prevent intermixing."""
    if not link: return False
    return bool(re.search(r"^(?:https?://)?(?:www\.)?(?:t\.me|telegram\.me)\/", str(link).strip().lower()))

DIRECT_URL_CACHE = {}
DIRECT_URL_CACHE_TTL = 900
DIRECT_RESOLVE_LOCKS = defaultdict(asyncio.Lock)
DIRECT_HEADER_CACHE = {}
DIRECT_HTTP_SESSION = None
DIRECT_HTTP_SESSION_LOCK = asyncio.Lock()

import yarl

def _safe_yarl(u):
    """Prevents aiohttp from double-encoding Terabox security signatures."""
    try:
        return yarl.URL(u, encoded=True) if '%' in u else u
    except Exception:
        return u

async def _get_direct_http_session():
    """Shared HTTP client with keep-alive/DNS reuse for direct media hosts."""
    global DIRECT_HTTP_SESSION
    if DIRECT_HTTP_SESSION is not None and not DIRECT_HTTP_SESSION.closed:
        return DIRECT_HTTP_SESSION
    async with DIRECT_HTTP_SESSION_LOCK:
        if DIRECT_HTTP_SESSION is None or DIRECT_HTTP_SESSION.closed:
            connector = aiohttp.TCPConnector(
                limit=100,          
                limit_per_host=20, 
                ttl_dns_cache=60, 
                keepalive_timeout=30, 
                enable_cleanup_closed=True,
            )
            timeout = aiohttp.ClientTimeout(total=None, connect=8, sock_connect=8, sock_read=15)
            DIRECT_HTTP_SESSION = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
                headers={
                    # 🟢 CRITICAL: Must match direct_link_generator.py exactly to prevent Gofile 400 Errors!
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
                },
            )
    return DIRECT_HTTP_SESSION

async def _close_direct_http_session():
    global DIRECT_HTTP_SESSION
    session = DIRECT_HTTP_SESSION
    DIRECT_HTTP_SESSION = None
    if session is not None and not session.closed:
        try:
            await session.close()
        except Exception:
            pass

async def resolve_direct_link(url):
    """Resolve common file-host pages to a stream URL, with coalesced/cached resolution."""
    original = str(url or '').strip()
    if not original:
        return original

    now = time.time()
    
    cached = DIRECT_URL_CACHE.get(original)
    if cached and cached[1] > now:
        return cached[0]
        
    if original in DIRECT_HEADER_CACHE:
        DIRECT_URL_CACHE[original] = (original, now + DIRECT_URL_CACHE_TTL)
        return original

    lock = DIRECT_RESOLVE_LOCKS[original]
    async with lock:
        now = time.time()
        cached = DIRECT_URL_CACHE.get(original)
        if cached and cached[1] > now:
            return cached[0]
        if original in DIRECT_HEADER_CACHE:
            return original

        result = original
        session = await _get_direct_http_session()

        from streaming.link_resolver import resolve_universal_link
        unv_url, unv_headers = await resolve_universal_link(original)
        
        if unv_url != original:
            if unv_headers:
                # 🟢 CRITICAL FIX: Store headers ONLY under the resolved CDN url!
                # This prevents loopback requests from erasing the cookies.
                DIRECT_HEADER_CACHE[unv_url] = unv_headers
            DIRECT_URL_CACHE[original] = (unv_url, now + DIRECT_URL_CACHE_TTL)
            return unv_url

        pixel_match = re.search(r"pixeldrain\.com/u/([a-zA-Z0-9_-]+)", original)
        if pixel_match:
            result = f"https://cdn.pixeldrain.eu.cc/{pixel_match.group(1)}"

        if "dropbox.com" in original:
            result = original.replace("?dl=0", "?dl=1").replace("&dl=0", "&dl=1")
            if "?dl=1" not in result and "&dl=1" not in result:
                result += "?dl=1"

        if result == original and ("onedrive.live.com" in original or "sharepoint.com" in original):
            result += "&download=1" if "?" in original else "?download=1"

        if result == original and "huggingface.co" in original and "/blob/" in original:
            result = original.replace("/blob/", "/resolve/")

        if result == original and "mediafire.com/file/" in original:
            try:
                async with session.get(original, allow_redirects=True) as r:
                    html_text = await r.text(errors='ignore')
                    m = re.search(r'href="(https?://download[^"]+)"\s+id="downloadButton"', html_text, re.I)
                    if m:
                        result = m.group(1)
            except Exception: pass

        if result == original:
            gdrive_match = re.search(r"drive\.google\.com/(?:file/d/|open\?id=|uc\?id=)([a-zA-Z0-9_-]+)", original)
            if gdrive_match:
                file_id = gdrive_match.group(1)
                scan_url = f"https://drive.google.com/uc?id={file_id}&export=download"
                try:
                    async with session.get(scan_url, allow_redirects=True) as r:
                        text = await r.text(errors='ignore')
                        confirm_match = re.search(r"confirm=([a-zA-Z0-9_-]+)", text)
                        if confirm_match:
                            result = f"https://drive.google.com/uc?id={file_id}&export=download&confirm={confirm_match.group(1)}"
                        elif "download_warning" in str(r.url):
                            m = re.search(r"confirm=([a-zA-Z0-9_-]+)", str(r.url))
                            if m:
                                result = f"https://drive.google.com/uc?id={file_id}&export=download&confirm={m.group(1)}"
                            else:
                                result = f"https://drive.google.com/uc?id={file_id}&export=download&confirm=t"
                        else:
                            result = str(r.url)
                except Exception: pass

        if result == original:
            try:
                u_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                async with session.get(original, headers=u_headers, allow_redirects=True) as r:
                    content_type = r.headers.get("Content-Type", "").lower()
                    if "text/html" in content_type:
                        html_text = await r.text(errors='ignore')
                        m = re.search(r'(?:<source[^>]+src=["\']|<video[^>]+src=["\'])(https?://[^"\']+\.(?:mp4|mkv|webm|m4v|mp3|m4a|flac|opus)(?:\?[^"\']*)?)["\']', html_text, re.I)
                        if m:
                            result = m.group(1).replace('&amp;', '&')
                        else:
                            m = re.search(r'href=["\'](https?://[^"\']+\.(?:mp4|mkv|webm|m4v|mp3|m4a|flac|opus)(?:\?[^"\']*)?)["\']', html_text, re.I)
                            if m:
                                result = m.group(1).replace('&amp;', '&')
                    else:
                        result = str(r.url) 
            except Exception: pass

        if result == original:
            if original not in DIRECT_HEADER_CACHE or "Cookie" not in DIRECT_HEADER_CACHE[original]:
                try:
                    async with session.get(
                        original,
                        headers={"Range": "bytes=0-0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0"},
                        allow_redirects=True,
                    ) as r:
                        result = str(r.url)
                        if r.status < 400: 
                            DIRECT_HEADER_CACHE[original] = {
                                "meta_content_type": r.headers.get("Content-Type", "").split(';')[0],
                                "meta_content_length": r.headers.get("Content-Length"),
                                "meta_content_range": r.headers.get("Content-Range"),
                                "meta_accept_ranges": r.headers.get("Accept-Ranges"),
                                "meta_content_disposition": r.headers.get("Content-Disposition", ""),
                            }
                except Exception:
                    result = original

        DIRECT_URL_CACHE[original] = (result, now + DIRECT_URL_CACHE_TTL)
        return result

async def _direct_upstream_request(url, request):
    """Open a direct HTTP source through the shared keep-alive session."""
    resolved = await resolve_direct_link(url)
    session = await _get_direct_http_session()
    
    from urllib.parse import urlparse
    
    # 🟢 FIX: Mimic a real browser precisely to bypass Cloudflare Worker 502/403s!
    req_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5",
        "Accept-Language": "en-US,en;q=0.5",
        "Sec-Fetch-Dest": "video",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "cross-site",
    }
    
    for header in (
        "Range", "If-Range", "If-Modified-Since", "If-None-Match", "Cookie"
    ):
        value = request.headers.get(header)
        if value:
            req_headers[header] = value

    # Smart Referer & Origin Injection for Worker Bypasses
    client_referer = request.headers.get("Referer")
    if client_referer:
        req_headers["Referer"] = client_referer
    else:
        parsed_res = urlparse(resolved)
        req_headers["Referer"] = f"{parsed_res.scheme}://{parsed_res.netloc}/"
        req_headers["Origin"] = f"{parsed_res.scheme}://{parsed_res.netloc}"

    resp = await session.request(
        method=request.method,
        url=resolved,
        headers=req_headers,
        allow_redirects=True,
    )
    
    # Log upstream worker errors for debugging
    if resp.status in (502, 503, 403):
        logger.warning(f"⚠️ Upstream {resp.status} Error from {resolved[:80]}")
        
    return session, resp, resolved

# --- GLOBAL NETWORK TRACKER ---
GLOBAL_NETWORK_STATS = {"active": {}, "recent": []}

def _track_stream(req, fname, uid):
    sid = uuid.uuid4().hex
    ip = req.headers.get("X-Forwarded-For", req.remote).split(",")[0].strip()
    ua = req.headers.get("User-Agent", "")
    br = "App"
    if "VLC" in ua: br = "VLC"
    elif "mpv" in ua: br = "MPV"
    elif "Chrome" in ua: br = "Chrome"
    elif "Safari" in ua and "Chrome" not in ua: br = "Safari"
    elif "Firefox" in ua: br = "Firefox"
    osn = "Device"
    if "Windows" in ua: osn = "Windows"
    elif "Mac OS" in ua: osn = "macOS"
    elif "Android" in ua: osn = "Android"
    elif "iPhone" in ua or "iPad" in ua: osn = "iOS"
    elif "Linux" in ua: osn = "Linux"
    GLOBAL_NETWORK_STATS["active"][sid] = {
        "ip": ip, "country": req.headers.get("CF-IPCountry", "Unknown"), 
        "device": f"{br} • {osn}", "filename": fname, 
        "start_time": time.time(), "user_id": uid
    }
    return sid

def _untrack_stream(sid):
    if sid in GLOBAL_NETWORK_STATS["active"]:
        entry = GLOBAL_NETWORK_STATS["active"].pop(sid)
        entry["end_time"] = time.time()
        GLOBAL_NETWORK_STATS["recent"].insert(0, entry)
        if len(GLOBAL_NETWORK_STATS["recent"]) > 50: 
            GLOBAL_NETWORK_STATS["recent"].pop()

from streaming.link_resolver import resolve_universal_link

async def _api_direct_stream_handler(request):
    try:
        user_id = int(request.query.get("user_id", 0))
    except Exception:
        user_id = 0
        
    url = request.query.get("url", "").strip()
    logger.info(f"🌐 [DIRECT STREAM] Proxying {request.method} request for: {url[:100]}...")
    if not url or not url.lower().startswith(("http://", "https://")):
        return web.Response(status=400, text="Invalid direct media URL")

    resolved = await resolve_direct_link(url)
    filename = _guess_filename_from_url(resolved, "direct_media", original_url=url).lower()
    
    is_zip = bool(re.search(r'\.(zip|7z|rar|tar|gz)(\.\d{3})?$', filename))
    
    session = await _get_direct_http_session()
    virtual_size = -1
    virtual_data_offset = 0
    mime_type = None

    zip_idx = request.query.get("zip_idx", "")
    if is_zip:
        try:
            zip_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0"}
            cached_h = DIRECT_HEADER_CACHE.get(resolved) or DIRECT_HEADER_CACHE.get(url) or {}
            
            for h_key in ["Cookie", "Referer", "Authorization", "User-Agent"]:
                if h_key in cached_h: 
                    zip_headers[h_key] = cached_h[h_key]

            raw_size = int(cached_h.get("meta_content_length", 0))
            if raw_size <= 0:
                try:
                    # 🟢 FAST NATIVE STRING (No _safe_yarl corruption)
                    async with session.head(resolved, headers=zip_headers, allow_redirects=True) as h_resp:
                        raw_size = int(h_resp.headers.get("Content-Length", 0))
                except Exception: pass
            
            if raw_size <= 0:
                try:
                    get_h = zip_headers.copy()
                    get_h["Range"] = "bytes=0-0"
                    async with session.get(resolved, headers=get_h, allow_redirects=True) as g_resp:
                        cr = g_resp.headers.get("Content-Range", "")
                        if cr and "/" in cr:
                            raw_size = int(cr.split("/")[-1])
                        else:
                            raw_size = int(g_resp.headers.get("Content-Length", 0))
                except Exception: pass
            
            if raw_size > 0:
                async def zip_read_http(off, length):
                    z_req_headers = zip_headers.copy()
                    z_req_headers["Range"] = f"bytes={off}-{off+length-1}"
                    async with session.get(resolved, headers=z_req_headers) as r:
                        return await r.read()
                
                magic_bytes = await zip_read_http(0, 4)
                if magic_bytes.startswith(b'PK'):
                    playlist = await get_zip_playlist(zip_read_http, raw_size)
                    if playlist:
                        target_entry = playlist[0]
                        if zip_idx.isdigit():
                            for track in playlist:
                                if track["original_index"] == int(zip_idx):
                                    target_entry = track
                                    break
                        entry = await resolve_specific_zip_entry(zip_read_http, target_entry)
                        if entry:
                            virtual_size = entry["comp_size"]
                            virtual_data_offset = entry["data_offset"]
                            mime_type = mimetypes.guess_type(entry["name"])[0] or "application/octet-stream"
                            
                            if entry["name"].lower().endswith('.mp3'): mime_type = "audio/mpeg"
                            elif entry["name"].lower().endswith(('.m4a', '.aac')): mime_type = "audio/mp4"
                            elif entry["name"].lower().endswith('.flac'): mime_type = "audio/flac"
                            elif entry["name"].lower().endswith('.ogg'): mime_type = "audio/ogg"
                            
                            filename = entry["name"]
                else:
                    logger.info("🎬 Fake HTTP ZIP detected. Bypassing ZIP Engine...")
        except Exception as e:
            logger.warning(f"Direct ZIP resolution failed: {e}")

    req_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
        "Accept": "video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5",
    }
    
    cached_h = DIRECT_HEADER_CACHE.get(resolved) or DIRECT_HEADER_CACHE.get(url) or {}
    for h_key in ["Cookie", "Referer", "Authorization", "User-Agent"]:
        if h_key in cached_h:
            req_headers[h_key] = cached_h[h_key]
            
    client_range = request.headers.get("Range", "")
    start_byte = 0
    end_byte = None
    
    if client_range:
        match = re.match(r"bytes=(\d*)-(\d*)", client_range)
        if match:
            if match.group(1): start_byte = int(match.group(1))
            if match.group(2): end_byte = int(match.group(2))
    
    if virtual_size > 0:
        if end_byte is None or end_byte >= virtual_size:
            end_byte = virtual_size - 1
        real_start = start_byte + virtual_data_offset
        real_end = end_byte + virtual_data_offset
        req_headers["Range"] = f"bytes={real_start}-{real_end}"
    else:
        if client_range:
            req_headers["Range"] = client_range

    for header in ("If-Range", "If-Modified-Since", "If-None-Match"):
        val = request.headers.get(header)
        if val: req_headers[header] = val

    try:
        # 🟢 FAST NATIVE STRING
        remote = await session.request(
            method=request.method,
            url=resolved,
            headers=req_headers,
            allow_redirects=True,
        )
    except Exception as exc:
        return web.Response(status=502, text=f"Direct source connection failed: {exc}")

    out_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Expose-Headers": "Content-Length, Content-Range, Accept-Ranges, Content-Disposition, ETag, Last-Modified, Cache-Control",
        "Cache-Control": "public, max-age=300",
        "Accept-Ranges": "bytes"
    }
    
    if virtual_size > 0:
        out_headers["Content-Type"] = mime_type
        chunk_len = end_byte - start_byte + 1
        out_headers["Content-Length"] = str(chunk_len)
        out_headers["Content-Range"] = f"bytes {start_byte}-{end_byte}/{virtual_size}"
        out_status = 206 if client_range else 200
    else:
        copy_headers = ("Content-Length", "Content-Range", "Content-Disposition", "ETag", "Last-Modified")
        for k in copy_headers:
            if remote.headers.get(k) is not None:
                out_headers[k] = remote.headers[k]
                
        upstream_mime = remote.headers.get("Content-Type", "").lower()
        if not upstream_mime or "octet-stream" in upstream_mime or "binary" in upstream_mime:
            import mimetypes
            guessed_mime = mimetypes.guess_type(filename)[0]
            if not guessed_mime:
                if filename.endswith(".mkv"): guessed_mime = "video/x-matroska"
                elif filename.endswith(".webm"): guessed_mime = "video/webm"
                elif filename.endswith((".m4a", ".aac")): guessed_mime = "audio/mp4"
                elif filename.endswith(".flac"): guessed_mime = "audio/flac"
                else: guessed_mime = "video/mp4"
            out_headers["Content-Type"] = guessed_mime
        else:
            out_headers["Content-Type"] = upstream_mime
            
        out_status = remote.status

    if request.method == "HEAD":
        remote.release()
        return web.Response(status=out_status, headers=out_headers)

    response = web.StreamResponse(status=out_status, headers=out_headers)
    sid = _track_stream(request, filename, user_id)
    try:
        await response.prepare(request)
        async for chunk in remote.content.iter_chunked(524288):
            if chunk: await response.write(chunk)
        await response.write_eof()
        return response
    except (ConnectionResetError, asyncio.CancelledError, aiohttp.ClientConnectionError, aiohttp.client_exceptions.ClientConnectionResetError, BrokenPipeError, ConnectionAbortedError):
        return response
    except Exception as exc:
        if "Connection closed" not in str(exc): logger.debug(f"Direct stream disconnect: {exc}")
        return response
    finally:
        _untrack_stream(sid)
        try: remote.release()
        except Exception:
            try: remote.close()
            except Exception: pass

MEDIA_META_CACHE = {}
MEDIA_META_TTL = 600
MEDIA_META_LOCKS = defaultdict(asyncio.Lock)


def _media_cache_key(user_id, link):
    return f"{user_id}:{link.strip()}"


def _guess_filename_from_url(url, fallback="Direct_Stream_Media", original_url=None):
    from urllib.parse import urlparse, parse_qsl, unquote
    import os
    import re
    try:
        for check_url in [original_url, url]:
            if check_url and check_url in DIRECT_HEADER_CACHE:
                # 🟢 Read from the safe meta_ key
                cd = DIRECT_HEADER_CACHE[check_url].get("meta_content_disposition", "")
                if cd:
                    m = re.search(r'filename\*?=(?:UTF-8\'\')?["\']?([^;"\']+)', cd, re.I)
                    if m:
                        return unquote(m.group(1))
                        
        parsed = urlparse(url)
        qs = dict(parse_qsl(parsed.query))
        for k in ['filename', 'name', 'file', 'title', 'path']:
            if k in qs:
                val = unquote(qs[k])
                name = os.path.basename(val)
                if name and "." in name:
                    return name
                elif val and "/" not in val:
                    return val
        
        name = os.path.basename(parsed.path)
        name = unquote(name) if name else fallback
        
        if name.lower() in ["download", "video", "media", "stream", "file", "play", fallback.lower()]:
            return fallback
            
        return name
    except Exception:
        return fallback

def _guess_browser_compatibility(mime_type, filename, streams):
    """Conservative browser-compatibility check used by the native player path."""
    mime = (mime_type or "").lower().split(";", 1)[0]
    import os
    ext = os.path.splitext(str(filename or ""))[1].lower()
    # 🟢 FIX: Ignore cover art so audio files aren't mistakenly treated as videos
    videos = [s for s in (streams or []) if s.get("codec_type") == "video" and s.get("codec_name") not in {"mjpeg", "png", "bmp", "webp"}]
    audios = [s for s in (streams or []) if s.get("codec_type") == "audio"]
    vc = str(videos[0].get("codec_name") if videos else "").lower()
    ac = str(audios[0].get("codec_name") if audios else "").lower()

    # These audio codecs are deliberately kept off the native browser path.
    # They need the compatibility/FFmpeg route for reliable playback.
    bad_audio = {"dts", "truehd", "ac3", "eac3"}

    # Standalone audio: preserve the original stream whenever its codec/MIME
    # is something the browser can consume.
    if not videos:
        if mime in {
            "audio/mpeg", "audio/mp4", "audio/m4a", "audio/aac", "audio/ogg",
            "audio/webm", "audio/wav", "audio/flac", "audio/opus", "audio/x-m4a"
        } or ext in {".m4a", ".mp3", ".aac", ".ogg", ".wav", ".flac", ".opus", ".mka", ".alac"}:
            return ac not in {"dts", "truehd", "ac3", "eac3"}
        return ac in {
            "mp3", "aac", "flac", "opus", "vorbis",
            "pcm_s16le", "pcm_s24le", "pcm_s32le",
            "pcm_s16be", "pcm_s24be", "pcm_s32be",
            "alac", "wavpack"
        }

    # WebM native route.
    if mime == "video/webm" or ext == ".webm":
        return vc in {"vp8", "vp9", "av1"} and ac not in bad_audio

    # MP4/M4V native route. H.264/VP9/AV1 are allowed here; the
    # browser-side player separately remains conservative about audio.
    if ext in {".mp4", ".m4v"} or mime in {"video/mp4", "application/mp4"}:
        # 🟢 FIX 1: Removed 'hevc', 'h265', 'hvc1'. Chrome/Firefox/Android CANNOT play HEVC natively!
        return vc in {
            "h264", "avc", "avc1", "vp9", "av1"
        } and ac not in bad_audio

    return False

