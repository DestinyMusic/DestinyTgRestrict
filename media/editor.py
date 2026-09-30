# ==============================================================================
# --- NEW: GOFILE UPLOADER & FFMPEG REMUX ENGINE ---
# ==============================================================================
import aiohttp
import os
import re
import xml.etree.ElementTree as ET

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


def _build_global_tags_xml(global_tags):
    root = ET.Element("Tags")
    tag = ET.SubElement(root, "Tag")
    ET.SubElement(tag, "Targets")
    
    has_valid_tags = False
    for key, value in global_tags.items():
        tag_name = str(key).strip().upper()
        if not re.fullmatch(r"[A-Z0-9_.-]{1,128}", tag_name):
            continue
        tag_value = clean_media_text(value)
        if not tag_value:
            continue
            
        simple = ET.SubElement(tag, "Simple")
        ET.SubElement(simple, "Name").text = tag_name
        ET.SubElement(simple, "String").text = tag_value
        has_valid_tags = True
        
    # 🟢 FIX: If all tags were erased/empty, return None so MKVToolNix ignores it
    if not has_valid_tags:
        return None
        
    return ET.tostring(root, encoding="unicode")


async def process_remux(input_file, output_file, stream_config, global_tags=None):
    """Instantly reshuffles, delays, adds external tracks, and renames streams using MKVToolNix."""
    
    # Initialize mkvmerge command
    cmd = ["mkvmerge", "-o", output_file]
    
    # 🟢 Global Metadata (Movie Title)
    if global_tags and global_tags.get("title"):
        cmd.extend(["--title", clean_media_text(global_tags["title"])])

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
                
            track_title = clean_media_text(track.get("title", ""))
            if track_title and track_title.lower() != "skip":
                ext_args.extend(["--track-name", f"0:{track_title}"])
                
            if track.get("lang"):
                ext_args.extend(["--language", f"0:{track['lang']}"])
                
            ext_args.append(ext_file)
            
        # 🟢 Handle Original File Tracks
        else:
            idx = str(track.get('index', '0')).replace('v:', '').replace('a:', '').replace('s:', '')
            
            if delay_ms != 0:
                main_args.extend(["--sync", f"{idx}:{delay_ms}"])
                
            track_title = clean_media_text(track.get("title", ""))
            if track_title and track_title.lower() != "skip":
                main_args.extend(["--track-name", f"{idx}:{track_title}"])
                
            if track.get("lang"):
                main_args.extend(["--language", f"{idx}:{track['lang']}"])

    # Build the final command structure
    cmd.extend(main_args)
    cmd.append(input_file)
    cmd.extend(ext_args)
    
    # Execute MKVToolNix
    proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    out, err = await proc.communicate()
    
    if proc.returncode != 0:
        # MKVMerge prints its errors to stdout instead of stderr, so we combine them!
        err_str = err.decode('utf-8', errors='ignore').strip()
        out_str = out.decode('utf-8', errors='ignore').strip()
        full_error = f"{err_str}\n{out_str}".strip()
        raise Exception(f"MKVMerge Error:\n{full_error}")

    # --- GLOBAL TAGS (XML METHOD) ---
    if global_tags is not None:
        xml_data = _build_global_tags_xml(global_tags)
        
        # 🟢 FIX: Only run the XML tagger if valid XML data was actually generated
        if xml_data:
            tags_path = f"{output_file}.tags.xml"
            try:
                root = ET.fromstring(xml_data)
                ET.ElementTree(root).write(tags_path, encoding="utf-8", xml_declaration=True)
                proc = await asyncio.create_subprocess_exec(
                    "mkvpropedit", output_file, "--tags", f"global:{tags_path}",
                    stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
                )
                out, err = await proc.communicate()
                if proc.returncode != 0:
                    error = err.decode('utf-8', 'ignore').strip()
                    raise Exception(error)
            except Exception as e:
                raise Exception(f"MKV metadata update failed: {e}")
        finally:
            if os.path.exists(tags_path):
                os.remove(tags_path)
        
    return output_file

# ==============================================================================
