import sys
import os
import re
import asyncio
from urllib.parse import quote, unquote
from aiohttp import web

async def _api_stream_handler(request):
    """
    Dynamic adaptive stream pipeline:
    - Direct 302 Pass-Through for External Players & 100% Native Web Media
    - Zero-CPU Remux (-c:v copy -c:a copy) when container is incompatible (e.g. MKV) but streams are supported
    - Partial Transcode (transcode video, copy audio OR transcode audio, copy video)
    - Dynamic Client Device Negotiation (iOS/Safari, Chrome/Firefox, VLC/MPV)
    """
    try:
        user_id = int(request.query.get("user_id", 0))
    except Exception:
        user_id = 0

    link = request.query.get("link", "").strip()
    quality = request.query.get("quality", "Original")
    audio_idx = request.query.get("audio_idx", None)
    audio_codec_req = request.query.get("audio_codec", "").lower().strip()
    start_time = request.query.get("start", None)
    force_transcode = request.query.get("transcode", "") in ("1", "true")
    force_x264 = request.query.get("force_x264", "") == "1"
    zip_idx = request.query.get("zip_idx", "").strip()

    if not link:
        return web.Response(status=400, text="No link provided")

    # --- 1. CLIENT DEVICE & CAPABILITY PROFILING ---
    ua = request.headers.get("User-Agent", "").lower()
    is_external = (
        request.query.get("external", "") == "1"
        or any(p in ua for p in ("vlc", "mpv", "potplayer", "infuse", "kodi", "exoplayer"))
    )
    is_apple = (
        ("safari" in ua and "chrome" not in ua and "android" not in ua)
        or "applecoremedia" in ua
        or "iphone" in ua
        or "ipad" in ua
        or "macintosh" in ua
    )

    # Client-reported capabilities via query parameters
    client_supports_hevc = request.query.get("hevc", "") in ("1", "true") or is_apple or is_external
    client_supports_ac3 = request.query.get("ac3", "") in ("1", "true") or is_apple or is_external
    client_supports_opus = request.query.get("opus", "") in ("1", "true") or ("chrome" in ua or "firefox" in ua or is_external)
    client_supports_flac = request.query.get("flac", "") in ("1", "true") or ("chrome" in ua or "firefox" in ua or is_apple or is_external)
    client_supports_vp9 = request.query.get("vp9", "") in ("1", "true") or ("chrome" in ua or "firefox" in ua or "android" in ua or is_external)
    client_supports_av1 = request.query.get("av1", "") in ("1", "true") or is_external

    is_tg = _is_tg_link(link)
    logger.info(f"🎬 [STREAM] User: {user_id} | Apple: {is_apple} | Ext: {is_external} | HEVC_Cap: {client_supports_hevc} | Link: {link[:80]}...")

    # --- 2. SOURCE LINK & PROXY RESOLUTION ---
    try:
        if is_tg:
            parsed = _parse_source_link(link)
            chat_id = parsed.get("chat_id")
            msg_id = parsed.get("msg_id")
            msg_range = parsed.get("msg_range")
            if chat_id is None or msg_id is None:
                return web.Response(status=400, text="Invalid Telegram link")
            
            pool, _ = await _get_working_tg_pool(user_id, chat_id, msg_id)
            if not pool:
                return web.Response(status=403, text="Telegram file inaccessible")
            msg = await get_client_msg(pool[0], chat_id, msg_id)
            media = msg.document or msg.video or msg.audio
            if not media:
                return web.Response(status=404, text="Media not found")
            
            filename = str(getattr(media, "file_name", "") or "").lower()
            mime_type = getattr(media, "mime_type", "video/mp4") or "video/mp4"
            actual_url = f"http://127.0.0.1:{PORT}/api/tg_stream?user_id={user_id}&chat_id={chat_id}&msg_id={msg_id}"
            if msg_range:
                actual_url += f"&range={msg_range[0]}-{msg_range[1]}"
            if zip_idx:
                actual_url += f"&zip_idx={zip_idx}"
            
            direct_stream_url = actual_url
        else:
            resolved_cdn = await resolve_direct_link(link)
            filename = _guess_filename_from_url(resolved_cdn, "direct_media", original_url=link).lower()
            
            if re.search(r'\.(7z|rar|tar|gz|iso|bin)(\.\d{3})?$', filename) or re.search(r'\.(part\d+|z\d+|r\d\d)$', filename):
                return web.Response(status=400, text="Compressed solid archives cannot be streamed.")

            # Loopback URL for FFmpeg to guarantee auth cookies and range compliance
            actual_url = f"http://127.0.0.1:{PORT}/api/direct_stream?user_id={user_id}&url={quote(link, safe='')}"
            if zip_idx:
                actual_url += f"&zip_idx={zip_idx}"
            direct_stream_url = actual_url
    except Exception as exc:
        return web.Response(status=502, text=f"Source resolution error: {exc}")

    # --- 3. METADATA & STREAM PROFILE EXTRACTION ---
    cache_key = _media_cache_key(user_id, link) + ":tags_False"
    cached_meta = MEDIA_META_CACHE.get(cache_key)
    video_codec = ""
    audio_codec = audio_codec_req
    channels = 2
    pix_fmt = "yuv420p"

    if cached_meta:
        meta = cached_meta[0]
        video_codec = (meta.get("video_codec") or "").lower()
        if not audio_codec:
            audio_codec = (meta.get("audio_codec") or "").lower()
        
        streams = meta.get("streams", [])
        for s in streams:
            if s.get("codec_type") == "video" and s.get("codec_name") not in {"mjpeg", "png", "bmp", "webp"}:
                pix_fmt = s.get("pix_fmt", "yuv420p").lower()
                break
            if s.get("codec_type") == "audio":
                channels = int(s.get("channels") or 2)

    is_audio = (not video_codec and bool(audio_codec)) or filename.endswith(
        (".flac", ".mp3", ".m4a", ".ogg", ".wav", ".aac", ".wma", ".opus", ".dsf", ".ape", ".mka", ".alac")
    )
    is_mkv_or_non_mp4 = filename.endswith((".mkv", ".mka", ".avi", ".wmv", ".flv", ".ts", ".m2ts", ".vob", ".webm"))

    # --- 4. DYNAMIC CODEC DECISION MATRIX ---
    # External players bypass all server-side processing
    if is_external and not force_transcode:
        raise web.HTTPFound(direct_stream_url)

    # VIDEO COPY DECISION
    copy_video = False
    if not is_audio:
        if quality == "Original" and not force_x264 and not force_transcode:
            # H.264: Universally supported, EXCEPT 10-bit (Hi10P) which breaks on mobile hardware
            if video_codec in {"h264", "avc", "avc1"}:
                copy_video = "10" not in pix_fmt
            # HEVC / H.265: Copy ONLY if client supports it (Safari, Edge/Chrome with HEVC flag)
            elif video_codec in {"hevc", "h265", "hvc1", "hev1"}:
                copy_video = client_supports_hevc
            # VP8 / VP9 / AV1: Native in modern browsers
            elif video_codec in {"vp8", "vp9"}:
                copy_video = client_supports_vp9
            elif video_codec in {"av1", "av01"}:
                copy_video = client_supports_av1

    # AUDIO COPY DECISION
    copy_audio = False
    if audio_codec in {"aac", "mp3"}:
        # Standard AAC and MP3 stereo can always be copied
        copy_audio = (channels <= 2) or client_supports_ac3
    elif audio_codec in {"opus", "vorbis"}:
        copy_audio = client_supports_opus
    elif audio_codec == "flac":
        copy_audio = client_supports_flac
    elif audio_codec in {"ac3", "eac3"}:
        copy_audio = client_supports_ac3
    # DTS, TrueHD, WMA, ALAC, raw PCM will always transcode to AAC

    # Check if native pass-through without FFmpeg is possible
    if (not is_mkv_or_non_mp4) and copy_video and copy_audio and (audio_idx is None) and not force_transcode:
        raise web.HTTPFound(direct_stream_url)

    # --- 5. BUILD OPTIMIZED FFMPEG COMMAND ---
    # Use 1MB-2MB probe limits to eliminate the 15-30s delay on throttled hosts
    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error",
        "-user_agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "-rw_timeout", "60000000",
        "-reconnect", "1", "-reconnect_streamed", "1", "-reconnect_delay_max", "5",
        "-reconnect_at_eof", "1", "-reconnect_on_network_error", "1",
        "-seekable", "1",
        "-probesize", "1500000", "-analyzeduration", "2000000",
        "-fflags", "+genpts+igndts"
    ]

    if start_time is not None:
        try:
            start_f = max(0.0, float(start_time))
            if start_f > 0:
                cmd += ["-ss", f"{start_f:.3f}"]
        except Exception:
            pass

    cmd += ["-i", actual_url]

    # Audio-only pipeline
    if is_audio:
        if audio_idx is not None and str(audio_idx).strip():
            cmd += ["-map", f"0:{audio_idx}"]
        else:
            cmd += ["-map", "0:a:0?"]
        cmd += ["-vn", "-sn"]

        if copy_audio and audio_codec == "mp3":
            cmd += ["-c:a", "copy", "-f", "mp3", "pipe:1"]
            mime_type = "audio/mpeg"
        elif copy_audio and audio_codec in {"opus", "vorbis"}:
            cmd += ["-c:a", "copy", "-f", "ogg", "pipe:1"]
            mime_type = "audio/ogg"
        elif copy_audio and audio_codec == "flac":
            cmd += ["-c:a", "copy", "-f", "flac", "pipe:1"]
            mime_type = "audio/flac"
        elif copy_audio and audio_codec == "aac":
            cmd += ["-c:a", "copy", "-f", "adts", "pipe:1"]
            mime_type = "audio/aac"
        else:
            # Universal fallback for DTS, TrueHD, PCM, etc.
            cmd += ["-c:a", "aac", "-b:a", "192k", "-ac", "2", "-af", "aresample=async=1000", "-f", "adts", "pipe:1"]
            mime_type = "audio/aac"

    # Video (+ Audio) pipeline
    else:
        cmd += ["-map", "0:v:0?"]
        if audio_idx is not None and str(audio_idx).strip():
            cmd += ["-map", f"0:{audio_idx}"]
        else:
            cmd += ["-map", "0:a:0?"]
        cmd += ["-sn"]  # Subtitles extracted dynamically via /api/subtitles to prevent blocking video stream

        res_scale_map = {"4K": "3840:-2", "1080p": "1920:-2", "720p": "1280:-2", "480p": "854:-2", "360p": "640:-2"}
        scale_filter = res_scale_map.get(quality)

        # Video stream handling
        if copy_video and not scale_filter:
            cmd += ["-c:v", "copy"]
            if video_codec in {"hevc", "h265", "hvc1", "hev1"}:
                cmd += ["-tag:v", "hvc1"]  # Mandatory for Safari/iOS & MP4 container playback
        else:
            scale_cmd = scale_filter or "trunc(iw/2)*2:trunc(ih/2)*2"
            cmd += [
                "-vf", f"scale={scale_cmd}",
                "-c:v", "libx264", "-preset", "ultrafast", "-tune", "zerolatency",
                "-pix_fmt", "yuv420p", "-threads", "0"
            ]

        # Audio stream handling
        if copy_audio:
            cmd += ["-c:a", "copy"]
        else:
            cmd += [
                "-c:a", "aac", "-b:a", "192k", "-ac", "2",
                "-af", "aresample=async=1000:min_hard_comp=0.100000:first_pts=0"
            ]

        cmd += [
            "-avoid_negative_ts", "make_zero",
            "-max_muxing_queue_size", "9999",
            "-movflags", "frag_keyframe+empty_moov+default_base_moof",
            "-muxdelay", "0",
            "-f", "mp4", "pipe:1"
        ]
        mime_type = "video/mp4"

    logger.info(f"🎬 [DYNAMIC TRANSCODE] Video Copy: {copy_video} | Audio Copy: {copy_audio} | File: {filename}")
    logger.debug(f"🎬 [CMD] {' '.join(cmd)}")

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=sys.stderr
    )

    # --- 6. RANGE & STREAM RESPONSE DISPATCH ---
    stream_headers = {
        "Content-Type": mime_type,
        "Access-Control-Allow-Origin": "*",
        "Cache-Control": "no-store",
    }

    apple_target_length = None
    if is_apple:
        stream_headers["Accept-Ranges"] = "bytes"
        client_range = request.headers.get("Range", "")
        if client_range:
            start_b, end_b = 0, 2147483647
            m = re.match(r"bytes=(\d*)-(\d*)", client_range.strip())
            if m:
                if m.group(1): start_b = int(m.group(1))
                if m.group(2): end_b = int(m.group(2))
            fake_total = 2147483648
            end_b = min(end_b, fake_total - 1)
            stream_headers["Content-Range"] = f"bytes {start_b}-{end_b}/{fake_total}"
            apple_target_length = end_b - start_b + 1
            stream_headers["Content-Length"] = str(apple_target_length)
            status_code = 206
        else:
            stream_headers["Content-Length"] = "2147483648"
            status_code = 200
    else:
        stream_headers["Accept-Ranges"] = "none"
        status_code = 200

    response = web.StreamResponse(status=status_code, headers=stream_headers)
    sid = _track_stream(request, filename, user_id)
    try:
        await response.prepare(request)
        bytes_sent = 0
        while True:
            chunk = await proc.stdout.read(262144)
            if not chunk:
                break
            if is_apple and apple_target_length is not None:
                if bytes_sent + len(chunk) >= apple_target_length:
                    chunk = chunk[:apple_target_length - bytes_sent]
                    await response.write(chunk)
                    break
            await response.write(chunk)
            bytes_sent += len(chunk)
        await response.write_eof()
    except (ConnectionResetError, asyncio.CancelledError, Exception):
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
