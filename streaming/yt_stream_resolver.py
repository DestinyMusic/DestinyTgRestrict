import asyncio
import json
import os
import logging

logger = logging.getLogger("BotLogger")

async def _extract_cli(url: str, use_cookies: bool = True):
    # 🟢 BULLETPROOF FIX: Run yt-dlp natively via CLI subprocess!
    # This completely bypasses all Python API thread crashes and AssertionError bugs.
    cmd = [
        "python", "-m", "yt_dlp",
        "--dump-json",
        "-f", "best[ext=mp4]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
        "--quiet",
        "--no-warnings",
        "--no-playlist",
        "--force-ipv4",
        "--impersonate", "chrome",  # Flawless Chrome TLS spoofing via CLI
        "--socket-timeout", "15",
        "--extractor-retries", "1"
    ]
    
    if use_cookies and os.path.exists("cookies.txt"):
        cmd.extend(["--cookies", "cookies.txt"])
        
    cmd.append(url)
    
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    
    if proc.returncode != 0:
        err_text = stderr.decode('utf-8', errors='ignore').strip()
        raise RuntimeError(f"CLI error: {err_text}")
        
    try:
        info = json.loads(stdout.decode('utf-8', errors='ignore'))
    except json.JSONDecodeError:
        raise ValueError(f"Failed to parse JSON. Stderr: {stderr.decode('utf-8', errors='ignore')}")

    stream_url = info.get("url")
    if not stream_url and "formats" in info:
        formats = [f for f in info.get("formats", []) if f.get("url")]
        if formats:
            stream_url = formats[-1]["url"]

    if not stream_url:
        raise ValueError("Direct streamable URL not found in yt-dlp output")

    return {
        "stream_url": stream_url,
        "headers": info.get("http_headers") or {},
        "title": info.get("title", "Direct Stream"),
        "duration": info.get("duration", 0)
    }

async def resolve_yt_dlp_stream(url: str):
    """Extracts stream URLs. Automatically falls back to cookie-less mode."""
    try:
        # Attempt 1: With Cookies
        return await _extract_cli(url, True)
    except Exception as e:
        logger.warning(f"yt-dlp resolution failed (Cookies Active): {str(e)[:200]}")
        
        # Attempt 2: Unconditional Fallback! 
        # If it fails for ANY reason (dead cookie, SSL drop), retry instantly without them!
        try:
            logger.info("🔄 Retrying yt-dlp without cookies to bypass Auth/TLS drop...")
            return await _extract_cli(url, False)
        except Exception as e2:
            logger.warning(f"yt-dlp resolution failed (No Cookies): {str(e2)[:200]}")
            
    return None
