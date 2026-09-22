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
    """Instantly reshuffles, delays, adds external tracks, and renames streams without re-encoding."""
    base_cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    inputs = ["-i", input_file]
    input_paths = [input_file]
    maps_and_meta = []
    
    # 🟢 Wipe all existing global metadata to ensure a clean slate (Removes Group Watermarks)
    maps_and_meta.extend(["-map_metadata", "-1"])
    
    # 🟢 Re-inject only the metadata the user left in the UI boxes
    if global_tags:
        for k, v in global_tags.items():
            if v.strip(): # Only add if the text box wasn't emptied
                maps_and_meta.extend(["-metadata", f"{k}={v.strip()}"])
        
    out_idx = 0
    for track in stream_config:
        delay_ms = int(track.get("delay", 0))
        delay_sec = delay_ms / 1000.0

        # Handle External Track Injections
        if track.get("type") in ["ext_audio", "ext_sub"]:
            ext_file = track.get("local_path")
            if not ext_file or not os.path.exists(ext_file):
                continue
                
            if delay_ms != 0:
                inputs.extend(["-itsoffset", str(delay_sec), "-i", ext_file])
                src_id = len(input_paths)
                input_paths.append(ext_file)
            else:
                inputs.extend(["-i", ext_file])
                src_id = len(input_paths)
                input_paths.append(ext_file)
                
            stream_type = "a:0" if track["type"] == "ext_audio" else "s:0"
            maps_and_meta.extend(["-map", f"{src_id}:{stream_type}"])
            
            if track.get("title") and track.get("title").lower() != "skip":
                maps_and_meta.extend([f"-metadata:s:{out_idx}", f"title={track['title']}"])
            if track.get("lang"):
                maps_and_meta.extend([f"-metadata:s:{out_idx}", f"language={track['lang']}"])
                
            out_idx += 1
        
        # Handle Original File Tracks
        else:
            if delay_ms != 0:
                inputs.extend(["-itsoffset", str(delay_sec), "-i", input_file])
                src_id = len(input_paths)
                input_paths.append(input_file)
            else:
                src_id = 0
                
            idx = str(track.get('index', '0')).replace('v:', '').replace('a:', '').replace('s:', '')
            maps_and_meta.extend(["-map", f"{src_id}:{idx}"])
            
            if track.get("title") and track.get("title").lower() != "skip":
                maps_and_meta.extend([f"-metadata:s:{out_idx}", f"title={track['title']}"])
                
            out_idx += 1
            
    final_cmd = base_cmd + inputs + maps_and_meta + ["-c", "copy", output_file]
    proc = await asyncio.create_subprocess_exec(*final_cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    out, err = await proc.communicate()
    
    if proc.returncode != 0: 
        raise Exception(err.decode())
    return output_file
# ==============================================================================
