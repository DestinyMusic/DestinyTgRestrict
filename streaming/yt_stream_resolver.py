import asyncio
import os
from yt_dlp import YoutubeDL
import logging

logger = logging.getLogger("BotLogger")

def _extract_stream_sync(url: str):
    ydl_opts = {
        "format": "best[ext=mp4]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
    }
    if os.path.exists("cookies.txt"):
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
    try:
        return await asyncio.to_thread(_extract_stream_sync, url)
    except Exception as e:
        logger.warning(f"yt-dlp stream resolution failed: {e}")
        return None
