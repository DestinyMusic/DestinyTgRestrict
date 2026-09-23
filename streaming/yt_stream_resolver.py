import asyncio
import os
from yt_dlp import YoutubeDL
import logging
import traceback

logger = logging.getLogger("BotLogger")

def _extract_stream_sync(url: str, use_cookies: bool = True):
    # 🟢 CRITICAL CURE FOR CURL_CFFI THREAD CRASH
    # curl_cffi requires an active event loop to impersonate Chrome.
    # Background threads don't have one by default, which caused the AssertionError!
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

    ydl_opts = {
        "format": "best[ext=mp4]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        
        # 🟢 BROWSER SPOOFING (CURES THE YOUTUBE EOF ERROR)
        "impersonate": "chrome",          # Uses curl_cffi to perfectly mimic Chrome TLS fingerprints
        "force_ipv4": True,               # YouTube blocks IPv6 Datacenters
        "socket_timeout": 15,             
        "extractor_retries": 1,
    }
    
    if use_cookies and os.path.exists("cookies.txt"):
        ydl_opts["cookiefile"] = "cookies.txt"

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        if not info:
            raise ValueError("No video metadata returned")

        stream_url = info.get("url")
        if not stream_url and "formats" in info:
            formats = [f for f in info["formats"] if f.get("url")]
            if formats:
                stream_url = formats[-1]["url"]

        if not stream_url:
            raise ValueError("Direct streamable URL not found")

        return {
            "stream_url": stream_url,
            "headers": info.get("http_headers") or {},
            "title": info.get("title", "Direct Stream"),
            "duration": info.get("duration", 0)
        }

async def resolve_yt_dlp_stream(url: str):
    """Extracts stream URLs. Automatically falls back to cookie-less mode."""
    try:
        # 🟢 Attempt 1: With Cookies
        return await asyncio.to_thread(_extract_stream_sync, url, True)
    except Exception as e:
        error_details = traceback.format_exc()
        logger.warning(f"yt-dlp stream resolution failed (Cookies Active):\n{error_details}")
        
        # 🟢 Attempt 2: Unconditional Fallback! 
        # If it fails for ANY reason with cookies, try instantly without them!
        try:
            logger.info("🔄 Retrying yt-dlp without cookies to bypass Auth/TLS drop...")
            return await asyncio.to_thread(_extract_stream_sync, url, False)
        except Exception as e2:
            error_details_2 = traceback.format_exc()
            logger.warning(f"yt-dlp stream resolution failed (No Cookies):\n{error_details_2}")
                
        return None
