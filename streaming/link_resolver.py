import asyncio
import logging
from urllib.parse import urlparse

from streaming.direct_link_generator import direct_link_generator
from streaming.url_shortener_bypass import is_url_shortener, bypass_shortener
from streaming.yt_stream_resolver import resolve_yt_dlp_stream

logger = logging.getLogger("BotLogger")

KNOWN_STREAM_SITES = (
    "youtube.com", "youtu.be", "twitter.com", "x.com", 
    "tiktok.com", "reddit.com", "facebook.com", "fb.watch", 
    "twitch.tv", "vimeo.com", "dailymotion.com"
)

async def resolve_universal_link(url: str):
    if not url:
        return url, {}

    domain = urlparse(url).hostname or ""

    # 1. Unshorten ouo.io shortlinks first
    if is_url_shortener(domain):
        try:
            logger.info(f"🔗 Resolving shortlink for {domain}...")
            url = await asyncio.to_thread(bypass_shortener, url)
            domain = urlparse(url).hostname or ""
        except Exception as e:
            logger.warning(f"Shortener bypass failed: {e}")

    # 2. Extract media streams from web video portals
    if any(site in domain.lower() for site in KNOWN_STREAM_SITES):
        yt_res = await resolve_yt_dlp_stream(url)
        if yt_res and yt_res.get("stream_url"):
            return yt_res["stream_url"], yt_res.get("headers", {})

    # 3. Direct host link generators (Terabox, Mediafire, Gofile, etc.)
    try:
        result = await asyncio.to_thread(direct_link_generator, url)
        raw_url = url
        headers = {}

        if isinstance(result, str):
            raw_url = result
            
        elif isinstance(result, tuple):
            raw_url, headers_raw = result
            # 🟢 CRITICAL FIX: Flawless Tuple Header Unpacking!
            header_lines = headers_raw.splitlines() if isinstance(headers_raw, str) else headers_raw
            for h in header_lines:
                if ":" in h:
                    k, v = h.split(":", 1)
                    headers[k.strip()] = v.strip()
                    
        elif isinstance(result, dict):
            if "contents" in result and result["contents"]:
                best_file = max(result["contents"], key=lambda x: x.get("size", 0))
                raw_url = best_file["url"]
            if "header" in result:
                for line in result["header"].split("\n"):
                    if ":" in line:
                        k, v = line.split(":", 1)
                        headers[k.strip()] = v.strip()

        logger.info(f"✅ Resolved Direct Link: {raw_url[:70]}...")
        return raw_url, headers
        
    except Exception as exc:
        # Fallback to yt-dlp before returning the raw URL
        yt_res = await resolve_yt_dlp_stream(url)
        if yt_res and yt_res.get("stream_url"):
            return yt_res["stream_url"], yt_res.get("headers", {})
        return url, {}
