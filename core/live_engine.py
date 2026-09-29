# ==============================================================================
# --- LIVE WATCHER ENGINE (WITH UNIVERSAL QUEUE & CATCH-UP) ---
# ==============================================================================

from pyrogram.handlers import MessageHandler

WATCHER_QUEUES = defaultdict(asyncio.Queue)
WATCHER_WORKERS = {}

async def start_watcher_worker(wid_str):
    """Ensure exactly one live worker task exists for this watcher."""
    task = WATCHER_WORKERS.get(wid_str)
    if task is None or task.done() or task.cancelled():
        WATCHER_WORKERS[wid_str] = asyncio.create_task(watcher_worker_loop(wid_str))

async def watcher_worker_loop(wid_str):
    """Process one watcher's queue serially and keep its checkpoint consistent."""
    queue = WATCHER_QUEUES[wid_str]
    while True:
        msg_id = await queue.get()
        try:
            watcher = await db.db.watchers.find_one({"_id": ObjectId(wid_str)})
            if not watcher:
                continue

            owner_id = watcher["user_id"]
            watcher_db_id = watcher["_id"]
            source_id = watcher["source_id"]
            source_thread = watcher.get("source_thread")
            dest_id = watcher["dest_id"]
            dest_thread = watcher.get("dest_thread")
            delay = max(3, min(int(watcher.get("delay", 3)), 3600))
            is_restricted = watcher.get("is_restricted", False)
            allowed_types = watcher.get("allowed_types", ["Video", "Document"])
            include_keywords = watcher.get("include_keywords", [])
            exclude_keywords = watcher.get("exclude_keywords", [])

            # Prefer the owner's connected user session for sources it can access;
            # otherwise use the bot. This is only an access-selection fallback.
            owner_client = USER_CLIENTS.get(owner_id)
            fetcher = owner_client if (owner_client and owner_client.is_connected) else app

            try:
                msg = await fetcher.get_messages(source_id, msg_id)
            except Exception as fetch_err:
                logger.warning(f"Watcher {wid_str}: could not fetch {source_id}/{msg_id}: {fetch_err}")
                msg = None

            # Never advance the checkpoint merely because an ID was dequeued.
            # Missing/deleted/inaccessible IDs can safely be considered skipped.
            if not msg or msg.empty:
                log_file_result("watcher", owner_id, wid_str, source_id, msg_id, media_filename(None, msg_id), "SKIPPED", "source message missing or inaccessible")
                await db.db.watchers.update_one(
                    {"_id": watcher_db_id},
                    {"$max": {"last_msg_id": int(msg_id)}, "$inc": {"stats.skipped": 1}}
                )
                continue

            msg_type = get_message_type(msg)
            if not msg_type:
                log_file_result("watcher", owner_id, wid_str, source_id, msg.id, media_filename(msg, msg.id), "SKIPPED", "unsupported or non-media message type")
                await db.db.watchers.update_one(
                    {"_id": watcher_db_id},
                    {"$max": {"last_msg_id": int(msg.id)}, "$inc": {"stats.skipped": 1}}
                )
                continue

            is_content_protected = (
                getattr(msg, "has_protected_content", False)
                or getattr(msg.chat, "has_protected_content", False)
            )

            await db.db.watchers.update_one(
                {"_id": watcher_db_id}, {"$inc": {"stats.detected": 1}}
            )

            if msg_type not in allowed_types:
                log_file_result("watcher", owner_id, wid_str, source_id, msg.id, media_filename(msg, msg.id), "SKIPPED", f"media type excluded by task filter: {msg_type}")
                await db.db.watchers.update_one(
                    {"_id": watcher_db_id},
                    {"$max": {"last_msg_id": int(msg.id)}, "$inc": {"stats.skipped": 1}}
                )
                continue

            if not filename_matches_filters(msg, include_keywords, exclude_keywords):
                log_file_result("watcher", owner_id, wid_str, source_id, msg.id, media_filename(msg, msg.id), "SKIPPED", "filename rejected by include/exclude keyword filters")
                await db.db.watchers.update_one(
                    {"_id": watcher_db_id},
                    {"$max": {"last_msg_id": int(msg.id)}, "$inc": {"stats.skipped": 1}}
                )
                continue

            # Canonical source-topic check. Telegram forum messages expose the
            # thread through message_thread_id; reply fields are only fallbacks
            # for clients/older message objects.
            if source_thread is not None:
                actual_thread = getattr(msg, "message_thread_id", None)
                if actual_thread is None:
                    actual_thread = getattr(msg, "reply_to_top_message_id", None)
                if actual_thread is None:
                    actual_thread = getattr(msg, "reply_to_message_id", None)

                # A topic service message can itself have the topic root ID.
                if actual_thread is None and getattr(msg, "id", None) == int(source_thread):
                    actual_thread = int(source_thread)

                if actual_thread != int(source_thread):
                    log_file_result("watcher", owner_id, wid_str, source_id, msg.id, media_filename(msg, msg.id), "SKIPPED", f"topic filter mismatch: expected {source_thread}, got {actual_thread}")
                    await db.db.watchers.update_one(
                        {"_id": watcher_db_id},
                        {"$max": {"last_msg_id": int(msg.id)}, "$inc": {"stats.skipped": 1}}
                    )
                    continue

            if delay > 0:
                await asyncio.sleep(delay)

            processed_successfully = False

            # 🟢 Determine Uploader early so we can show it in the UI even if restricted
            upload_client = app
            worker_bots = USER_TASK_BOTS.get(owner_id, [])
            if worker_bots:
                connected_workers = [wb for wb in worker_bots if getattr(wb, "is_connected", False)]
                if connected_workers:
                    upload_client = connected_workers[int(time.time()) % len(connected_workers)]

            # 🟢 Inject fetcher/uploader into DB for UI rendering
            await db.db.watchers.update_one(
                {"_id": watcher_db_id},
                {"$set": {"fetcher": _get_client_label(fetcher), "uploader": _get_client_label(upload_client)}}
            )

            if not is_restricted and not is_content_protected and not (watcher.get("thumb_file_id") or watcher.get("thumb_b64")):
                if getattr(msg, "media_group_id", None):
                    group_cache_key = f"{owner_id}_{source_id}_{msg.media_group_id}_{dest_id}_{dest_thread}"
                    if WATCHER_MEDIA_GROUPS.get(group_cache_key):
                        log_file_result("watcher", owner_id, wid_str, source_id, msg.id, media_filename(msg, msg.id), "SKIPPED", "duplicate member of an already processed media group")
                        await db.db.watchers.update_one(
                            {"_id": watcher_db_id},
                            {"$max": {"last_msg_id": int(msg.id)}}
                        )
                        continue
                    WATCHER_MEDIA_GROUPS[group_cache_key] = True

                    try:
                        await USER_FLOOD_LOCKS[owner_id].wait_if_locked()
                        try:
                            m_group = await fetcher.get_media_group(source_id, msg.id)
                        except Exception:
                            m_group = [msg]
                        group_size = len(m_group)

                        try:
                            copy_res = await safe_send(
                                upload_client, owner_id, dest_id, None, True,
                                upload_client.copy_media_group,
                                chat_id=dest_id,
                                from_chat_id=source_id,
                                message_id=msg.id,
                                message_thread_id=dest_thread
                            )
                        except Exception:
                            if owner_client and owner_client.is_connected:
                                # 🟢 FIX: Update the DB so Web UI shows the fallback Uploader!
                                await db.db.watchers.update_one({"_id": watcher_db_id}, {"$set": {"uploader": _get_client_label(owner_client)}})
                                
                                copy_res = await safe_send(
                                    owner_client, owner_id, dest_id, None, False,
                                    owner_client.copy_media_group,
                                    chat_id=dest_id,
                                    from_chat_id=source_id,
                                    message_id=msg.id,
                                    message_thread_id=dest_thread
                                )
                            else:
                                copy_res = False

                        if copy_res:
                            processed_successfully = True
                            if delay > 0 and group_size > 1:
                                await asyncio.sleep(delay * (group_size - 1))
                    except FloodWait as e:
                        USER_FLOOD_LOCKS[owner_id].set_lock(e.value + 5)
                        await asyncio.sleep(e.value + 5)
                        try:
                            if owner_client and owner_client.is_connected:
                                # 🟢 FIX: Update UI on FloodWait retry fallback
                                await db.db.watchers.update_one({"_id": watcher_db_id}, {"$set": {"uploader": _get_client_label(owner_client)}})
                                
                                copy_res = await safe_send(
                                    owner_client, owner_id, dest_id, None, False,
                                    owner_client.copy_media_group,
                                    chat_id=dest_id, from_chat_id=source_id,
                                    message_id=msg.id, message_thread_id=dest_thread
                                )
                                processed_successfully = bool(copy_res)
                        except Exception as retry_err:
                            logger.warning(
                                "FILE_ATTEMPT scope=watcher user_id=%s task_id=%s source_id=%s message_id=%s file=%r stage=fast-copy-retry reason=%r",
                                owner_id, wid_str, source_id, msg.id, media_filename(msg, msg.id),
                                f"{type(retry_err).__name__}: {retry_err}",
                            )
                    except Exception as e:
                        logger.warning(
                            "FILE_ATTEMPT scope=watcher user_id=%s task_id=%s source_id=%s message_id=%s file=%r stage=fast-copy reason=%r; trying download/upload path",
                            owner_id, wid_str, source_id, msg.id, media_filename(msg, msg.id),
                            f"{type(e).__name__}: {e}",
                        )

                else:
                    try:
                        await USER_FLOOD_LOCKS[owner_id].wait_if_locked()
                        try:
                            copy_res = await safe_send(
                                upload_client, owner_id, dest_id, None, True,
                                upload_client.copy_message,
                                chat_id=dest_id,
                                from_chat_id=source_id,
                                message_id=msg.id,
                                message_thread_id=dest_thread
                            )
                        except Exception:
                            if owner_client and owner_client.is_connected:
                                # 🟢 FIX: Update the DB so Web UI shows the fallback Uploader!
                                await db.db.watchers.update_one({"_id": watcher_db_id}, {"$set": {"uploader": _get_client_label(owner_client)}})
                                
                                copy_res = await safe_send(
                                    owner_client, owner_id, dest_id, None, False,
                                    owner_client.copy_message,
                                    chat_id=dest_id,
                                    from_chat_id=source_id,
                                    message_id=msg.id,
                                    message_thread_id=dest_thread
                                )
                            else:
                                copy_res = False
                        if copy_res:
                            processed_successfully = True

                    except FloodWait as e:
                        USER_FLOOD_LOCKS[owner_id].set_lock(e.value + 5)
                        await asyncio.sleep(e.value + 5)
                        try:
                            if owner_client and owner_client.is_connected:
                                # 🟢 FIX: Update UI on FloodWait retry fallback
                                await db.db.watchers.update_one({"_id": watcher_db_id}, {"$set": {"uploader": _get_client_label(owner_client)}})
                                
                                copy_res = await safe_send(
                                    owner_client, owner_id, dest_id, None, False,
                                    owner_client.copy_message,
                                    chat_id=dest_id, from_chat_id=source_id,
                                    message_id=msg.id, message_thread_id=dest_thread
                                )
                                processed_successfully = bool(copy_res)
                        except Exception as retry_err:
                            logger.warning(
                                "FILE_ATTEMPT scope=watcher user_id=%s task_id=%s source_id=%s message_id=%s file=%r stage=fast-copy-retry reason=%r",
                                owner_id, wid_str, source_id, msg.id, media_filename(msg, msg.id),
                                f"{type(retry_err).__name__}: {retry_err}",
                            )
                    except Exception as e:
                        logger.warning(
                            "FILE_ATTEMPT scope=watcher user_id=%s task_id=%s source_id=%s message_id=%s file=%r stage=fast-copy reason=%r; trying download/upload path",
                            owner_id, wid_str, source_id, msg.id, media_filename(msg, msg.id),
                            f"{type(e).__name__}: {e}",
                        )

            if processed_successfully:
                log_file_result("watcher", owner_id, wid_str, source_id, msg.id, media_filename(msg, msg.id), "SUCCESS")
                await db.db.watchers.update_one(
                    {"_id": watcher_db_id},
                    {"$max": {"last_msg_id": int(msg.id)}, "$inc": {"stats.success": 1}}
                )
                continue

            # Existing heavy-processing path. No new protected-content bypass is
            # introduced here; it uses the file's existing implementation.
            try:
                # 🟢 FIX: Removed dummy_status creation so watchers operate 100% silently in TG
                task_uuid = uuid.uuid4().hex
                if owner_id not in ACTIVE_PROCESSES:
                    ACTIVE_PROCESSES[owner_id] = {}
                ACTIVE_PROCESSES[owner_id][task_uuid] = {
                    "user": "Watcher",
                    "dest_title_name": watcher.get("dest_title", "Destination"),
                    "source_title": watcher.get("source_title", "Source"),
                    "item": f"Live Watcher ID: {msg.id}",
                    "started": time.time(),
                    "is_watcher": True,
                    "source_id": source_id,
                    "include_keywords": include_keywords,
                    "exclude_keywords": exclude_keywords,
                    "thumb_file_id": watcher.get("thumb_file_id"),
                    "thumb_b64": watcher.get("thumb_b64"),
                }

                result_reason = None
                try:
                    result = await handle_private(
                        client=app,
                        acc=owner_client,
                        message=msg,
                        chatid=source_id,
                        msgid=msg.id,
                        index=1,
                        total_count=1,
                        status_message=None, # 🟢 FIX: Passed None to disable TG UI updates
                        dest_chat_id=dest_id,
                        dest_thread_id=dest_thread,
                        delay=0,
                        user_id=owner_id,
                        task_uuid=task_uuid,
                        is_restricted=True,
                        allowed_types=allowed_types
                    )
                finally:
                    result_reason = ACTIVE_PROCESSES.get(owner_id, {}).get(task_uuid, {}).get("last_result_reason")
                    cleanup_task_memory(owner_id, task_uuid)

                if result == "SUCCESS" or result is True:
                    log_file_result("watcher", owner_id, wid_str, source_id, msg.id, media_filename(msg, msg.id), "SUCCESS")
                    await db.db.watchers.update_one(
                        {"_id": watcher_db_id},
                        {"$max": {"last_msg_id": int(msg.id)}, "$inc": {"stats.success": 1}}
                    )
                elif result == "SKIPPED":
                    log_file_result("watcher", owner_id, wid_str, source_id, msg.id, media_filename(msg, msg.id), "SKIPPED", result_reason or "message was filtered or unavailable")
                    await db.db.watchers.update_one(
                        {"_id": watcher_db_id},
                        {"$max": {"last_msg_id": int(msg.id)}, "$inc": {"stats.skipped": 1}}
                    )
                else:
                    log_file_result("watcher", owner_id, wid_str, source_id, msg.id, media_filename(msg, msg.id), "FAILED", result_reason or f"processor returned {result!r}; see preceding task logs")
                    await db.db.watchers.update_one(
                        {"_id": watcher_db_id},
                        {"$max": {"last_msg_id": int(msg.id)}, "$inc": {"stats.failed": 1}}
                    )
            except Exception as e:
                log_file_result("watcher", owner_id, wid_str, source_id, msg.id, media_filename(msg, msg.id), "FAILED", f"{type(e).__name__}: {e}")
                logger.error(f"Watcher {wid_str} failed for user {owner_id}, message {msg.id}: {e}", exc_info=True)
                await db.db.watchers.update_one(
                    {"_id": watcher_db_id},
                    {"$max": {"last_msg_id": int(msg.id)}, "$inc": {"stats.failed": 1}}
                )

        except Exception as outer_e:
            logger.error(f"Fatal error in watcher worker {wid_str}: {outer_e}", exc_info=True)
        finally:
            queue.task_done()

async def process_watcher_message(client, message):
    chat_id = message.chat.id
    
    # 👇 NEW: INSTANT EVENT LOOP RELIEF
    if chat_id not in GLOBAL_WATCHER_SOURCES:
        return

    topic_id = getattr(message, "message_thread_id", None)
    if topic_id is None:
        topic_id = getattr(message, "reply_to_top_message_id", None)
    if topic_id is None:
        topic_id = getattr(message, "reply_to_message_id", None)

    cursor = await db.get_watchers_for_source(chat_id, topic_id)
    watchers = await cursor.to_list(length=100)

    # 🟢 FIX: Always merge global chat watchers (source_thread = None)
    # This prevents the bot from ignoring messages inside topics when the whole group is watched.
    if topic_id is not None:
        cursor_global = await db.get_watchers_for_source(chat_id, None)
        watchers.extend(await cursor_global.to_list(length=100))

    # 🟢 Live Listener ONLY pushes IDs to the queue now!
    # Use a bounded recent-event cache rather than remembering only the last
    # event. Bot/user updates can arrive interleaved, so a one-entry cache can
    # still enqueue the same message twice.
    for w in watchers:
        wid = str(w["_id"])

        dedupe_key = (message.chat.id, topic_id, message.id)

        cache = WATCHER_DEDUPE_CACHE[wid]
        if dedupe_key in cache:
            cache.move_to_end(dedupe_key)
            continue
        cache[dedupe_key] = time.time()
        while len(cache) > WATCHER_DEDUPE_LIMIT:
            cache.popitem(last=False)

        await WATCHER_QUEUES[wid].put(message.id)
        await start_watcher_worker(wid)

async def user_watcher_handler(client, message):
    # 🟢 FIX: Wrap in create_task so it returns instantly and frees up the Pyrogram queue!
    asyncio.create_task(process_watcher_message(client, message))

# ==============================================================================
