import asyncio
import os
from yt_dlp import YoutubeDL
import logging

logger = logging.getLogger("BotLogger")

def _extract_stream_sync(url: str, use_cookies: bool = True):
    ydl_opts = {
        "format": "best[ext=mp4]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "socket_timeout": 15,
        
        # 🟢 THE ULTIMATE YOUTUBE BYPASS: 
        # Forces yt-dlp to use curl_cffi to spoof a real Chrome TLS Fingerprint. 
        # This completely stops YouTube from dropping the SSL connection!
        "impersonate": "Chrome", 
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
    """Extracts stream URLs. Automatically falls back to cookie-less mode if YouTube drops the SSL connection."""
    try:
        # Attempt 1: With Cookies (For age-restricted content)
        return await asyncio.to_thread(_extract_stream_sync, url, True)
    except Exception as e:
        err_str = str(e).lower()
        logger.warning(f"yt-dlp stream resolution failed (Cookies Active): {e}")
        
        # Attempt 2: If the cookie is expired, retry instantly without it!
        if "ssl" in err_str or "eof" in err_str or "cookie" in err_str or "sign in" in err_str:
            try:
                logger.info("🔄 Retrying yt-dlp without cookies to bypass Auth/SSL drop...")
                return await asyncio.to_thread(_extract_stream_sync, url, False)
            except Exception as e2:
                logger.warning(f"yt-dlp stream resolution failed (No Cookies): {e2}")
                
        return None
