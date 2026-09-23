import asyncio
import os
from yt_dlp import YoutubeDL
import logging
import traceback

logger = logging.getLogger("BotLogger")

def _extract_stream_sync(url: str, use_cookies: bool = True):
    ydl_opts = {
        "format": "best[ext=mp4]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        
        # 🟢 PROPER IPV4 & BROWSER IMPERSONATION FIXES
        "force_ipv4": True,               # Correct yt-dlp API argument to force IPv4
        "impersonate": "chrome",          # Uses curl_cffi to perfectly mimic Chrome TLS fingerprints
        "socket_timeout": 15,             # 15s is safer for curl_cffi handshakes
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
        # 🟢 FIX: Use repr(e) so OS-level socket errors don't evaluate to a blank string
        logger.warning(f"yt-dlp stream resolution failed (Cookies Active): {repr(e)}")
        
        # 🟢 Attempt 2: Unconditional Fallback! 
        # If it fails for ANY reason with cookies, try instantly without them!
        try:
            logger.info("🔄 Retrying yt-dlp without cookies to bypass Auth/TLS drop...")
            return await asyncio.to_thread(_extract_stream_sync, url, False)
        except Exception as e2:
            logger.warning(f"yt-dlp stream resolution failed (No Cookies): {repr(e2)}")
                
        return None
