# ==============================================================================
# --- NEW ROBUSTNESS HELPERS ---
# ==============================================================================

async def send_log(text):
    if not LOG_CHANNEL:
        return
    try:
        chat_id, topic_id = parse_chat_topic(LOG_CHANNEL)
        await app.send_message(chat_id, text, message_thread_id=topic_id, disable_web_page_preview=True)
    except Exception as e:
        print(f"❌ Failed to send log: {e}")

# --- SMART LOG ROUTING ---
USER_LOG_CACHE = {}

async def get_fallback_log_chat(client_to_use, client_identifier, bot_id=None):
    """Finds the best available scratchpad chat. Tries LOG_CHANNEL -> ADMINS -> Bot's PM."""
    if client_identifier in USER_LOG_CACHE:
        return USER_LOG_CACHE[client_identifier]
        
    targets = []
    if LOG_CHANNEL:
        c_id, t_id = parse_chat_topic(LOG_CHANNEL)
        targets.append((c_id, t_id))
        
    for admin in ADMINS:
        targets.append((admin, None))
        
    # 🟢 If all else fails, use the DM between the User and the Bot!
    if bot_id and client_to_use != app:
        targets.append((bot_id, None))
    else:
        targets.append(("me", None)) # Failsafe for bot itself
    
    for c_id, t_id in targets:
        try:
            # 🟢 Pre-flight check to ensure write access BEFORE doing heavy uploads
            msg = await client_to_use.send_message(chat_id=c_id, text="🔄", message_thread_id=t_id)
            await msg.delete()
            USER_LOG_CACHE[client_identifier] = (c_id, t_id)
            return c_id, t_id
        except Exception:
            continue
            
    return "me", None

async def check_disk_space():
    try:
        total, used, free = shutil.disk_usage(".")
        free_mb = free / (1024 * 1024)
        if free_mb < 500: 
            return False
        return True
    except:
        return True

async def cleanup_watchdog():
    while True:
        await asyncio.sleep(600) 
        try:
            download_path = Path(f"./downloads_{INSTANCE_ID}")
            if not download_path.exists(): continue
            
            current_time = time.time()
            max_age = 2 * 60 * 60 
            
            for user_folder in download_path.iterdir():
                if not user_folder.is_dir():
                    continue

                for task_folder in user_folder.iterdir():
                    if not task_folder.is_dir():
                        continue

                    folder_time = task_folder.stat().st_mtime
                    if (current_time - folder_time) > max_age:
                        shutil.rmtree(task_folder)
                        await send_log(f"🧹 **Auto-Cleanup:** Deleted stuck folder `{task_folder.name}` (Older than 2h)")
        except Exception as e:
            logger.error(f"Watchdog Error: {e}", exc_info=True)
            
async def start_task_final(client: Client, message_context: Message, task_data: dict, delay: int, user_id: int):
    if not await check_disk_space():
        msg = "⚠️ **Server Busy:** Disk is almost full. Please wait for other tasks to finish."
        if isinstance(message_context, Message):
             await message_context.reply(msg, quote=True)
        await send_log("🚨 **Critical:** Disk Space Low (<500MB). Tasks rejected.")
        return

    if user_id not in ADMINS and batch_temp.ACTIVE_TASKS[user_id] >= MAX_CONCURRENT_TASKS_PER_USER:
        TASK_QUEUE[user_id].append({
            "client": client,
            "message": message_context,
            "data": dict(task_data), 
            "delay": delay
        })
        position = len(TASK_QUEUE[user_id])
        await message_context.reply(
            f"⏳ **Added to Queue:** Position #{position}\n"
            f"Task will start automatically when your current tasks finish.",
            quote=True
        )
        return

    task_uuid = uuid.uuid4().hex
    dest = task_data.get("dest_title", "Direct Message")
    
    batch_temp.ACTIVE_TASKS[user_id] += 1
    batch_temp.IS_BATCH[user_id] = False

    # 🟢 FIX: Explicitly direct users to the Web UI upon registration
    start_msg = f"✅ **Task Registered!**\nDestination: `{dest}`\nSpeed: `{delay}s` delay\nTask ID: `{task_uuid[:8]}`\n\n🌐 **Please open the Web Dashboard to track live progress.**"
    try:
        if isinstance(message_context, Message):
            if message_context.from_user.is_bot:
                await message_context.edit(start_msg)
            else:
                await message_context.reply(start_msg)
    except: pass

    if user_id not in ACTIVE_PROCESSES:
        ACTIVE_PROCESSES[user_id] = {}
    ACTIVE_PROCESSES[user_id][task_uuid] = {
        "user": task_data.get("dest_title", f"User({user_id})"),
        "dest_title_name": task_data.get("dest_title", "Direct Message"), 
        "item": task_data.get("link", "Unknown"),
        "started": time.time()
    }
    
    is_restricted = task_data.get("is_restricted", False)
    task_snapshot = dict(task_data)

    asyncio.create_task(
        process_links_logic(
            client,
            message_context,
            task_snapshot["link"],
            dest_chat_id=task_snapshot.get("dest_chat_id"),
            dest_thread_id=task_snapshot.get("dest_thread_id"),
            dest_title=dest,
            delay=delay,
            acc_user_id=user_id,
            task_uuid=task_uuid,
            is_restricted=is_restricted,
            allowed_types=task_snapshot.get("allowed_types")
        )
    )   

async def handle_public_unrestricted(client: Client, acc, chatid: str, msgid: int, dest_chat_id, dest_thread_id, user_id, task_uuid, filter_thread_id, allowed_types, delay=3, pre_fetched_msg=None):
    """Fast-Path exclusively for Public Unrestricted links. Supports Albums."""
    
    msg = pre_fetched_msg
    fetcher = acc if acc else client
    
    # 🟢 NEW: Load Balancer for the Fast-Path!
    upload_client = client
    worker_bots = USER_TASK_BOTS.get(user_id, [])
    if worker_bots:
        connected_workers = [wb for wb in worker_bots if getattr(wb, "is_connected", False)]
        if connected_workers:
            import random
            upload_client = random.choice(connected_workers)

    # 🟢 FIX: Inject UI Labels for Web Dashboard (Fast-Path bypasses router)
    if task_uuid and user_id in ACTIVE_PROCESSES and task_uuid in ACTIVE_PROCESSES[user_id]:
        def _lbl(c):
            if not c: return "Unknown"
            nm = getattr(c, "name", "Unknown")
            if "User_" in nm or "temp_acc_" in nm: return "👤 User Session"
            if "worker_bot_" in nm: return f"🤖 Worker {nm.split('_')[-1]}"
            if nm == "RestrictedBot": return "🤖 Main Bot"
            return f"🤖 {nm}"
        
        if "fetcher" not in ACTIVE_PROCESSES[user_id][task_uuid]:
            ACTIVE_PROCESSES[user_id][task_uuid]["fetcher"] = _lbl(fetcher)
        ACTIVE_PROCESSES[user_id][task_uuid]["uploader"] = _lbl(upload_client)

    if not msg:
        try:
            msg = await fetcher.get_messages(chatid, msgid)
        except Exception as e:
            logger.error(f"Failed to fetch msg {msgid}: {e}")
            return "FAILED"

    if not msg or msg.empty: 
        return "SKIPPED"

    # Strict Topic Filtering
    if filter_thread_id is not None:
        actual_thread = getattr(msg, "message_thread_id", None)
        if actual_thread is None:
            if filter_thread_id != 1 and getattr(msg, "reply_to_top_message_id", None) != filter_thread_id and getattr(msg, "reply_to_message_id", None) != filter_thread_id and msg.id != filter_thread_id:
                return "SKIPPED"
        elif actual_thread != filter_thread_id:
            return "SKIPPED"

    # Strict Type Filtering
    msg_type = get_message_type(msg)
    if not msg_type or (allowed_types and msg_type not in allowed_types):
        return "SKIPPED"

    # 🟢 Shield live watchers from global batch cancellations
    is_w_task = False
    if user_id in ACTIVE_PROCESSES and task_uuid in ACTIVE_PROCESSES[user_id]:
        is_w_task = ACTIVE_PROCESSES[user_id][task_uuid].get("is_watcher", False)

    if (batch_temp.IS_BATCH.get(user_id) and not is_w_task) or (task_uuid and CANCEL_FLAGS.get(task_uuid)):
        return "FAILED"

    # 🟢 Mid-Batch Restriction Fallback Ejector
    is_content_protected = getattr(msg, "has_protected_content", False) or getattr(msg.chat, "has_protected_content", False)
    if is_content_protected:
        return "FALLBACK_RESTRICTED"

    # 🟢 Text Fast-Forward
    if msg_type == "Text":
        try:
            await upload_client.send_message(dest_chat_id, msg.text, entities=msg.entities, message_thread_id=dest_thread_id)
            return "SUCCESS"
        except Exception as e:
            # 🟢 KICKS TO DOWNLOAD MODE IF FORWARDS ARE RESTRICTED
            if "CHAT_FORWARDS_RESTRICTED" in str(e) or "RESTRICTED" in str(e): return "FALLBACK_RESTRICTED"
            if acc:
                try:
                    await acc.send_message(dest_chat_id, msg.text, entities=msg.entities, message_thread_id=dest_thread_id)
                    return "SUCCESS"
                except Exception as e2: 
                    if "CHAT_FORWARDS_RESTRICTED" in str(e2) or "RESTRICTED" in str(e2): return "FALLBACK_RESTRICTED"
                    return "FAILED"
            return "FAILED"

    try:
        await USER_FLOOD_LOCKS[user_id].wait_if_locked()
        
        # 🟢 ALBUM LOGIC RE-INTEGRATED
        if msg.media_group_id:
            try: m_group = await fetcher.get_media_group(chatid, msgid)
            except: m_group = [msg]
            
            group_size = len(m_group)
            if task_uuid:
                for m in m_group: batch_temp.SKIP_IDS[task_uuid].add(m.id)

            try:
                copy_res = await upload_client.copy_media_group(chat_id=dest_chat_id, from_chat_id=chatid, message_id=msgid, message_thread_id=dest_thread_id)
            except Exception as e:
                if "CHAT_FORWARDS_RESTRICTED" in str(e) or "RESTRICTED" in str(e): return "FALLBACK_RESTRICTED"
                if acc:
                    try:
                        copy_res = await acc.copy_media_group(chat_id=dest_chat_id, from_chat_id=chatid, message_id=msgid, message_thread_id=dest_thread_id)
                    except Exception as e2:
                        if "CHAT_FORWARDS_RESTRICTED" in str(e2) or "RESTRICTED" in str(e2): return "FALLBACK_RESTRICTED"
                        copy_res = False
                else: copy_res = False
            
            if copy_res:
                if delay > 0 and group_size > 1: await asyncio.sleep(delay * (group_size - 1))
                return "SUCCESS"
            return "FAILED"

        # 🟢 Single Media Copy
        try:
            copy_res = await upload_client.copy_message(chat_id=dest_chat_id, from_chat_id=chatid, message_id=msgid, message_thread_id=dest_thread_id)
            if not copy_res: raise ValueError("Bot copy failed")
            return "SUCCESS"
        except Exception as e:
            if "CHAT_FORWARDS_RESTRICTED" in str(e) or "RESTRICTED" in str(e):
                return "FALLBACK_RESTRICTED"
            if acc:
                try: 
                    copy_res = await acc.copy_message(chat_id=dest_chat_id, from_chat_id=chatid, message_id=msgid, message_thread_id=dest_thread_id)
                    return "SUCCESS" if copy_res else "FAILED"
                except Exception as e2: 
                    if "CHAT_FORWARDS_RESTRICTED" in str(e2) or "RESTRICTED" in str(e2):
                        return "FALLBACK_RESTRICTED"
                    return "FAILED"
            return "FAILED"

    except FloodWait as e:
        USER_FLOOD_LOCKS[user_id].set_lock(e.value + 5)
        await asyncio.sleep(e.value + 5)
        return "FAILED" 
    except Exception as e:
        logger.error(f"Total copy failure for {msgid}: {e}")
        return "FAILED"

async def process_links_logic(client: Client, message: Message, text: str, dest_chat_id=None, dest_thread_id=None, dest_title="Direct Message", delay=3, acc_user_id=None, task_uuid=None, is_restricted=False, allowed_types=None, resume_from_id=None, saved_source_title=None):
    user_id = acc_user_id or (message.from_user.id if message and message.from_user else 0)
    
    # 🟢 Resolve Real User Name (Not Bot Name)
    real_user_name = None
    if message and message.from_user and not message.from_user.is_bot:
        real_user_name = message.from_user.first_name
        if message.from_user.last_name:
            real_user_name += f" {message.from_user.last_name}"
            
    if not real_user_name and user_id:
        user_doc = await db.col.find_one({"id": int(user_id)})
        if user_doc and user_doc.get("name") and not str(user_doc.get("name")).startswith("User "):
            real_user_name = user_doc.get("name")
            
    if not real_user_name and user_id:
        try:
            tg_user = await client.get_users(user_id)
            if tg_user:
                real_user_name = tg_user.first_name or "User"
                if tg_user.last_name:
                    real_user_name += f" {tg_user.last_name}"
                await db.col.update_one({"id": int(user_id)}, {"$set": {"name": real_user_name}})
        except Exception:
            real_user_name = "User"
            
    if not real_user_name:
        real_user_name = "User"

    user_mention = f"[{real_user_name}](tg://user?id={user_id})"
    msg_chat_id = message.chat.id if message else user_id
    msg_id = message.id if message else None
    
    if user_id not in ACTIVE_PROCESSES: ACTIVE_PROCESSES[user_id] = {}
    if not task_uuid: task_uuid = uuid.uuid4().hex
    
    ACTIVE_PROCESSES[user_id][task_uuid] = {
        "user": user_mention, 
        "dest_title_name": dest_title,
        "item": text[:50]+"...", 
        "started": time.time()
    }

    if dest_chat_id is None: dest_chat_id = msg_chat_id
    if dest_thread_id is None: dest_thread_id = message.message_thread_id if message else None

    if "t.me/" in text:
        acc = None
        success_count = 0
        failed_count = 0
        skipped_count = 0
        total_count = 0
        status_message = None

        parsed_source = _parse_source_link(text)
        filter_thread_id = parsed_source.get("topic_id")
        msg_id_hint = parsed_source.get("msg_id")

        start_time = time.time()
        source_title = "Unknown Source"

        try:
            was_cancelled = False
            range_match = re.search(r"(\d+)\s*-\s*(\d+)", text)
            if range_match:
                fromID, toID = int(range_match.group(1)), int(range_match.group(2))
            elif msg_id_hint is not None:
                fromID = toID = int(msg_id_hint)
            else:
                if message: return await message.reply("❌ Invalid link format. Send a valid Telegram post link with a message ID.")
                return

            if resume_from_id:
                fromID = resume_from_id

            total_count = max(1, toID - fromID + 1)

            user_data = await db.get_session(user_id)
            acc = None
            is_temp_acc = False
            
            if user_data:
                api_id = await db.get_api_id(user_id) or API_ID
                api_hash = await db.get_api_hash(user_id) or API_HASH
                
                user_workers = 8
                
                acc = Client(
                    name=f"temp_acc_{user_id}_{uuid.uuid4().hex}", 
                    in_memory=True,
                    session_string=user_data, 
                    api_hash=api_hash, 
                    api_id=api_id, 
                    no_updates=True,
                    workers=user_workers,
                    sleep_threshold=120, # 🟢 Increased
                    ipv6=False,
                    **get_transmission_kwargs(workers=user_workers, is_bot=False) # 🟢 Force 1 concurrent
                )
                await acc.start()
                is_temp_acc = True

            try:
                source_ref = parsed_source.get("chat_id")
                if source_ref is None:
                    return await message.reply("❌ Could not resolve source chat.")

                # 🟢 CRITICAL FIX: Force User Session to cache the peer using the original Username!
                # If we skip this, acc throws PEER_ID_INVALID when given a raw integer ID later.
                if acc:
                    try: await acc.get_chat(source_ref)
                    except Exception:
                        try: await acc.resolve_peer(source_ref)
                        except Exception: pass

                # 🟢 Attempt to get the REAL name of the channel / User / Bot
                try:
                    source_chat = await client.get_chat(source_ref)
                    source_title = source_chat.title or source_chat.first_name or str(source_ref)
                    if getattr(source_chat, "last_name", None):
                        source_title += f" {source_chat.last_name}"
                    ACTUAL_CHAT_ID = source_chat.id
                except Exception:
                    if acc:
                        try:
                            source_chat = await acc.get_chat(source_ref)
                            source_title = source_chat.title or source_chat.first_name or str(source_ref)
                            if getattr(source_chat, "last_name", None):
                                source_title += f" {source_chat.last_name}"
                            ACTUAL_CHAT_ID = source_chat.id
                        except Exception:
                            # Force fallback for public strings if get_chat fails
                            ACTUAL_CHAT_ID = source_ref
                            source_title = str(source_ref)
                    else:
                        ACTUAL_CHAT_ID = source_ref
                        source_title = str(source_ref)
                        
                # 🟢 CRITICAL FIX: The User Session (acc) MUST resolve the peer ID 
                # before the loop starts, or Telegram throws PEER_ID_INVALID!
                if acc:
                    try:
                        await acc.resolve_peer(ACTUAL_CHAT_ID)
                    except Exception:
                        pass

            except Exception as e: 
                if not acc:
                    is_pub = isinstance(source_ref, str) and not str(source_ref).lstrip('-').isdigit()
                    reason = "The public username might be incorrect/banned." if is_pub else "I am not inside this private chat."
                    return await message.reply(
                        f"❌ **Could not access Source.**\n\n"
                        f"You are not logged in, and I cannot read this chat directly.\n"
                        f"💡 **Reason:** {reason}\n"
                        f"**Fix:** Please use `/login` to route through your own account, OR add me to the source chat (**as an Admin for Channels, or a normal Member for Groups**).\n\n"
                        f"**Error:** `{e}`"
                    )
                logger.warning(f"Could not fetch chat title for {source_ref}: {e}")
                ACTUAL_CHAT_ID = source_ref 

            if saved_source_title and source_title == "Unknown Source":
                source_title = saved_source_title

            t_name = ""
            if filter_thread_id:
                fetcher = acc if acc else client
                topic_addon = await get_topic_title(fetcher, ACTUAL_CHAT_ID, filter_thread_id)
                source_title += topic_addon
                t_name = topic_addon.strip(" ()")

            # --- 🟢 DESTINATION METADATA RESOLVER ---
            # If the destination is a raw ID, force the User Session to fetch the real Group/Topic name!
            if str(dest_title).lstrip("-").isdigit() or dest_title == "Target Chat":
                try:
                    d_chat = await client.get_chat(dest_chat_id)
                    dest_title = d_chat.title or d_chat.first_name or str(dest_chat_id)
                except Exception:
                    if acc:
                        try:
                            d_chat = await acc.get_chat(dest_chat_id)
                            dest_title = d_chat.title or d_chat.first_name or str(dest_chat_id)
                        except Exception:
                            pass
                
                # Fetch the exact Topic Name using the User Session
                if dest_thread_id:
                    fetcher = acc if acc else client
                    t_addon = await get_topic_title(fetcher, dest_chat_id, dest_thread_id)
                    dest_title += t_addon
                    
                # Dynamically update the Web UI so it drops the ugly ID
                if task_uuid in ACTIVE_PROCESSES.get(user_id, {}):
                    ACTIVE_PROCESSES[user_id][task_uuid]["dest_title_name"] = dest_title
            # ----------------------------------------
            
            ACTIVE_PROCESSES[user_id][task_uuid].update({"source_title": source_title, "total": total_count, "current": 0})
            
            # 🟢 [DB SAVE] Register task for Auto-Resume with the CORRECT fetched source title
            await db.add_active_task(
                task_uuid=task_uuid, user_id=user_id, link=text, dest_chat_id=dest_chat_id,
                dest_thread_id=dest_thread_id, dest_title=dest_title, delay=delay,
                is_restricted=is_restricted, allowed_types=allowed_types,
                source_title=source_title, current_msg_id=fromID, to_id=toID
            )

            # 🟢 [DETAILED LOGGING] Cleaned up to prevent double Topic IDs!
            log_user_link = f"[{real_user_name}](tg://user?id={user_id})"
            log_dst_display = f"{dest_chat_id}" + (f"/{dest_thread_id}" if dest_thread_id else "")
            
            detailed_log = (
                f"▶️ **Task Started**\n"
                f"**User:** {log_user_link} (`{user_id}`)\n"
                f"**Task:** {source_title} -> {dest_title}\n"
                f"**Link:** {text} -> `{log_dst_display}`"
            )
            await send_log(detailed_log)
            
            status_text_header = f"**Batch Task Started!** 🚀\n"
            inner_header = ""
            if filter_thread_id:
                status_text_header += f"**Filter:** `{t_name} Only` 🎯\n"
                inner_header = f"Filter: {t_name} Only 🎯"

            kwargs_status = {"chat_id": msg_chat_id}
            if msg_id: 
                kwargs_status["reply_to_message_id"] = msg_id
            if message and message.message_thread_id:
                kwargs_status["message_thread_id"] = message.message_thread_id

            status_message = await client.send_message(
                # 🟢 FIX: Update wording so users know no further TG updates will happen
                text=f"🚀 **Batch Task Started!**\n{status_text_header}\n**Source:** {source_title}\n**Destination:** {dest_title}\n**Total Items:** {total_count}\n\n🌐 **All live progress, speed, and ETA will be shown EXCLUSIVELY in the Web Dashboard.**\n*(To prevent chat spam, no progress bars will be printed here)*",
                **kwargs_status
            )
            last_update_time = time.time()
            # 🟢 Deleted the old hardcoded inner_header line here!

            all_ids = list(range(fromID, toID + 1))
            chunk_size = 100
            global_index = 1
            
            for chunk_start in range(0, len(all_ids), chunk_size):
                chunk_ids = all_ids[chunk_start : chunk_start + chunk_size]
                
                if batch_temp.IS_BATCH.get(user_id) or (task_uuid and CANCEL_FLAGS.get(task_uuid)):
                    was_cancelled = True
                    break
                
                fetcher = acc if acc else client
                chunk_messages = []
                chunk_success = False
                
                try:
                    # 🔥 THE MAGIC: Fetching 100 messages in one single API call!
                    chunk_messages = await fetcher.get_messages(ACTUAL_CHAT_ID, chunk_ids)
                    chunk_success = True
                except FloodWait as e:
                    if e.value > 300:
                        try: await status_message.edit_text(f"❌ **Task Cancelled automatically**\nReason: FloodWait too long ({e.value}s).")
                        except Exception: pass
                        was_cancelled = True
                        break
                    
                    try: 
                        if not is_restricted: await status_message.edit_text(f"⏳ **Rate Limiting Detected**\nSleeping for {e.value} seconds to catch breath...")
                    except Exception: pass
                    
                    USER_FLOOD_LOCKS[user_id].set_lock(e.value + 5)
                    await asyncio.sleep(e.value + 5)
                    
                    try: 
                        chunk_messages = await fetcher.get_messages(ACTUAL_CHAT_ID, chunk_ids)
                        chunk_success = True
                    except Exception as inner_e:
                        logger.error(f"Chunk fetch failed after FloodWait: {inner_e}")
                except Exception as e:
                    logger.error(f"Chunk fetch failed: {e}")

                # Build dictionary of valid messages to match IDs instantly
                msg_dict = {m.id: m for m in chunk_messages if m and not getattr(m, 'empty', True)}

                for msgid in chunk_ids:
                    index = global_index
                    global_index += 1
                    loop_start_time = time.time()
                    
                    # 🟢 [DB UPDATE] Tick progress so if server crashes, it resumes here
                    await db.update_task_progress(task_uuid, msgid)

                    if task_uuid in ACTIVE_PROCESSES.get(user_id, {}):
                        ACTIVE_PROCESSES[user_id][task_uuid]["current"] = index

                    if batch_temp.IS_BATCH.get(user_id) or (task_uuid and CANCEL_FLAGS.get(task_uuid)):
                        was_cancelled = True
                        break

                    # --- ALBUM SKIP LOGIC ---
                    if msgid in batch_temp.SKIP_IDS.get(task_uuid, set()):
                        success_count += 1
                        continue 
                    # ------------------------

                    # ⚡ LIGHTNING-FAST SKIP: If chunk loaded but ID isn't in it, it's deleted.
                    if chunk_success and msgid not in msg_dict:
                        skipped_count += 1
                        if task_uuid in ACTIVE_PROCESSES.get(user_id, {}):
                            ACTIVE_PROCESSES[user_id][task_uuid].update({
                                "current": index, "success": success_count,
                                "skipped": skipped_count, "failed": failed_count
                            })
                        continue

                    # Grab the pre-loaded message
                    pre_fetched_msg = msg_dict.get(msgid)
                    
                    is_success = False
                    task_result = "FAILED"
                    try:
                        chatid = ACTUAL_CHAT_ID
                        
                        # 🟢 FIX: Determine if link is a Public string username
                        is_pub = isinstance(parsed_source.get("chat_id"), str) and not str(parsed_source.get("chat_id")).lstrip('-').isdigit()
                        
                        # 🟢 FIX: Bot PMs and User PMs must NEVER use the public fast-path 
                        is_bot_or_user_pm = False
                        if "source_chat" in locals():
                            chat_type_str = str(getattr(source_chat, "type", "")).upper()
                            if "BOT" in chat_type_str or "PRIVATE" in chat_type_str:
                                is_bot_or_user_pm = True

                        if is_pub and not is_restricted and not is_bot_or_user_pm:
                            task_result = await handle_public_unrestricted(
                                client, acc, chatid, msgid, dest_chat_id, dest_thread_id, 
                                user_id, task_uuid, filter_thread_id, allowed_types, delay, pre_fetched_msg=pre_fetched_msg
                            )
                            if task_result == "FALLBACK_RESTRICTED":
                                task_result = await handle_private(
                                    client, acc, message, chatid, msgid, index, total_count, 
                                    None, dest_chat_id, dest_thread_id, delay, # 🟢 FIX: Passed None to disable TG UI updates
                                    user_id, task_uuid, 
                                    is_restricted=True, header_text=inner_header,
                                    filter_thread_id=filter_thread_id, allowed_types=allowed_types, pre_fetched_msg=pre_fetched_msg
                                )
                        else:
                            task_result = await handle_private(
                                client, acc, message, chatid, msgid, index, total_count, 
                                None, dest_chat_id, dest_thread_id, delay, # 🟢 FIX: Passed None to disable TG UI updates
                                user_id, task_uuid, 
                                is_restricted=is_restricted, header_text=inner_header,
                                filter_thread_id=filter_thread_id, allowed_types=allowed_types, pre_fetched_msg=pre_fetched_msg
                            )
                    
                    except FloodWait as e:
                        if e.value > 300:
                            print(f"FloodWait too long ({e.value}s). Stopping task.")
                            try: await status_message.edit_text(f"❌ **Task Cancelled automatically**\nReason: FloodWait too long ({e.value}s).")
                            except Exception: pass 
                            was_cancelled = True
                            break

                        try: 
                            if not is_restricted: await status_message.edit_text(f"⏳ **Rate Limiting Detected**\nSleeping for {e.value} seconds...")
                        except Exception: pass
                        
                        USER_FLOOD_LOCKS[user_id].set_lock(e.value + 5) 
                        await asyncio.sleep(e.value + 5)
                        
                    except Exception as e: 
                        logger.error(f"Error processing {msgid} for user {user_id}", exc_info=True)
                        await send_log(f"❌ **Task Error:** Message `{msgid}` failed.\nUser: `{user_id}`\nError: `{e}`")

                    # Accurately map results to Skipped vs Failed
                    if task_result == "SUCCESS" or task_result is True: 
                        success_count += 1
                        is_success = True
                    elif task_result == "SKIPPED": 
                        skipped_count += 1
                        is_success = False
                    else: 
                        failed_count += 1
                        is_success = False

                    # 🟢 [NEW] Feed live stats to Web UI!
                    if task_uuid in ACTIVE_PROCESSES.get(user_id, {}):
                        ACTIVE_PROCESSES[user_id][task_uuid].update({
                            "current": index,
                            "success": success_count,
                            "skipped": skipped_count,
                            "failed": failed_count
                        })

                    if index < total_count:
                        if is_success:
                            elapsed_time = time.time() - loop_start_time
                            actual_sleep = max(0, delay - elapsed_time)
                            await asyncio.sleep(actual_sleep)
                        else:
                            await asyncio.sleep(0.05)

                    if not is_restricted:
                        pass # Web UI handles progress, no Telegram edits needed
                
                # Break the outer chunk loop if cancelled from inside the inner loop
                if 'was_cancelled' in locals() and was_cancelled:
                    break
                    
        except Exception as e:
            await send_log(f"❌ **Task Crashed**\nUser: `{user_id}`\nError: `{e}`")

        finally:
            # 🟢 [DB DELETE] Task completed successfully or was explicitly cancelled by user
            await db.remove_active_task(task_uuid)
            
            cleanup_task_memory(user_id, task_uuid)
            batch_temp.SKIP_IDS.pop(task_uuid, None) # Clear RAM
            
            batch_temp.ACTIVE_TASKS[user_id] = max(0, batch_temp.ACTIVE_TASKS.get(user_id, 0) - 1)

            if TASK_QUEUE[user_id]:
                next_item = TASK_QUEUE[user_id].pop(0)
                asyncio.create_task(
                    start_task_final(
                        next_item["client"],
                        next_item["message"],
                        dict(next_item["data"]),
                        next_item["delay"],
                        user_id
                    )
                )

            if acc and is_temp_acc:
                try: await acc.stop()
                except: pass

            duration = time.time() - start_time
            time_taken_str = get_readable_time(int(duration))
            
            if 'was_cancelled' in locals() and was_cancelled:
                header = f"Batch was Cancelled! 🛑 {user_mention} ✨"
            else:
                header = f"Batch was Completed! ✅ {user_mention} ✨"

            final_text = (
                f"{header}\n"
                f"📝 **Task :** {source_title} → {dest_title}\n"
                f"⏱ **Time Taken:** `{time_taken_str}`\n"
                f"📊 **Statistics:**\n"
                f"├ 📥 **Total Requested:** `{total_count}`\n"
                f"├ ✅ **Successful:** `{success_count}`\n"
                f"├ ⏭ **Skipped:** `{skipped_count}`\n"
                f"└ ❌ **Failed:** `{failed_count}`"
            )
            
            # 🟢 FIX: Edit the initial static message with the final completion statistics
            try: 
                kwargs_final = {"text": final_text}
                await status_message.edit_text(**kwargs_final)
            except: 
                try:
                    kwargs_final = {"chat_id": msg_chat_id, "text": final_text}
                    if msg_id: kwargs_final["reply_to_message_id"] = msg_id
                    await client.send_message(**kwargs_final)
                except: pass
            # The status message is kept as a permanent log, so delete() is removed

# ==============================================================================
