# --- 2. MESSAGE FETCHER & VALIDATOR ---
# ==============================================================================
from pyrogram.errors import FloodWait

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
        except Exception:
            return None, None

    if not msg or msg.empty: return None, None

    if filter_thread_id is not None:
        actual_thread = getattr(msg, "message_thread_id", None)
        if actual_thread is None:
            # 🟢 FIX: If targeting General Topic (1), a missing thread ID is a valid match!
            if filter_thread_id != 1 and getattr(msg, "reply_to_top_message_id", None) != filter_thread_id and getattr(msg, "reply_to_message_id", None) != filter_thread_id and msg.id != filter_thread_id:
                return None, None
        elif actual_thread != filter_thread_id:
            return None, None

    msg_type = get_message_type(msg)
    if not msg_type: return None, None
    if allowed_types is not None and msg_type not in allowed_types: return None, None
    
    # 🟢 FIX: Shield Watchers from Global Cancels
    is_w_task = False
    if user_id in ACTIVE_PROCESSES and task_uuid in ACTIVE_PROCESSES[user_id]:
        is_w_task = ACTIVE_PROCESSES[user_id][task_uuid].get("is_watcher", False)
        
    if (batch_temp.IS_BATCH.get(user_id) and not is_w_task) or (task_uuid and CANCEL_FLAGS.get(task_uuid)): 
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

async def _execute_unrestricted_copy(client, acc, chat_id, msgid, dest_chat_id, dest_thread_id, msg, msg_type, user_id, task_uuid, delay):
    # 🟢 Select an Upload Client (Worker Bot > Main Bot)
    upload_client = client
    worker_bots = USER_TASK_BOTS.get(user_id, [])
    if worker_bots:
        connected_workers = [wb for wb in worker_bots if getattr(wb, "is_connected", False)]
        if connected_workers:
            upload_client = connected_workers[int(time.time()) % len(connected_workers)]
            
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
            await safe_send(upload_client, user_id, dest_chat_id, task_uuid, True, upload_client.copy_message, chat_id=dest_chat_id, from_chat_id=chat_id, message_id=msgid, message_thread_id=dest_thread_id)
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

async def _execute_public_live_unrestricted_copy(client, acc, chat_id, msgid, dest_chat_id, dest_thread_id, msg, msg_type, user_id, task_uuid, delay):
    # 🟢 Select an Upload Client (Worker Bot > Main Bot)
    upload_client = client
    worker_bots = USER_TASK_BOTS.get(user_id, [])
    if worker_bots:
        connected_workers = [wb for wb in worker_bots if getattr(wb, "is_connected", False)]
        if connected_workers:
            upload_client = connected_workers[int(time.time()) % len(connected_workers)]

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
    return await _execute_public_live_unrestricted_copy(client, acc, chat_id, msgid, dest_chat_id, dest_thread_id, msg, msg_type, kwargs.get("user_id"), kwargs.get("task_uuid"), kwargs.get("delay", 3))

# 2 Pvt link
async def handle_unrestricted_private(client, acc, chat_id, msgid, dest_chat_id, dest_thread_id, msg, msg_type, **kwargs):
    return await _execute_unrestricted_copy(client, acc, chat_id, msgid, dest_chat_id, dest_thread_id, msg, msg_type, kwargs.get("user_id"), kwargs.get("task_uuid"), kwargs.get("delay", 3))

# 3 Live watch
async def handle_unrestricted_live(client, acc, chat_id, msgid, dest_chat_id, dest_thread_id, msg, msg_type, **kwargs):
    return await _execute_public_live_unrestricted_copy(client, acc, chat_id, msgid, dest_chat_id, dest_thread_id, msg, msg_type, kwargs.get("user_id"), kwargs.get("task_uuid"), kwargs.get("delay", 3))

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

async def build_rich_caption(file_path, msg_type, msg):
    try:
        file_name = "Unknown"
        if msg_type == "Audio" and getattr(msg, "audio", None): file_name = getattr(msg.audio, "file_name", "Audio.m4a")
        elif msg_type == "Video" and getattr(msg, "video", None): file_name = getattr(msg.video, "file_name", "Video.mp4")
        elif getattr(msg, "document", None): file_name = getattr(msg.document, "file_name", "File.dat")
        
        if not file_path or not os.path.exists(file_path):
            return None
            
        size_bytes = os.path.getsize(file_path)
        size_str = _pretty_bytes(size_bytes)
        
        if msg_type == "Audio":
            bitrate_str = "Unknown Quality"
            try:
                # 🟢 FIX: Fetch Format, BitDepth, Bitrate, and SampleRate simultaneously
                cmd = ["mediainfo", "--Inform=Audio;%Format%|%BitDepth%|%BitRate/String%|%SamplingRate/String%", str(file_path)]
                proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
                stdout, _ = await proc.communicate()
                
                # Get the first audio stream only to prevent multiline errors
                out = stdout.decode('utf-8', errors='ignore').strip().split('\n')[0] 
                
                if out:
                    parts = out.split('|')
                    if len(parts) >= 4:
                        fmt = parts[0].strip()
                        depth = parts[1].strip()
                        bitrate = parts[2].strip().replace(" ", "")
                        sample_rate = parts[3].strip().replace(" ", "")
                        
                        # Clean up technical formats for a beautiful UI display
                        if "MPEG Audio" in fmt: fmt = "MP3"
                        elif "AAC" in fmt: fmt = "AAC"
                        elif "FLAC" in fmt: fmt = "FLAC"
                        elif "ALAC" in fmt: fmt = "ALAC"
                        elif "Wave" in fmt: fmt = "WAV"
                        elif "Opus" in fmt: fmt = "OPUS"
                        elif "Vorbis" in fmt: fmt = "OGG"
                        
                        # Lossless formats show Bit Depth (e.g. 24Bit), Lossy show Bitrate (e.g. 320kbps)
                        if depth:
                            bitrate_str = f"{fmt} • {depth}Bit - {sample_rate}"
                        elif bitrate:
                            bitrate_str = f"{fmt} • {bitrate} - {sample_rate}"
                        else:
                            bitrate_str = f"{fmt} • {sample_rate}"
            except: 
                pass
                
            return f"<b>{html.escape(file_name)}</b>\n\n🗂 <code>{size_str}</code>\n🎧 <code>{bitrate_str}</code>"
            
        elif msg_type == "Video":
            w = getattr(msg.video, "width", 0) if getattr(msg, "video", None) else 0
            h = getattr(msg.video, "height", 0) if getattr(msg, "video", None) else 0
            dur = getattr(msg.video, "duration", 0) if getattr(msg, "video", None) else 0
            dur_str = f"{dur//60}m{dur%60}s" if dur else "Unknown"
            
            audio_lng = "Unknown"
            sub_lng = "None"
            try:
                cmd = ["mediainfo", "--Inform=General;%Audio_Language_List%|%Text_Language_List%", str(file_path)]
                proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
                stdout, _ = await proc.communicate()
                out = stdout.decode().strip().split('|')
                if len(out) == 2:
                    a_list, s_list = out[0].strip(), out[1].strip()
                    # 🟢 FIX: Replace MediaInfo's ' / ' separator with a clean comma
                    if a_list: audio_lng = a_list.replace(" / ", ", ")
                    if s_list: sub_lng = s_list.replace(" / ", ", ")
                elif len(out) == 1 and out[0].strip():
                    audio_lng = out[0].strip().replace(" / ", ", ")
            except: pass
            
            return f"<b>{html.escape(file_name)}</b>\n\n🗂 <code>{size_str}</code> 💎 <code>{w}x{h}</code>\n⏳ <code>{dur_str}</code> 💬 <code>{sub_lng}</code>\n🔊 <code>{audio_lng}</code>"
            
    except Exception as e:
        logger.debug(f"Rich caption generation failed: {e}")
    return None
    
# ==============================================================================
# --- CORE RESTRICTED DOWNLOAD / UPLOAD ENGINE ---
# ==============================================================================

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

    original_filename = "unknown_file"
    if msg.document and msg.document.file_name: original_filename = msg.document.file_name
    elif msg.video and msg.video.file_name: original_filename = msg.video.file_name
    elif msg.audio and msg.audio.file_name: original_filename = msg.audio.file_name
    elif msg_type == "Photo": original_filename = f"{msgid}.jpg"
    elif msg_type == "Voice": original_filename = f"{msgid}.ogg"

    safe_filename = sanitize_filename(original_filename)
    if not safe_filename.strip(): safe_filename = f"{msgid}.dat"
    file_path_to_save = task_folder_path / safe_filename

    # 🟢 DEFINED EARLY: Define fetcher first before we use it in the UI label!
    fetcher = acc if acc else client

    # 🟢 [NEW] Save current file name to active processes for Web UI
    if task_uuid and user_id in ACTIVE_PROCESSES and task_uuid in ACTIVE_PROCESSES[user_id]:
        ACTIVE_PROCESSES[user_id][task_uuid]["current_file"] = safe_filename
        ACTIVE_PROCESSES[user_id][task_uuid]["fetcher"] = _get_client_label(fetcher)
        
        predicted_uploader = client
        worker_bots = USER_TASK_BOTS.get(user_id, [])
        if worker_bots:
            connected_workers = [wb for wb in worker_bots if getattr(wb, "is_connected", False)]
            if connected_workers:
                predicted_uploader = connected_workers[index % len(connected_workers)]
        ACTIVE_PROCESSES[user_id][task_uuid]["uploader"] = _get_client_label(predicted_uploader)

    # 🟢 [FIX] Wipe previous file's progress so stale numbers NEVER carry over!
    if task_uuid:
        PROGRESS.pop(f"{task_uuid}:down", None)
        PROGRESS.pop(f"{task_uuid}:up", None)
        
    file_path = None
    ph_path = None
    download_success = False

    split_limit = 2000 * 1024 * 1024 
    is_premium = False
    
    try:
        if acc:
            me = acc.me if acc.me else await acc.get_me()
            if me.is_premium: is_premium = True
    except Exception: pass

    # 🟢 Define the watcher shield variable
    is_w_task = False
    if user_id in ACTIVE_PROCESSES and task_uuid in ACTIVE_PROCESSES[user_id]:
        is_w_task = ACTIVE_PROCESSES[user_id][task_uuid].get("is_watcher", False)

    try: 
        for attempt in range(3):
            if (batch_temp.IS_BATCH.get(user_id) and not is_w_task) or (task_uuid and CANCEL_FLAGS.get(task_uuid)): return False
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
                        
                        try:
                            if status_message: await status_message.edit_text(f"☁️ **Uploading via Premium Session...**")
                        except FloodWait: pass
                        
                        bot_id = client.me.id if getattr(client, "me", None) else int(BOT_TOKEN.split(":")[0])
                        log_chat_id, log_topic_id = await get_fallback_log_chat(acc, user_id, bot_id=bot_id)
                        
                        # --- 🟢 RICH CAPTION EXTRACTION ---
                        custom_cap = await build_rich_caption(file_path, msg_type, msg_fresh)
                        if custom_cap:
                            caption = custom_cap
                            caption_entities = None
                            p_mode = enums.ParseMode.HTML
                        else:
                            caption = msg_fresh.caption if getattr(msg_fresh, "caption", None) else ""
                            caption_entities = msg_fresh.caption_entities if getattr(msg_fresh, "caption_entities", None) else None
                            p_mode = None

                        a_dur = getattr(msg_fresh.audio, "duration", 0) if getattr(msg_fresh, "audio", None) else 0
                        a_perf = getattr(msg_fresh.audio, "performer", None) if getattr(msg_fresh, "audio", None) else None
                        a_tit = getattr(msg_fresh.audio, "title", None) if getattr(msg_fresh, "audio", None) else None

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
                        
                        try:
                            if status_message: await status_message.edit_text(f"✂️ **Splitting large file ({_pretty_bytes(file_size)})...**")
                        except FloodWait: pass

                        # --- 🟢 RICH CAPTION EXTRACTION FOR SPLIT PARTS ---
                        custom_cap = await build_rich_caption(file_path, msg_type, msg_fresh)
                        if custom_cap:
                            caption = custom_cap
                            caption_entities = None
                            p_mode = enums.ParseMode.HTML
                        else:
                            caption = msg_fresh.caption if getattr(msg_fresh, "caption", None) else ""
                            caption_entities = msg_fresh.caption_entities if getattr(msg_fresh, "caption_entities", None) else None
                            p_mode = None

                        parts = await split_file_python(file_path, chunk_size=1900*1024*1024)
                        
                        if task_uuid and f"{task_uuid}:up" in PROGRESS: del PROGRESS[f"{task_uuid}:up"]
                    
                    async with USER_SEMAPHORES[user_id]:
                        async with SERVER_UPLOAD_LIMIT:
                            for part in parts:
                                if (batch_temp.IS_BATCH.get(user_id) and not is_w_task) or (task_uuid and CANCEL_FLAGS.get(task_uuid)): raise Exception("CANCELLED")
                                while True:
                                    await USER_FLOOD_LOCKS[user_id].wait_if_locked() 
                                    try:
                                        kwargs = {"chat_id": dest_chat_id, "document": str(part), "caption": caption}
                                        if caption_entities: kwargs["caption_entities"] = caption_entities
                                        if p_mode: kwargs["parse_mode"] = p_mode
                                        if dest_thread_id: kwargs["message_thread_id"] = dest_thread_id
                                        
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
                    except asyncio.TimeoutError:
                        return False
                
                try:
                    thumb = None
                    if msg_fresh.document and msg_fresh.document.thumbs: thumb = msg_fresh.document.thumbs[0]
                    elif msg_fresh.video and msg_fresh.video.thumbs: thumb = msg_fresh.video.thumbs[0]
                    elif msg_fresh.audio and msg_fresh.audio.thumbs: thumb = msg_fresh.audio.thumbs[0]
                    if thumb: ph_path = await fetcher.download_media(thumb.file_id, file_name=str(task_folder_path / "thumb.jpg"))
                except Exception: pass

                download_success = True
                break
            except FloodWait as e: 
                if e.value > 300: raise e
                USER_FLOOD_LOCKS[user_id].set_lock(e.value + 5) 
                await asyncio.sleep(e.value + 5)
            except Exception as e:
                if "CANCELLED" in str(e): return False
                await asyncio.sleep(5)

        if not download_success: return False
        if (batch_temp.IS_BATCH.get(user_id) and not is_w_task) or (task_uuid and CANCEL_FLAGS.get(task_uuid)): return False

        if task_uuid:
            PROGRESS.pop(f"{task_uuid}:up", None)
            PROGRESS.pop(f"{task_uuid}:down", None)
        
        # --- 🟢 RICH CAPTION EXTRACTION FOR NORMAL FILES ---
        custom_cap = await build_rich_caption(file_path, msg_type, msg_fresh)
        if custom_cap:
            caption = custom_cap
            caption_entities = None
            p_mode = enums.ParseMode.HTML
        else:
            caption = msg_fresh.caption if getattr(msg_fresh, "caption", None) else None
            caption_entities = msg_fresh.caption_entities if getattr(msg_fresh, "caption_entities", None) else None
            p_mode = None
        
        upload_success = False

        # 🟢 NEW: Select an Upload Client (Worker Bot > Main Bot)
        upload_client = client
        worker_bots = USER_TASK_BOTS.get(user_id, [])
        if worker_bots:
            connected_workers = [wb for wb in worker_bots if getattr(wb, "is_connected", False)]
            if connected_workers:
                upload_client = connected_workers[index % len(connected_workers)]
        
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
                        try:
                            if msg_type == "Document": await safe_send(upload_client, user_id, dest_chat_id, task_uuid, True, upload_client.send_document, document=file_path, progress=p_func, progress_args=p_args, **kwargs)
                            elif msg_type == "Video": await safe_send(upload_client, user_id, dest_chat_id, task_uuid, True, upload_client.send_video, video=file_path, duration=v_dur, width=v_w, height=v_h, progress=p_func, progress_args=p_args, **kwargs)
                            elif msg_type == "Audio": await safe_send(upload_client, user_id, dest_chat_id, task_uuid, True, upload_client.send_audio, audio=file_path, duration=a_dur, performer=a_perf, title=a_tit, progress=p_func, progress_args=p_args, **kwargs)
                            elif msg_type == "Photo": await safe_send(upload_client, user_id, dest_chat_id, task_uuid, True, upload_client.send_photo, photo=file_path, **kwargs)
                            elif msg_type == "Voice": await safe_send(upload_client, user_id, dest_chat_id, task_uuid, True, upload_client.send_voice, voice=file_path, progress=p_func, progress_args=p_args, **kwargs)
                            elif msg_type == "Animation": await safe_send(upload_client, user_id, dest_chat_id, task_uuid, True, upload_client.send_animation, animation=file_path, **kwargs)
                            elif msg_type == "Sticker": await safe_send(upload_client, user_id, dest_chat_id, task_uuid, True, upload_client.send_sticker, chat_id=dest_chat_id, sticker=file_path, message_thread_id=dest_thread_id)
                            else:
                                raise ValueError(f"Unsupported upload type: {msg_type}")
                            sent = True
                        except Exception:
                            if acc:
                                # 🟢 UPDATE UI: Show User Session taking over heavy upload!
                                if task_uuid and user_id in ACTIVE_PROCESSES and task_uuid in ACTIVE_PROCESSES[user_id]:
                                    ACTIVE_PROCESSES[user_id][task_uuid]["uploader"] = _get_client_label(acc)
                                    
                                if msg_type == "Document": await safe_send(acc, user_id, dest_chat_id, task_uuid, False, acc.send_document, document=file_path, progress=p_func, progress_args=p_args, **kwargs)
                                elif msg_type == "Video": await safe_send(acc, user_id, dest_chat_id, task_uuid, False, acc.send_video, video=file_path, duration=v_dur, width=v_w, height=v_h, progress=p_func, progress_args=p_args, **kwargs)
                                elif msg_type == "Audio": await safe_send(acc, user_id, dest_chat_id, task_uuid, False, acc.send_audio, audio=file_path, duration=a_dur, performer=a_perf, title=a_tit, progress=p_func, progress_args=p_args, **kwargs)
                                elif msg_type == "Photo": await safe_send(acc, user_id, dest_chat_id, task_uuid, False, acc.send_photo, photo=file_path, **kwargs)
                                elif msg_type == "Voice": await safe_send(acc, user_id, dest_chat_id, task_uuid, False, acc.send_voice, voice=file_path, progress=p_func, progress_args=p_args, **kwargs)
                                elif msg_type == "Animation": await safe_send(acc, user_id, dest_chat_id, task_uuid, False, acc.send_animation, animation=file_path, **kwargs)
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
                        break
        
        return upload_success

    finally:
        try:
            if 'task_folder_path' in locals() and task_folder_path.exists():
                shutil.rmtree(task_folder_path)
        except Exception: pass
        gc.collect()

