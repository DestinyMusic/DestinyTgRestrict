# ==============================================================================
# --- 2. MESSAGE FETCHER & VALIDATOR ---
# ==============================================================================
import os 
from pyrogram.errors import FloodWait

def _set_task_result_reason(user_id, task_uuid, reason):
    task_info = ACTIVE_PROCESSES.get(user_id, {}).get(task_uuid)
    if task_info is not None:
        task_info["last_result_reason"] = reason


async def _fetch_and_validate_msg(client, acc, chatid, msgid, user_id, filter_thread_id, allowed_types, task_uuid, pre_fetched_msg=None):
    fetcher = acc if acc else client
    
    # Assign default UI labels early to prevent "Unknown"
    if task_uuid and user_id in ACTIVE_PROCESSES and task_uuid in ACTIVE_PROCESSES[user_id]:
        if "fetcher" not in ACTIVE_PROCESSES[user_id][task_uuid]:
            ACTIVE_PROCESSES[user_id][task_uuid]["fetcher"] = _get_client_label(fetcher)
        if "uploader" not in ACTIVE_PROCESSES[user_id][task_uuid]:
            ACTIVE_PROCESSES[user_id][task_uuid]["uploader"] = "🤖 Pending..."

    # Use the chunked message if available, otherwise fetch it manually
    msg = pre_fetched_msg
    if not msg:
        try:
            msg = await fetcher.get_messages(chatid, msgid)
        except FloodWait as e:
            raise e # Pass rate limits back up to the batch engine
        except Exception as exc:
            _set_task_result_reason(user_id, task_uuid, f"source message fetch failed: {type(exc).__name__}: {exc}")
            return None, None

    if not msg or msg.empty:
        _set_task_result_reason(user_id, task_uuid, "source message missing or inaccessible")
        return None, None

    if filter_thread_id is not None:
        # 🟢 FIX: Bot DMs and Chat DMs do not have topics. 
        # Ignore thread filters for DMs so live watchers detect them!
        chat_type = str(getattr(getattr(msg, "chat", None), "type", ""))
        is_private_dm = "PRIVATE" in chat_type or "BOT" in chat_type or (isinstance(chatid, int) and chatid > 0)
        
        if not is_private_dm:
            actual_thread = getattr(msg, "message_thread_id", None)
            if actual_thread is None:
                # 🟢 FIX: If targeting General Topic (1), a missing thread ID is a valid match!
                if filter_thread_id != 1 and getattr(msg, "reply_to_top_message_id", None) != filter_thread_id and getattr(msg, "reply_to_message_id", None) != filter_thread_id and msg.id != filter_thread_id:
                    _set_task_result_reason(user_id, task_uuid, f"topic filter mismatch: expected {filter_thread_id}, no topic ID found")
                    return None, None
            elif actual_thread != filter_thread_id:
                _set_task_result_reason(user_id, task_uuid, f"topic filter mismatch: expected {filter_thread_id}, got {actual_thread}")
                return None, None

    msg_type = get_message_type(msg)
    if not msg_type:
        _set_task_result_reason(user_id, task_uuid, "unsupported or non-media message type")
        return None, None
    if allowed_types is not None and msg_type not in allowed_types:
        _set_task_result_reason(user_id, task_uuid, f"media type excluded by task filter: {msg_type}")
        return None, None

    task_info = ACTIVE_PROCESSES.get(user_id, {}).get(task_uuid, {})
    if not filename_matches_filters(
        msg,
        task_info.get("include_keywords"),
        task_info.get("exclude_keywords"),
    ):
        _set_task_result_reason(user_id, task_uuid, "filename rejected by include/exclude keyword filters")
        return None, None
    
    # 🟢 FIX: Shield Watchers from Global Cancels
    is_w_task = False
    if user_id in ACTIVE_PROCESSES and task_uuid in ACTIVE_PROCESSES[user_id]:
        is_w_task = ACTIVE_PROCESSES[user_id][task_uuid].get("is_watcher", False)
        
    if (batch_temp.IS_BATCH.get(user_id) and not is_w_task) or (task_uuid and CANCEL_FLAGS.get(task_uuid)):
        _set_task_result_reason(user_id, task_uuid, "task cancelled")
        return None, None

    return msg, msg_type

# ==============================================================================
# --- 3. THE ROUTER (Replaces handle_private) ---
# ==============================================================================

async def handle_private(client: Client, acc, message: Message, chatid, msgid: int, index: int, total_count: int, status_message: Message, dest_chat_id, dest_thread_id, delay, user_id, task_uuid=None, is_restricted=False, header_text="", filter_thread_id=None, allowed_types=None, pre_fetched_msg=None):
    fetcher = acc if acc else client

    # 1. Determine link type
    is_public = isinstance(chatid, str) and not chatid.lstrip('-').isdigit()
    is_live_watch = (delay == 0 and status_message and "Watcher" in getattr(status_message, "text", ""))

    # 2. Pre-fetch and validate message natively
    msg, msg_type = await _fetch_and_validate_msg(client, acc, chatid, msgid, user_id, filter_thread_id, allowed_types, task_uuid, pre_fetched_msg)
    if not msg:
        return "SKIPPED" 

    kwargs = {
        "msg": msg, "msg_type": msg_type, "index": index, "total_count": total_count, 
        "status_message": status_message, "dest_chat_id": dest_chat_id, "dest_thread_id": dest_thread_id,
        "delay": delay, "user_id": user_id, "task_uuid": task_uuid, "header_text": header_text
    }

    # 3. Route the task
    is_content_protected = is_restricted or getattr(msg, "has_protected_content", False) or getattr(msg.chat, "has_protected_content", False)
    task_info = ACTIVE_PROCESSES.get(user_id, {}).get(task_uuid, {})
    if (task_info.get("thumb_file_id") or task_info.get("thumb_b64")) and msg_type != "Text":
        return await _execute_restricted_download_upload(client, acc, chatid, msgid, **kwargs)
    
    if not is_content_protected:
        if is_live_watch:
            return await handle_unrestricted_live(client, acc, chatid, msgid, **kwargs)
        elif is_public:
            return await handle_unrestricted_public(client, acc, chatid, msgid, **kwargs)
        else:
            return await handle_unrestricted_private(client, acc, chatid, msgid, **kwargs)
    else:
        if is_live_watch:
            return await handle_restricted_live(client, acc, chatid, msgid, **kwargs)
        elif is_public:
            return await handle_restricted_public(client, acc, chatid, msgid, **kwargs)
        else:
            return await handle_restricted_private(client, acc, chatid, msgid, **kwargs)

# ==============================================================================
# --- 🟢 UNRESTRICTED ROUTES (WITH ALBUM SUPPORT) ---
# ==============================================================================

def _get_client_label(c):
    if not c: return "Unknown"
    name = getattr(c, "name", "")
    if name.startswith("worker_bot_"):
        return f"🤖 Worker {name.split('_')[-1]}"
    elif name.startswith("User_") or name.startswith("temp_acc_"):
        try:
            fn = c.me.first_name if getattr(c, "me", None) else "User Session"
            return f"👤 {fn}"
        except:
            return "👤 User Session"
    elif name == "RestrictedBot":
        return "🤖 Main Bot"
    return f"🤖 {name}"

def get_dynamic_upload_client(client, acc, user_id, task_uuid, msg_index):
    """Dynamically slices worker bots across multiple concurrent tasks to prevent FloodWaits."""
    worker_bots = USER_TASK_BOTS.get(user_id, [])
    connected = [wb for wb in worker_bots if getattr(wb, "is_connected", False)]
    
    if not connected:
        return client
        
    # 1. Count active batch tasks (Ignore Watchers)
    user_tasks = [
        tid for tid, info in ACTIVE_PROCESSES.get(user_id, {}).items() 
        if not info.get("is_watcher", False)
    ]
    
    if not user_tasks or task_uuid not in user_tasks:
        return connected[msg_index % len(connected)]
        
    total_tasks = len(user_tasks)
    my_rank = user_tasks.index(task_uuid)
    total_bots = len(connected)
    
    # 2. Slice logic
    if total_tasks == 1:
        return connected[msg_index % total_bots] # Use all bots for 1 task
        
    bots_per_task = max(1, total_bots // total_tasks)
    start_idx = my_rank * bots_per_task
    
    # 3. Overflow logic (if more tasks than bots, overflow uses User Session or Main Bot)
    if start_idx >= total_bots:
        return acc if acc else client
        
    # 4. Grab dedicated slice for this specific task
    my_slice = connected[start_idx : start_idx + bots_per_task]
    if not my_slice:
        return acc if acc else client
        
    return my_slice[msg_index % len(my_slice)]

async def _execute_unrestricted_copy(client, acc, chat_id, msgid, dest_chat_id, dest_thread_id, msg, msg_type, user_id, task_uuid, delay, index=1):
    # 🟢 FIX: Force User Session for Bot DMs and Chat DMs because Worker Bots can't access them!
    is_source_dm = isinstance(chat_id, int) and chat_id > 0
    is_dest_dm = isinstance(dest_chat_id, int) and dest_chat_id > 0
    
    if (is_source_dm or is_dest_dm) and acc:
        upload_client = acc
    else:
        upload_client = get_dynamic_upload_client(client, acc, user_id, task_uuid, index)
            
    if task_uuid and user_id in ACTIVE_PROCESSES and task_uuid in ACTIVE_PROCESSES[user_id]:
        ACTIVE_PROCESSES[user_id][task_uuid]["fetcher"] = _get_client_label(acc if acc else client)
        ACTIVE_PROCESSES[user_id][task_uuid]["uploader"] = _get_client_label(upload_client)

    if msg_type == "Text":
        try:
            await safe_send(upload_client, user_id, dest_chat_id, task_uuid, True, upload_client.send_message, chat_id=dest_chat_id, text=msg.text, entities=msg.entities, message_thread_id=dest_thread_id)
            return True
        except Exception:
            if acc:
                try:
                    await safe_send(acc, user_id, dest_chat_id, task_uuid, False, acc.send_message, chat_id=dest_chat_id, text=msg.text, entities=msg.entities, message_thread_id=dest_thread_id)
                    return True
                except: return False
            return False
            
    try:
        await USER_FLOOD_LOCKS[user_id].wait_if_locked()
        
        if msg.media_group_id:
            fetcher = acc if acc else upload_client
            try:
                m_group = await fetcher.get_media_group(chat_id, msgid)
                group_size = len(m_group)
                if task_uuid:
                    for m in m_group: batch_temp.SKIP_IDS[task_uuid].add(m.id)
            except: group_size = 1

            try:
                copy_res = await safe_send(upload_client, user_id, dest_chat_id, task_uuid, True, upload_client.copy_media_group, chat_id=dest_chat_id, from_chat_id=chat_id, message_id=msgid, message_thread_id=dest_thread_id)
            except Exception:
                if acc:
                    copy_res = await safe_send(acc, user_id, dest_chat_id, task_uuid, False, acc.copy_media_group, chat_id=dest_chat_id, from_chat_id=chat_id, message_id=msgid, message_thread_id=dest_thread_id)
                else: copy_res = False
            
            if copy_res:
                if delay > 0 and group_size > 1: await asyncio.sleep(delay * (group_size - 1))
                return True
            return False

        try:
            task_info = ACTIVE_PROCESSES.get(user_id, {}).get(task_uuid, {})
            cleanup_tags = task_info.get("cleanup_keywords", [])
            copy_kwargs = {
                "chat_id": dest_chat_id,
                "from_chat_id": chat_id,
                "message_id": msgid,
                "message_thread_id": dest_thread_id
            }
            if msg.caption:
                clean_cap, clean_ent = clean_caption(msg.caption, msg.caption_entities, custom_tags=cleanup_tags)
                copy_kwargs["caption"] = clean_cap
                if clean_ent:
                    copy_kwargs["caption_entities"] = clean_ent

            await safe_send(upload_client, user_id, dest_chat_id, task_uuid, True, upload_client.copy_message, **copy_kwargs)
            return True
        except Exception:
            if acc:
                # 🟢 UPDATE UI: Show User Session taking over!
                if task_uuid and user_id in ACTIVE_PROCESSES and task_uuid in ACTIVE_PROCESSES[user_id]:
                    ACTIVE_PROCESSES[user_id][task_uuid]["uploader"] = _get_client_label(acc)
                    
                owner_copy = await safe_send(acc, user_id, dest_chat_id, task_uuid, False, acc.copy_message, chat_id=dest_chat_id, from_chat_id=chat_id, message_id=msgid, message_thread_id=dest_thread_id)
                return bool(owner_copy)
            return False
    except FloodWait as e:
        USER_FLOOD_LOCKS[user_id].set_lock(e.value + 5)
        await asyncio.sleep(e.value + 5)
        if acc:
            try:
                await safe_send(acc, user_id, dest_chat_id, task_uuid, False, acc.copy_message, chat_id=dest_chat_id, from_chat_id=chat_id, message_id=msgid, message_thread_id=dest_thread_id)
                return True
            except: return False
        return False
    except Exception: return False

async def _execute_public_live_unrestricted_copy(client, acc, chat_id, msgid, dest_chat_id, dest_thread_id, msg, msg_type, user_id, task_uuid, delay, index=1):
    # 🟢 FIX: Force User Session for Bot DMs and Chat DMs
    is_source_dm = isinstance(chat_id, int) and chat_id > 0
    is_dest_dm = isinstance(dest_chat_id, int) and dest_chat_id > 0
    
    if (is_source_dm or is_dest_dm) and acc:
        upload_client = acc
    else:
        upload_client = get_dynamic_upload_client(client, acc, user_id, task_uuid, index)

    if task_uuid and user_id in ACTIVE_PROCESSES and task_uuid in ACTIVE_PROCESSES[user_id]:
        ACTIVE_PROCESSES[user_id][task_uuid]["fetcher"] = _get_client_label(acc if acc else client)
        ACTIVE_PROCESSES[user_id][task_uuid]["uploader"] = _get_client_label(upload_client)

    if msg_type == "Text":
        try:
            await safe_send(upload_client, user_id, dest_chat_id, task_uuid, True, upload_client.send_message, chat_id=dest_chat_id, text=msg.text, entities=msg.entities, message_thread_id=dest_thread_id)
            return True
        except Exception:
            if acc:
                try:
                    await safe_send(acc, user_id, dest_chat_id, task_uuid, False, acc.send_message, chat_id=dest_chat_id, text=msg.text, entities=msg.entities, message_thread_id=dest_thread_id)
                    return True
                except: return False
            return False
            
    try:
        await USER_FLOOD_LOCKS[user_id].wait_if_locked()
        
        if msg.media_group_id:
            try: m_group = await upload_client.get_media_group(chat_id, msgid)
            except:
                if acc:
                    try: m_group = await acc.get_media_group(chat_id, msgid)
                    except: m_group = [msg]
                else: m_group = [msg]
            group_size = len(m_group)
            
            if task_uuid:
                for m in m_group: batch_temp.SKIP_IDS[task_uuid].add(m.id)

            try:
                copy_res = await safe_send(upload_client, user_id, dest_chat_id, task_uuid, True, upload_client.copy_media_group, chat_id=dest_chat_id, from_chat_id=chat_id, message_id=msgid, message_thread_id=dest_thread_id)
                if not copy_res: raise ValueError("Bot copy None")
            except Exception:
                if acc:
                    copy_res = await safe_send(acc, user_id, dest_chat_id, task_uuid, False, acc.copy_media_group, chat_id=dest_chat_id, from_chat_id=chat_id, message_id=msgid, message_thread_id=dest_thread_id)
                else: copy_res = False
            
            if copy_res:
                if delay > 0 and group_size > 1: await asyncio.sleep(delay * (group_size - 1))
                return True
            return False

        try:
            copy_res = await safe_send(upload_client, user_id, dest_chat_id, task_uuid, True, upload_client.copy_message, chat_id=dest_chat_id, from_chat_id=chat_id, message_id=msgid, message_thread_id=dest_thread_id)
            if not copy_res: raise ValueError("Bot copy returned None")
            return True
        except Exception:
            if acc:
                # 🟢 UPDATE UI: Show User Session taking over!
                if task_uuid and user_id in ACTIVE_PROCESSES and task_uuid in ACTIVE_PROCESSES[user_id]:
                    ACTIVE_PROCESSES[user_id][task_uuid]["uploader"] = _get_client_label(acc)
                    
                owner_copy = await safe_send(acc, user_id, dest_chat_id, task_uuid, False, acc.copy_message, chat_id=dest_chat_id, from_chat_id=chat_id, message_id=msgid, message_thread_id=dest_thread_id)
                return bool(owner_copy)
            return False
    except FloodWait as e:
        USER_FLOOD_LOCKS[user_id].set_lock(e.value + 5)
        await asyncio.sleep(e.value + 5)
        if acc:
            try:
                owner_copy = await safe_send(acc, user_id, dest_chat_id, task_uuid, False, acc.copy_message, chat_id=dest_chat_id, from_chat_id=chat_id, message_id=msgid, message_thread_id=dest_thread_id)
                return bool(owner_copy)
            except: return False
        return False
    except Exception: return False

# 1 Public Link
async def handle_unrestricted_public(client, acc, chat_id, msgid, dest_chat_id, dest_thread_id, msg, msg_type, **kwargs):
    return await _execute_public_live_unrestricted_copy(client, acc, chat_id, msgid, dest_chat_id, dest_thread_id, msg, msg_type, kwargs.get("user_id"), kwargs.get("task_uuid"), kwargs.get("delay", 3), kwargs.get("index", 1))

# 2 Pvt link
async def handle_unrestricted_private(client, acc, chat_id, msgid, dest_chat_id, dest_thread_id, msg, msg_type, **kwargs):
    return await _execute_unrestricted_copy(client, acc, chat_id, msgid, dest_chat_id, dest_thread_id, msg, msg_type, kwargs.get("user_id"), kwargs.get("task_uuid"), kwargs.get("delay", 3), kwargs.get("index", 1))

# 3 Live watch
async def handle_unrestricted_live(client, acc, chat_id, msgid, dest_chat_id, dest_thread_id, msg, msg_type, **kwargs):
    return await _execute_public_live_unrestricted_copy(client, acc, chat_id, msgid, dest_chat_id, dest_thread_id, msg, msg_type, kwargs.get("user_id"), kwargs.get("task_uuid"), kwargs.get("delay", 3), kwargs.get("index", 1))

# ==============================================================================
# --- 🔴 RESTRICTED ROUTES ---
# ==============================================================================

# 1 Public Link
async def handle_restricted_public(client, acc, chat_id, msgid, **kwargs):
    return await _execute_restricted_download_upload(client, acc, chat_id, msgid, **kwargs)

# 2 Pvt link
async def handle_restricted_private(client, acc, chat_id, msgid, **kwargs):
    return await _execute_restricted_download_upload(client, acc, chat_id, msgid, **kwargs)

# 3 Live watch
async def handle_restricted_live(client, acc, chat_id, msgid, **kwargs):
    return await _execute_restricted_download_upload(client, acc, chat_id, msgid, **kwargs)

async def build_rich_caption(file_path, msg_type, msg, override_name=None, override_size=None):
    try:
        import math, re
        file_name = override_name
        if not file_name:
            file_name = "Unknown"
            if msg_type == "Audio" and getattr(msg, "audio", None): file_name = getattr(msg.audio, "file_name", "Audio.m4a")
            elif msg_type == "Video" and getattr(msg, "video", None): file_name = getattr(msg.video, "file_name", "Video.mp4")
            elif getattr(msg, "document", None): file_name = getattr(msg.document, "file_name", "File.dat")
        file_name = clean_media_text(file_name)
        
        if not file_path or not os.path.exists(file_path):
            return None
            
        size_bytes = override_size if override_size is not None else os.path.getsize(file_path)
        size_str = _pretty_bytes(size_bytes)
        
        meta_str = ""
        
        if msg_type == "Audio":
            bitrate_str = "Unknown Quality"
            try:
                cmd = ["mediainfo", "--Inform=Audio;%Format%|%BitDepth%|%BitRate/String%|%SamplingRate/String%", str(file_path)]
                proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
                stdout, _ = await proc.communicate()
                out = stdout.decode('utf-8', errors='ignore').strip().split('\n')[0] 
                if out:
                    parts = out.split('|')
                    if len(parts) >= 4:
                        fmt = parts[0].strip()
                        depth = parts[1].strip()
                        bitrate = parts[2].strip().replace(" ", "")
                        sample_rate = parts[3].strip().replace(" ", "")
                        
                        if "MPEG Audio" in fmt: fmt = "MP3"
                        elif "AAC" in fmt: fmt = "AAC"
                        elif "FLAC" in fmt: fmt = "FLAC"
                        elif "ALAC" in fmt: fmt = "ALAC"
                        elif "Wave" in fmt: fmt = "WAV"
                        elif "Opus" in fmt: fmt = "OPUS"
                        elif "Vorbis" in fmt: fmt = "OGG"
                        
                        if depth: bitrate_str = f"{fmt} • {depth}Bit - {sample_rate}"
                        elif bitrate: bitrate_str = f"{fmt} • {bitrate} - {sample_rate}"
                        else: bitrate_str = f"{fmt} • {sample_rate}"
            except: pass
            meta_str = f"\n🎧 <code>{bitrate_str}</code>"
            
        elif msg_type == "Video":
            w = getattr(msg.video, "width", 0) if getattr(msg, "video", None) else 0
            h = getattr(msg.video, "height", 0) if getattr(msg, "video", None) else 0
            dur = getattr(msg.video, "duration", 0) if getattr(msg, "video", None) else 0
            
            if dur:
                d = math.floor(dur / 86400)
                hr = math.floor((dur % 86400) / 3600)
                m = math.floor((dur % 3600) / 60)
                s = math.floor(dur % 60)
                
                if d > 0: dur_str = f"{d}d {hr}h {m}m {s}s"
                elif hr > 0: dur_str = f"{hr}h {m}m {s}s"
                elif m > 0: dur_str = f"{m}m {s}s"
                else: dur_str = f"{s}s"
            else:
                dur_str = "Unknown"
            
            audio_lng = "Unknown"
            sub_lng = "None"
            try:
                cmd = ["mediainfo", "--Inform=General;%Audio_Language_List%|%Text_Language_List%", str(file_path)]
                proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
                stdout, _ = await proc.communicate()
                out = stdout.decode().strip().split('|')
                if len(out) == 2:
                    a_list, s_list = out[0].strip(), out[1].strip()
                    if a_list: audio_lng = a_list.replace(" / ", ", ")
                    if s_list: sub_lng = s_list.replace(" / ", ", ")
                elif len(out) == 1 and out[0].strip():
                    audio_lng = out[0].strip().replace(" / ", ", ")
            except: pass
            
            meta_str = f" 💎 <code>{w}x{h}</code>\n⏳ <code>{dur_str}</code> 💬 <code>{sub_lng}</code>\n🔊 <code>{audio_lng}</code>"
            
        return f"<b>{html.escape(file_name)}</b>\n\n🗂 <code>{size_str}</code>{meta_str}"
    except Exception as e:
        logger.debug(f"Rich caption generation failed: {e}")
    return None


async def _prepare_task_thumbnail(client, task_folder_path, user_id, task_uuid):
    task_info = ACTIVE_PROCESSES.get(user_id, {}).get(task_uuid, {})
    file_id = task_info.get("thumb_file_id")
    thumb_b64 = task_info.get("thumb_b64")
    if not file_id and not thumb_b64:
        return None

    thumb_path = task_folder_path / "task_thumbnail.jpg"
    if thumb_path.exists():
        return str(thumb_path)

    source_path = task_folder_path / "task_thumbnail_source"
    try:
        if file_id:
            downloaded = await client.download_media(file_id, file_name=str(source_path))
        else:
            import base64
            encoded = thumb_b64.split(",", 1)[-1]
            source_path.write_bytes(base64.b64decode(encoded, validate=True))
            downloaded = str(source_path)
        if not downloaded:
            return None
        from PIL import Image
        with Image.open(downloaded) as image:
            image = image.convert("RGB")
            for dimensions in ((320, 320), (256, 256), (160, 160)):
                image.thumbnail(dimensions)
                for quality in (80, 65, 50):
                    image.save(thumb_path, format="JPEG", quality=quality, optimize=True)
                    if thumb_path.stat().st_size <= 200_000:
                        break
                if thumb_path.stat().st_size <= 200_000:
                    break
        if thumb_path.stat().st_size > 200_000:
            thumb_path.unlink(missing_ok=True)
            return None
        os.remove(downloaded)
        return str(thumb_path)
    except Exception as exc:
        logger.warning(f"Custom task thumbnail could not be prepared: {exc}")
        return None

# ==============================================================================
# --- CORE RESTRICTED DOWNLOAD / UPLOAD ENGINE ---
# ==============================================================================

async def process_internal_metadata(file_path, cleanup_tags):
    """
    Scans MKV/MP4 files and strips specified tags from internal streams (audio, subs, etc).
    Uses ultra-fast MKVPropEdit for MKVs with a reliable FFmpeg fallback.
    """
    import os, json
    from pathlib import Path
    
    if not cleanup_tags or not file_path or not os.path.exists(file_path):
        return
        
    ext = str(file_path).lower()
    if not ext.endswith(('.mkv', '.mp4', '.m4a', '.mp3', '.flac', '.webm')):
        return

    try:
        # 1. Probe the file for existing tags
        cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", str(file_path)]
        proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        stdout, _ = await proc.communicate()
        if not stdout: return
        
        info = json.loads(stdout)
        from bot.utils import clean_media_text

        needs_change = False
        
        # --- PREPARE COMMANDS FOR BOTH ENGINES ---
        ffmpeg_args = ["ffmpeg", "-y", "-i", str(file_path), "-map", "0", "-c", "copy", "-map_metadata", "0"]
        mkvprop_args = ["mkvpropedit", str(file_path)]

        mkv_global_edits = []
        mkv_track_edits = {} 

        # 2. Clean Global File Tags
        format_tags = info.get("format", {}).get("tags", {})
        for k, v in format_tags.items():
            if k.lower() in ["title", "album", "artist"]:
                cleaned_val = clean_media_text(v, custom_tags=cleanup_tags)
                if cleaned_val != v:
                    needs_change = True
                    ffmpeg_args.extend(["-metadata", f"{k}={cleaned_val}"])
                    if k.lower() == "title":
                        if cleaned_val:
                            mkv_global_edits.extend(["--set", f"title={cleaned_val}"])
                        else:
                            mkv_global_edits.extend(["--delete", "title"])

        # 3. Clean Individual Track Tags (Audio, Video, Subtitles)
        v_idx, a_idx, s_idx = 1, 1, 1
        for s in info.get("streams", []):
            idx = s.get("index")
            codec_type = s.get("codec_type")

            # Create absolute MKV Track IDs (v1, a1, s1)
            if codec_type == "video":
                mkv_tid = f"v{v_idx}"
                v_idx += 1
            elif codec_type == "audio":
                mkv_tid = f"a{a_idx}"
                a_idx += 1
            elif codec_type == "subtitle":
                mkv_tid = f"s{s_idx}"
                s_idx += 1
            else:
                mkv_tid = None

            stream_tags = s.get("tags", {})
            name_processed = False
            lang_processed = False
            
            for k, v in stream_tags.items():
                k_lower = k.lower()
                if k_lower in ["title", "handler_name", "language"]:
                    
                    # Prevent duplicate track name edits for MKVPropEdit
                    if k_lower in ["title", "handler_name"]:
                        if name_processed: continue
                        name_processed = True
                        
                    if k_lower == "language":
                        if lang_processed: continue
                        lang_processed = True

                    cleaned_val = clean_media_text(v, custom_tags=cleanup_tags)
                    if cleaned_val != v:
                        needs_change = True
                        ffmpeg_args.extend([f"-metadata:s:{idx}", f"{k}={cleaned_val}"])
                        
                        if mkv_tid:
                            if mkv_tid not in mkv_track_edits:
                                mkv_track_edits[mkv_tid] = []
                                
                            if k_lower in ["title", "handler_name"]:
                                if cleaned_val:
                                    mkv_track_edits[mkv_tid].extend(["--set", f"name={cleaned_val}"])
                                else:
                                    mkv_track_edits[mkv_tid].extend(["--delete", "name"])
                            elif k_lower == "language":
                                if cleaned_val:
                                    mkv_track_edits[mkv_tid].extend(["--set", f"language={cleaned_val}"])
                                else:
                                    mkv_track_edits[mkv_tid].extend(["--delete", "language"])

        if not needs_change:
            return

        # Assemble final MKVPropEdit Command cleanly
        if mkv_global_edits:
            mkvprop_args.extend(["--edit", "info"])
            mkvprop_args.extend(mkv_global_edits)
            
        for tid, edits in mkv_track_edits.items():
            mkvprop_args.extend(["--edit", f"track:{tid}"])
            mkvprop_args.extend(edits)

        # 4. EXECUTION WITH FALLBACK ENGINE
        is_mkv = ext.endswith(('.mkv', '.webm'))
        mkvprop_success = False

        if is_mkv:
            try:
                proc_mkv = await asyncio.create_subprocess_exec(*mkvprop_args, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL)
                await proc_mkv.communicate()
                if proc_mkv.returncode == 0:
                    mkvprop_success = True
            except Exception:
                pass

        if not mkvprop_success:
            temp_out = str(file_path) + ".tmp" + Path(file_path).suffix
            ffmpeg_args.append(str(temp_out))
            
            proc_ff = await asyncio.create_subprocess_exec(*ffmpeg_args, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL)
            await proc_ff.communicate()
            
            if proc_ff.returncode == 0 and os.path.exists(temp_out):
                os.replace(temp_out, str(file_path))
            else:
                if os.path.exists(temp_out):
                    os.remove(temp_out)

    except Exception as e:
        pass # Silently proceed so the upload doesn't crash if metadata engines fail

async def _execute_restricted_download_upload(client, acc, chatid, msgid, dest_chat_id, dest_thread_id, msg, msg_type, index, total_count, status_message, delay, user_id, task_uuid, header_text):
    
    if msg_type == "Text":
        try:
            await safe_send(client, user_id, dest_chat_id, task_uuid, True, client.send_message, chat_id=dest_chat_id, text=msg.text, entities=msg.entities, message_thread_id=dest_thread_id)
            return True
        except Exception:
            if acc:
                try:
                    await safe_send(acc, user_id, dest_chat_id, task_uuid, False, acc.send_message, chat_id=dest_chat_id, text=msg.text, entities=msg.entities, message_thread_id=dest_thread_id)
                    return True
                except: return False
            return False

    folder_name = task_uuid if task_uuid else str(getattr(status_message, "id", "dummy"))
    task_folder_path = Path(f"./downloads_{INSTANCE_ID}/{user_id}/{folder_name}/")
    task_folder_path.mkdir(parents=True, exist_ok=True)

    task_info = ACTIVE_PROCESSES.get(user_id, {}).get(task_uuid, {})
    cleanup_tags = task_info.get("cleanup_keywords", [])
    original_filename = "unknown_file"
    if msg.caption:
        # 🟢 FIX: Use the first line of the beautiful caption to name the file, avoiding Telegram truncation
        base_name = msg.caption.split('\n')[0].strip()
        ext = ""
        if msg.document and msg.document.file_name: ext = os.path.splitext(msg.document.file_name)[1]
        elif msg.video and msg.video.file_name: ext = os.path.splitext(msg.video.file_name)[1]
        elif msg.audio and msg.audio.file_name: ext = os.path.splitext(msg.audio.file_name)[1]
        elif msg_type == "Photo": ext = ".jpg"
        elif msg_type == "Voice": ext = ".ogg"
        
        original_filename = base_name + ext if not base_name.lower().endswith(ext.lower()) else base_name
    else:
        if msg.document and msg.document.file_name: original_filename = msg.document.file_name
        elif msg.video and msg.video.file_name: original_filename = msg.video.file_name
        elif msg.audio and msg.audio.file_name: original_filename = msg.audio.file_name
        elif msg_type == "Photo": original_filename = f"{msgid}.jpg"
        elif msg_type == "Voice": original_filename = f"{msgid}.ogg"

    # Clean the filename using global CLEANUP_TAGS + per-task cleanup_keywords
    clean_orig_name = clean_media_text(original_filename, custom_tags=cleanup_tags)
    safe_filename = build_media_filename(clean_orig_name, msg, index)
    safe_filename = clean_media_text(safe_filename, custom_tags=cleanup_tags)

    if not safe_filename.strip(): safe_filename = f"{msgid}.dat"
    file_path_to_save = task_folder_path / safe_filename
    ph_path = await _prepare_task_thumbnail(client, task_folder_path, user_id, task_uuid)

    # 🟢 DEFINED EARLY: Define fetcher first before we use it in the UI label!
    fetcher = acc if acc else client

    # 🟢 [NEW] Save current file name to active processes for Web UI
    if task_uuid and user_id in ACTIVE_PROCESSES and task_uuid in ACTIVE_PROCESSES[user_id]:
        ACTIVE_PROCESSES[user_id][task_uuid]["current_file"] = safe_filename
        ACTIVE_PROCESSES[user_id][task_uuid]["fetcher"] = _get_client_label(fetcher)
        
        predicted_uploader = get_dynamic_upload_client(client, acc, user_id, task_uuid, index)
        ACTIVE_PROCESSES[user_id][task_uuid]["uploader"] = _get_client_label(predicted_uploader)

    # 🟢 [FIX] Wipe previous file's progress so stale numbers NEVER carry over!
    if task_uuid:
        PROGRESS.pop(f"{task_uuid}:down", None)
        PROGRESS.pop(f"{task_uuid}:up", None)
        
    file_path = None
    download_success = False

    is_premium = False
    try:
        if acc:
            me = acc.me if acc.me else await acc.get_me()
            if me.is_premium: is_premium = True
    except Exception: pass
    
    # 🟢 DYNAMIC SPLIT LIMIT: Calculates 4GB vs 2GB buffers cleanly
    split_limit = (3980 * 1024 * 1024) if is_premium else (1980 * 1024 * 1024)

    # 🟢 Define the watcher shield variable
    is_w_task = False
    if user_id in ACTIVE_PROCESSES and task_uuid in ACTIVE_PROCESSES[user_id]:
        is_w_task = ACTIVE_PROCESSES[user_id][task_uuid].get("is_watcher", False)

    last_error_reason = None
    try: 
        for attempt in range(3):
            if (batch_temp.IS_BATCH.get(user_id) and not is_w_task) or (task_uuid and CANCEL_FLAGS.get(task_uuid)):
                _set_task_result_reason(user_id, task_uuid, "task cancelled before file processing")
                return False
            try:
                msg_fresh = await fetcher.get_messages(chatid, msgid)
                if msg_fresh.empty: return False
                
                file_size = 0
                if msg_fresh.document: file_size = msg_fresh.document.file_size
                elif msg_fresh.video: file_size = msg_fresh.video.file_size
                elif msg_fresh.audio: file_size = msg_fresh.audio.file_size

                if file_size > split_limit:
                    if is_premium and acc:
                        if USER_DOWNLOAD_SEMAPHORES[user_id].locked():
                            try:
                                if status_message: await status_message.edit_text(f"🚀 **Large File ({_pretty_bytes(file_size)})**\n⏳ Waiting in Download Queue...")
                            except FloodWait: pass
                        async with USER_DOWNLOAD_SEMAPHORES[user_id]:
                            file_path = await fetcher.download_media(msg_fresh, file_name=str(file_path_to_save), progress=progress, progress_args=["down", task_uuid])
                        
                        await process_internal_metadata(file_path, cleanup_tags) # 🟢 NEW
                        
                        try:
                            if status_message: await status_message.edit_text(f"☁️ **Uploading via Premium Session...**")
                        except FloodWait: pass
                        
                        bot_id = client.me.id if getattr(client, "me", None) else int(BOT_TOKEN.split(":")[0])
                        log_chat_id, log_topic_id = await get_fallback_log_chat(acc, user_id, bot_id=bot_id)
                        
                        # --- 🟢 PRESERVE SOURCE CAPTION & CLEAN TAGS ---
                        if msg_fresh.caption:
                            caption, caption_entities = clean_caption(
                                msg_fresh.caption,
                                msg_fresh.caption_entities,
                                custom_tags=cleanup_tags
                            )
                            p_mode = None
                        else:
                            custom_cap = await build_rich_caption(file_path, msg_type, msg_fresh, override_name=safe_filename)
                            if custom_cap:
                                caption = custom_cap
                                caption_entities = None
                                p_mode = enums.ParseMode.HTML
                            else:
                                caption, caption_entities = None, None
                                p_mode = None

                        a_dur = getattr(msg_fresh.audio, "duration", 0) if getattr(msg_fresh, "audio", None) else 0
                        a_perf = getattr(msg_fresh.audio, "performer", None) if getattr(msg_fresh, "audio", None) else None
                        a_tit = getattr(msg_fresh.audio, "title", None) if getattr(msg_fresh, "audio", None) else None
                        a_perf = clean_media_text(a_perf) if a_perf else a_perf
                        a_tit = clean_media_text(a_tit) if a_tit else a_tit

                        # 🟢 SMART AUDIO TAG EXTRACTOR: Fixes <unknown> artists!
                        if msg_type == "Audio":
                            if not a_perf or a_perf.lower() in ["unknown", "<unknown>"]:
                                clean_name = os.path.splitext(safe_filename)[0]
                                if " - " in clean_name:
                                    parts = clean_name.split(" - ", 1)
                                    a_perf = parts[0].strip() # Artist is before the dash
                                    if not a_tit or a_tit.lower() in ["unknown", "<unknown>", clean_name.lower()]:
                                        a_tit = parts[1].strip() # Title is after the dash
                                else:
                                    a_perf = "Unknown Artist"
                            if not a_tit or a_tit.lower() in ["unknown", "<unknown>"]:
                                a_tit = os.path.splitext(safe_filename)[0]

                        v_dur = getattr(msg_fresh.video, "duration", 0) if getattr(msg_fresh, "video", None) else 0
                        v_w = getattr(msg_fresh.video, "width", 0) if getattr(msg_fresh, "video", None) else 0
                        v_h = getattr(msg_fresh.video, "height", 0) if getattr(msg_fresh, "video", None) else 0

                        sent_msg = None
                        
                        try:
                            kwargs = {"chat_id": log_chat_id, "caption": caption}
                            if log_topic_id: kwargs["message_thread_id"] = log_topic_id
                            if caption_entities: kwargs["caption_entities"] = caption_entities
                            if p_mode: kwargs["parse_mode"] = p_mode
                            if ph_path and os.path.exists(ph_path): kwargs["thumb"] = ph_path
                            p_args = ["up", task_uuid]
                            
                            if "Document" == msg_type: sent_msg = await acc.send_document(document=file_path, progress=progress, progress_args=p_args, **kwargs)
                            elif "Video" == msg_type: sent_msg = await acc.send_video(video=file_path, duration=v_dur, width=v_w, height=v_h, progress=progress, progress_args=p_args, **kwargs)
                            elif "Audio" == msg_type: sent_msg = await acc.send_audio(audio=file_path, duration=a_dur, performer=a_perf, title=a_tit, progress=progress, progress_args=p_args, **kwargs)
                            else: sent_msg = await acc.send_document(document=file_path, progress=progress, progress_args=p_args, **kwargs)
                            
                            if sent_msg:
                                try:
                                    bot_read_chat_id = user_id if log_chat_id == bot_id else log_chat_id
                                    await safe_send(client, user_id, dest_chat_id, task_uuid, True, client.copy_message, chat_id=dest_chat_id, from_chat_id=bot_read_chat_id, message_id=sent_msg.id, message_thread_id=dest_thread_id)
                                except Exception:
                                    await safe_send(acc, user_id, dest_chat_id, task_uuid, False, acc.copy_message, chat_id=dest_chat_id, from_chat_id=log_chat_id, message_id=sent_msg.id, message_thread_id=dest_thread_id)
                        except Exception as up_err:
                            raise up_err
                        finally:
                            try:
                                if file_path and os.path.exists(file_path): os.remove(file_path)
                            except Exception: pass
                        return True
                    else:
                        if USER_DOWNLOAD_SEMAPHORES[user_id].locked():
                            try:
                                if status_message: await status_message.edit_text(f"✂️ **Large File ({_pretty_bytes(file_size)})**\n⏳ Waiting in Download Queue...")
                            except FloodWait: pass
                        async with USER_DOWNLOAD_SEMAPHORES[user_id]:
                            file_path = await fetcher.download_media(msg_fresh, file_name=str(file_path_to_save), progress=progress, progress_args=["down", task_uuid])
                        
                        await process_internal_metadata(file_path, cleanup_tags) # 🟢 NEW
                        
                        try:
                            if status_message: await status_message.edit_text(f"✂️ **Splitting large file ({_pretty_bytes(file_size)})...**")
                        except FloodWait: pass

                        # --- 🟢 PRESERVE SOURCE CAPTION & CLEAN TAGS FOR SPLIT PARTS ---
                        if msg_fresh.caption:
                            caption, caption_entities = clean_caption(
                                msg_fresh.caption,
                                msg_fresh.caption_entities,
                                custom_tags=cleanup_tags
                            )
                            p_mode = None
                        else:
                            custom_cap = await build_rich_caption(file_path, msg_type, msg_fresh, override_name=safe_filename)
                            if custom_cap:
                                caption = custom_cap
                                caption_entities = None
                                p_mode = enums.ParseMode.HTML
                            else:
                                caption, caption_entities = None, None
                                p_mode = None

                        # 🟢 USE DYNAMIC CHUNK SIZE (Based on Premium)
                        parts = await split_file_python(file_path, chunk_size=split_limit)
                        
                        if task_uuid and f"{task_uuid}:up" in PROGRESS: del PROGRESS[f"{task_uuid}:up"]
                    
                    async with USER_SEMAPHORES[user_id]:
                        async with SERVER_UPLOAD_LIMIT:
                            for part in parts:
                                if (batch_temp.IS_BATCH.get(user_id) and not is_w_task) or (task_uuid and CANCEL_FLAGS.get(task_uuid)): raise Exception("CANCELLED")
                                
                                # 🟢 DYNAMIC CAPTION
                                if msg_fresh.caption:
                                    final_cap = caption
                                else:
                                    part_size = os.path.getsize(part)
                                    part_name = Path(part).name
                                    part_cap = await build_rich_caption(file_path, msg_type, msg_fresh, override_name=part_name, override_size=part_size)
                                    final_cap = part_cap if part_cap else caption

                                while True:
                                    await USER_FLOOD_LOCKS[user_id].wait_if_locked() 
                                    try:
                                        kwargs = {"chat_id": dest_chat_id, "document": str(part), "caption": final_cap}
                                        if caption_entities: kwargs["caption_entities"] = caption_entities
                                        if p_mode: kwargs["parse_mode"] = p_mode
                                        if dest_thread_id: kwargs["message_thread_id"] = dest_thread_id
                                        if ph_path and os.path.exists(ph_path): kwargs["thumb"] = ph_path
                                        
                                        try:
                                            await safe_send(upload_client, user_id, dest_chat_id, task_uuid, True, upload_client.send_document, **kwargs)
                                        except Exception:
                                            if acc: await safe_send(acc, user_id, dest_chat_id, task_uuid, False, acc.send_document, **kwargs)
                                        break
                                    except FloodWait as e: 
                                        if e.value > 300: raise e
                                        USER_FLOOD_LOCKS[user_id].set_lock(e.value + 5) 
                                        await asyncio.sleep(e.value + 5)
                                    except Exception: break
                                try: 
                                    if os.path.exists(part): os.remove(part)
                                except Exception: pass
                    
                    try:
                        if file_path and os.path.exists(file_path): os.remove(file_path)
                    except Exception: pass
                    return True 
                else:
                    try:
                        if USER_DOWNLOAD_SEMAPHORES[user_id].locked():
                            try:
                                if status_message: await status_message.edit_text(f"⏳ **Queued...**\nWaiting for active download to finish...")
                            except FloodWait: pass
                        async with USER_DOWNLOAD_SEMAPHORES[user_id]:
                            file_path = await asyncio.wait_for(
                                fetcher.download_media(msg_fresh, file_name=str(file_path_to_save), progress=progress, progress_args=["down", task_uuid]),
                                timeout=1200
                            )
                        
                        await process_internal_metadata(file_path, cleanup_tags) # 🟢 NEW
                    except asyncio.TimeoutError:
                        return False
                
                try:
                    thumb = None
                    if msg_fresh.document and msg_fresh.document.thumbs: thumb = msg_fresh.document.thumbs[0]
                    elif msg_fresh.video and msg_fresh.video.thumbs: thumb = msg_fresh.video.thumbs[0]
                    elif msg_fresh.audio and msg_fresh.audio.thumbs: thumb = msg_fresh.audio.thumbs[0]
                    if thumb and not ph_path: ph_path = await fetcher.download_media(thumb.file_id, file_name=str(task_folder_path / "thumb.jpg"))
                except Exception: pass

                download_success = True
                break
            except FloodWait as e: 
                if e.value > 300: raise e
                USER_FLOOD_LOCKS[user_id].set_lock(e.value + 5) 
                await asyncio.sleep(e.value + 5)
            except Exception as e:
                if "CANCELLED" in str(e): return False
                last_error_reason = f"{type(e).__name__}: {e}"
                _set_task_result_reason(user_id, task_uuid, f"download attempt {attempt + 1}/3 failed: {last_error_reason}")
                logger.warning(
                    "FILE_ATTEMPT scope=restricted user_id=%s task_id=%s source_id=%s message_id=%s file=%r attempt=%s/3 reason=%r",
                    user_id, task_uuid or "-", chatid, msgid, safe_filename, attempt + 1, last_error_reason,
                )
                await asyncio.sleep(5)

        if not download_success:
            _set_task_result_reason(user_id, task_uuid, last_error_reason or "download failed without an exception")
            return False
        if (batch_temp.IS_BATCH.get(user_id) and not is_w_task) or (task_uuid and CANCEL_FLAGS.get(task_uuid)):
            _set_task_result_reason(user_id, task_uuid, "task cancelled after download")
            return False

        if task_uuid:
            PROGRESS.pop(f"{task_uuid}:up", None)
            PROGRESS.pop(f"{task_uuid}:down", None)
        
        # --- 🟢 PRESERVE SOURCE CAPTION & CLEAN TAGS ---
        if msg_fresh.caption:
            caption, caption_entities = clean_caption(
                msg_fresh.caption,
                msg_fresh.caption_entities,
                custom_tags=cleanup_tags
            )
            p_mode = None
        else:
            # Fallback to MediaInfo metadata box only if the source post had no caption
            custom_cap = await build_rich_caption(file_path, msg_type, msg_fresh, override_name=safe_filename)
            if custom_cap:
                caption = custom_cap
                caption_entities = None
                p_mode = enums.ParseMode.HTML
            else:
                caption, caption_entities = None, None
                p_mode = None
        
        upload_success = False

        # 🟢 NEW: Select an Upload Client (Worker Bot > Main Bot)
        file_size_final = os.path.getsize(file_path) if file_path and os.path.exists(file_path) else 0
        
        # 🟢 FORCE USER SESSION: Standard bots crash if handed files > 2GB, AND Worker bots can't upload to DMs!
        is_dest_dm = isinstance(dest_chat_id, int) and dest_chat_id > 0
        if (file_size_final > (1980 * 1024 * 1024) and is_premium and acc) or (is_dest_dm and acc):
            upload_client = acc
        else:
            upload_client = get_dynamic_upload_client(client, acc, user_id, task_uuid, index)
            
        async with SERVER_UPLOAD_LIMIT:
            async with USER_SEMAPHORES[user_id]:
                while True:
                    if (batch_temp.IS_BATCH.get(user_id) and not is_w_task) or (task_uuid and CANCEL_FLAGS.get(task_uuid)): break
                    
                    await USER_FLOOD_LOCKS[user_id].wait_if_locked() 
                    try:
                        kwargs = {"chat_id": dest_chat_id, "message_thread_id": dest_thread_id, "caption": caption}
                        if caption_entities: kwargs["caption_entities"] = caption_entities
                        if p_mode: kwargs["parse_mode"] = p_mode
                        if ph_path and os.path.exists(ph_path): kwargs["thumb"] = ph_path
                            
                        p_args = ["up", task_uuid]
                        p_func = progress

                        a_dur = getattr(msg_fresh.audio, "duration", 0) if getattr(msg_fresh, "audio", None) else 0
                        a_perf = getattr(msg_fresh.audio, "performer", None) if getattr(msg_fresh, "audio", None) else None
                        a_tit = getattr(msg_fresh.audio, "title", None) if getattr(msg_fresh, "audio", None) else None
                        a_perf = clean_media_text(a_perf) if a_perf else a_perf
                        a_tit = clean_media_text(a_tit) if a_tit else a_tit

                        if msg_type == "Audio":
                            if not a_perf or a_perf.lower() in ["unknown", "<unknown>"]:
                                clean_name = os.path.splitext(safe_filename)[0]
                                if " - " in clean_name:
                                    parts = clean_name.split(" - ", 1)
                                    a_perf = parts[0].strip() 
                                    if not a_tit or a_tit.lower() in ["unknown", "<unknown>", clean_name.lower()]:
                                        a_tit = parts[1].strip()
                                else:
                                    a_perf = "Unknown Artist"
                            if not a_tit or a_tit.lower() in ["unknown", "<unknown>"]:
                                a_tit = os.path.splitext(safe_filename)[0]

                        v_dur = getattr(msg_fresh.video, "duration", 0) if getattr(msg_fresh, "video", None) else 0
                        v_w = getattr(msg_fresh.video, "width", 0) if getattr(msg_fresh, "video", None) else 0
                        v_h = getattr(msg_fresh.video, "height", 0) if getattr(msg_fresh, "video", None) else 0

                        sent = False
                        # Safe copy of kwargs that strips unsupported parameters for Photos/Voices/Stickers
                        upload_kwargs = dict(kwargs)
                        if msg_type in ("Photo", "Voice", "Sticker"):
                            upload_kwargs.pop("thumb", None)
                        if msg_type == "Sticker":
                            upload_kwargs.pop("caption", None)
                            upload_kwargs.pop("caption_entities", None)
                            upload_kwargs.pop("parse_mode", None)

                        try:
                            if msg_type == "Document": await safe_send(upload_client, user_id, dest_chat_id, task_uuid, True, upload_client.send_document, document=file_path, progress=p_func, progress_args=p_args, **upload_kwargs)
                            elif msg_type == "Video": await safe_send(upload_client, user_id, dest_chat_id, task_uuid, True, upload_client.send_video, video=file_path, duration=v_dur, width=v_w, height=v_h, progress=p_func, progress_args=p_args, **upload_kwargs)
                            elif msg_type == "Audio": await safe_send(upload_client, user_id, dest_chat_id, task_uuid, True, upload_client.send_audio, audio=file_path, duration=a_dur, performer=a_perf, title=a_tit, progress=p_func, progress_args=p_args, **upload_kwargs)
                            elif msg_type == "Photo": await safe_send(upload_client, user_id, dest_chat_id, task_uuid, True, upload_client.send_photo, photo=file_path, **upload_kwargs)
                            elif msg_type == "Voice": await safe_send(upload_client, user_id, dest_chat_id, task_uuid, True, upload_client.send_voice, voice=file_path, progress=p_func, progress_args=p_args, **upload_kwargs)
                            elif msg_type == "Animation": await safe_send(upload_client, user_id, dest_chat_id, task_uuid, True, upload_client.send_animation, animation=file_path, **upload_kwargs)
                            elif msg_type == "Sticker": await safe_send(upload_client, user_id, dest_chat_id, task_uuid, True, upload_client.send_sticker, chat_id=dest_chat_id, sticker=file_path, message_thread_id=dest_thread_id)
                            else:
                                raise ValueError(f"Unsupported upload type: {msg_type}")
                            sent = True
                        except Exception:
                            if acc:
                                if task_uuid and user_id in ACTIVE_PROCESSES and task_uuid in ACTIVE_PROCESSES[user_id]:
                                    ACTIVE_PROCESSES[user_id][task_uuid]["uploader"] = _get_client_label(acc)
                                    
                                if msg_type == "Document": await safe_send(acc, user_id, dest_chat_id, task_uuid, False, acc.send_document, document=file_path, progress=p_func, progress_args=p_args, **upload_kwargs)
                                elif msg_type == "Video": await safe_send(acc, user_id, dest_chat_id, task_uuid, False, acc.send_video, video=file_path, duration=v_dur, width=v_w, height=v_h, progress=p_func, progress_args=p_args, **upload_kwargs)
                                elif msg_type == "Audio": await safe_send(acc, user_id, dest_chat_id, task_uuid, False, acc.send_audio, audio=file_path, duration=a_dur, performer=a_perf, title=a_tit, progress=p_func, progress_args=p_args, **upload_kwargs)
                                elif msg_type == "Photo": await safe_send(acc, user_id, dest_chat_id, task_uuid, False, acc.send_photo, photo=file_path, **upload_kwargs)
                                elif msg_type == "Voice": await safe_send(acc, user_id, dest_chat_id, task_uuid, False, acc.send_voice, voice=file_path, progress=p_func, progress_args=p_args, **upload_kwargs)
                                elif msg_type == "Animation": await safe_send(acc, user_id, dest_chat_id, task_uuid, False, acc.send_animation, animation=file_path, **upload_kwargs)
                                elif msg_type == "Sticker": await safe_send(acc, user_id, dest_chat_id, task_uuid, False, acc.send_sticker, chat_id=dest_chat_id, sticker=file_path, message_thread_id=dest_thread_id)
                                else:
                                    raise ValueError(f"Unsupported upload type: {msg_type}")
                                sent = True

                        if sent:
                            upload_success = True
                            break
                    except FloodWait as e:
                        if e.value > 300: raise e
                        USER_FLOOD_LOCKS[user_id].set_lock(e.value + 5) 
                        await asyncio.sleep(e.value + 5)
                    except Exception as e:
                        if "CANCELLED" in str(e): break
                        last_error_reason = f"{type(e).__name__}: {e}"
                        _set_task_result_reason(user_id, task_uuid, f"upload failed: {last_error_reason}")
                        logger.error(
                            "FILE_UPLOAD_FAILED user_id=%s task_id=%s source_id=%s message_id=%s file=%r reason=%r",
                            user_id, task_uuid or "-", chatid, msgid, safe_filename, last_error_reason,
                            exc_info=True,
                        )
                        break
        
        if not upload_success and not last_error_reason:
            _set_task_result_reason(user_id, task_uuid, "upload did not complete; task was cancelled or sender returned no result")
        return upload_success

    finally:
        try:
            if 'task_folder_path' in locals() and task_folder_path.exists():
                shutil.rmtree(task_folder_path)
        except Exception: pass
        gc.collect()
