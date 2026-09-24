# ==============================================================================
# --- NEW: GOFILE UPLOADER & FFMPEG REMUX ENGINE ---
# ==============================================================================
import aiohttp
import os

async def upload_to_gofile(file_path: str):
    """Uploads a file to GoFile.io and returns the public download link."""
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.gofile.io/servers") as resp:
            data = await resp.json()
            if data.get("status") != "ok": raise Exception("Failed to get GoFile server")
            server = data["data"]["servers"][0]["name"]
            
        upload_url = f"https://{server}.gofile.io/contents/uploadfile"
        with open(file_path, 'rb') as f:
            form = aiohttp.FormData()
            form.add_field('file', f, filename=os.path.basename(file_path))
            async with session.post(upload_url, data=form) as resp:
                upload_data = await resp.json()
                if upload_data.get("status") == "ok":
                    return upload_data["data"]["downloadPage"]
                raise Exception(f"GoFile Error: {upload_data}")

async def process_remux(input_file, output_file, stream_config, global_tags=None):
    """Instantly reshuffles, delays, adds external tracks, and renames streams using MKVToolNix."""
    
    # Initialize mkvmerge command
    cmd = ["mkvmerge", "-o", output_file]
    
    # 🟢 Global Metadata (Movie Title)
    if global_tags and global_tags.get("title"):
        cmd.extend(["--title", global_tags["title"].strip()])

    main_tracks = []
    main_args = []
    ext_args = []

    for track in stream_config:
        delay_ms = int(track.get("delay", 0))
        
        # 🟢 Handle External Track Injections
        if track.get("type") in ["ext_audio", "ext_sub"]:
            ext_file = track.get("local_path")
            if not ext_file or not os.path.exists(ext_file):
                continue
            
            # External files typically hold their target stream at index 0
            if delay_ms != 0:
                ext_args.extend(["--sync", f"0:{delay_ms}"])
                
            if track.get("title") and track.get("title").lower() != "skip":
                ext_args.extend(["--track-name", f"0:{track['title']}"])
                
            if track.get("lang"):
                ext_args.extend(["--language", f"0:{track['lang']}"])
                
            ext_args.append(ext_file)
            
        # 🟢 Handle Original File Tracks
        else:
            idx = str(track.get('index', '0')).replace('v:', '').replace('a:', '').replace('s:', '')
            main_tracks.append(idx)
            
            if delay_ms != 0:
                main_args.extend(["--sync", f"{idx}:{delay_ms}"])
                
            if track.get("title") and track.get("title").lower() != "skip":
                main_args.extend(["--track-name", f"{idx}:{track['title']}"])
                
            if track.get("lang"):
                main_args.extend(["--language", f"{idx}:{track['lang']}"])

    # Build the final command structure
    if main_tracks:
        cmd.extend(["--tracks", ",".join(main_tracks)])
        cmd.extend(main_args)
        cmd.append(input_file)
    else:
        # Failsafe if the user unchecked all original video/audio tracks
        cmd.extend(["--no-video", "--no-audio", "--no-subtitles", input_file]) 

    # Append external tracks to the end of the command
    cmd.extend(ext_args)
    
    # Execute MKVToolNix
    proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    out, err = await proc.communicate()
    
    if proc.returncode != 0:
        err_str = err.decode('utf-8', errors='ignore')
        raise Exception(f"MKVMerge Error: {err_str}")
        
    return output_file

# ==============================================================================
