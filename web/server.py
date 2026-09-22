# ==============================================================================
# --- FULL-STACK STREMIO WEB ENGINE & AUTHENTICATION BRIDGE ---
# ==============================================================================
try:
    from aiohttp import web
except ImportError:
    web = None

HTML_DASHBOARD = (BASE_DIR / "web" / "templates" / "dashboard.html").read_text(encoding="utf-8")
async def _dashboard_ui_handler(request):
    return web.Response(text=HTML_DASHBOARD, content_type='text/html', status=200)

async def _api_login_handler(request):
    try:
        data = await request.json()
        user_id = int(data.get("user_id"))
        password = data.get("password")
        
        if not await db.is_user_approved(user_id):
            return web.json_response({"status": "error", "message": "⛔ Unauthorized: You are not allowed to access this dashboard."})
            
        user = await db.col.find_one({"id": user_id})
        if not user:
            return web.json_response({"status": "error", "message": "Account not found! Please go to Telegram and send /start to the bot first."})

        stored_pwd = user.get("web_password")
        if not stored_pwd or stored_pwd == password:
            import secrets
            # 🟢 FIX: Generate a secure session token
            web_token = secrets.token_hex(16)
            
            update_data = {"web_token": web_token}
            if not stored_pwd:
                update_data["web_password"] = password
                
            await db.col.update_one({"id": user_id}, {"$set": update_data})
            return web.json_response({"status": "success", "token": web_token})
        else:
            return web.json_response({"status": "error", "message": "Incorrect password!"})
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)}, status=400)

async def _api_forgot_password_handler(request):
    try:
        data = await request.json()
        user_id = int(data.get("user_id"))
        
        user = await db.col.find_one({"id": user_id})
        if not user:
            return web.json_response({"status": "error", "message": "Account not found! Please send /start to the bot in Telegram."})
            
        stored_pwd = user.get("web_password")
        if not stored_pwd:
            return web.json_response({"status": "error", "message": "You haven't set a web password yet. Just enter a new password to register!"})
            
        try:
            await app.send_message(
                chat_id=user_id,
                text=f"🔐 **Web Portal Password Recovery**\n\nYour current web dashboard password is: `{stored_pwd}`\n\n_If you did not request this, please change your password in the dashboard settings._"
            )
            return web.json_response({"status": "success", "message": "Your password has been sent to your Telegram PM!"})
        except Exception as e:
            return web.json_response({"status": "error", "message": "Failed to send PM. Please ensure you have started the bot in Telegram and haven't blocked it!"})
            
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)}, status=400)

async def _api_password_handler(request):
    try:
        data = await request.json()
        user_id = int(data.get("user_id"))
        password = data.get("password")
        await db.col.update_one({"id": user_id}, {"$set": {"web_password": password}})
        return web.json_response({"status": "success"})
    except Exception:
        return web.json_response({"status": "error"}, status=400)

async def _api_stats_handler(request):
    try:
        user_id = int(request.query.get("user_id", 0))
    except:
        user_id = 0

    # 🟢 TOKEN CHECK
    token = request.query.get("token", "")
    user_doc = await db.col.find_one({"id": user_id})
    if not user_doc or user_doc.get("web_token") != token:
        return web.json_response({"status": "error", "message": "Unauthorized: Invalid or expired Web Token."})

    uptime_seconds = int(time.time() - BOT_START_TIME)
    days, rem = divmod(uptime_seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)
    uptime_str = f"{days}d, {hours:02d}h: {minutes:02d}m" if days > 0 else f"{hours:02d}h: {minutes:02d}m"
    
    # User-specific tasks
    user_tasks = ACTIVE_PROCESSES.get(user_id, {})
    task_details = []
    for t_id, info in user_tasks.items():
        tot = info.get("total", 0)
        curr = info.get("current", 0)
        
        prog_down = PROGRESS.get(f"{t_id}:down")
        prog_up = PROGRESS.get(f"{t_id}:up")
        
        phase = "Processing"
        speed = 0
        eta = 0
        file_current = 0
        file_total = 0
        percent = 0.0

        if prog_up and prog_up["current"] > 0 and prog_up["current"] < prog_up["total"]:
            phase = "Uploading"
            speed = prog_up["speed"]
            eta = prog_up["eta"]
            file_current = prog_up["current"]
            file_total = prog_up["total"]
            percent = prog_up.get("percent", 0.0)
        elif prog_down and prog_down["current"] > 0 and prog_down["current"] < prog_down["total"]:
            phase = "Downloading"
            speed = prog_down["speed"]
            eta = prog_down["eta"]
            file_current = prog_down["current"]
            file_total = prog_down["total"]
            percent = prog_down.get("percent", 0.0)
        else:
            if tot > 0:
                percent = (curr / tot * 100)

        src_name = info.get("source_title")
        if not src_name or src_name == "Unknown Source":
            src_name = info.get("item", "Task")
            
        task_details.append({
            "id": t_id,
            "name": src_name,
            "dest": info.get("dest_title_name", "DM"),
            "batch_current": curr,
            "batch_total": tot,
            "phase": phase,
            "speed": speed,
            "eta": eta,
            "file_current": file_current,
            "file_total": file_total,
            "percent": percent,
            "success": info.get("success", 0),
            "skipped": info.get("skipped", 0),
            "failed": info.get("failed", 0),
            "current_file": info.get("current_file", ""),
            "fetcher": info.get("fetcher", "🤖 Unknown"),
            "uploader": info.get("uploader", "🤖 Unknown")
        })

    # User-specific watchers
    watcher_cursor = db.db.watchers.find({"user_id": user_id})
    watcher_details = []
    async for w in watcher_cursor:
        stats = w.get("stats", {})
        watcher_details.append({
            "id": str(w["_id"]),
            "source": w.get("source_title", "Source"),
            "dest": w.get("dest_title", "Destination"),
            "detected": stats.get("detected", 0),
            "success": stats.get("success", 0),
            "skipped": stats.get("skipped", 0),
            "failed": stats.get("failed", 0),
            "fetcher": w.get("fetcher", "⏳ Waiting..."),
            "uploader": w.get("uploader", "⏳ Waiting...")
        })

    total_watchers = await db.db.watchers.count_documents({"user_id": user_id})
    
    # Check if user session exists in DB
    user_doc = await db.col.find_one({"id": user_id})
    tg_session_active = bool(user_doc and user_doc.get("session"))
    user_name = user_doc.get("name", "User") if user_doc else "User"
    is_admin = await db.is_user_admin(user_id)

    return web.json_response({
        "uptime": uptime_str,
        "user_name": user_name,
        "is_admin": is_admin,
        "ram": psutil.virtual_memory().percent,
        "cpu": psutil.cpu_percent(),
        "active_tasks": len(user_tasks),
        "active_watchers": total_watchers,
        "tg_session_active": tg_session_active,
        "tasks": task_details,
        "watchers": watcher_details
    })

async def _api_add_task(request):
    try:
        data = await request.json()
        user_id = int(data.get("user_id"))
        
        # 1. 🟢 EXTRACT TOKEN FROM JSON BODY
        token = data.get("token", "") 
        
        # 2. 🟢 VERIFY TOKEN AGAINST DATABASE
        user_doc = await db.col.find_one({"id": user_id})
        if not user_doc or user_doc.get("web_token") != token:
            return web.json_response({"status": "error", "message": "Unauthorized: Invalid or expired Web Token. Please logout and login again."})

        # 3. Proceed with the rest of the code normally
        link = data.get("link")
        dest_str = data.get("dest", "")
        delay = max(3, min(int(data.get("delay", 3)), 3600))
        allowed_types = data.get("filters", ["Video", "Document"])
        if not isinstance(allowed_types, list):
            allowed_types = ["Video", "Document"]
        allowed_types = [t for t in allowed_types if t in ALL_MSG_TYPES]

        if not link: return web.json_response({"status": "error", "message": "No link provided"})

        dest_chat_id = user_id
        dest_thread_id = None
        dest_title = "Saved Messages"
        
        if dest_str:
            dest_chat_id, dest_thread_id = _parse_chat_target(dest_str)
            uclient = USER_CLIENTS.get(user_id, app)
            try:
                d_chat = await uclient.get_chat(dest_chat_id)
                dest_title = d_chat.title or d_chat.first_name or str(dest_chat_id)
                if dest_thread_id: 
                    dest_title += await get_topic_title(uclient, dest_chat_id, dest_thread_id)
            except:
                dest_title = str(dest_chat_id)

        # 🟢 NEW: Check Worker Bots access and warn via PM if missing!
        worker_bots = USER_TASK_BOTS.get(user_id, [])
        is_dm = str(dest_chat_id).lstrip("-").isdigit() and not str(dest_chat_id).startswith("-100") and int(dest_chat_id) > 0
        if worker_bots and not is_dm:
            has_worker_access = False
            for wb in worker_bots:
                try:
                    if not getattr(wb, "is_connected", False): await wb.connect()
                    wb_member = await wb.get_chat_member(dest_chat_id, "me")
                    if wb_member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
                        has_worker_access = True
                        break
                except Exception: pass
            if not has_worker_access:
                try: await app.send_message(user_id, f"⚠️ **Worker Bot Warning:** You just started a Batch Task to `{dest_title}` via the Web UI, but your Worker Bots are not Admins there!\n\nI will fallback to your User Session. Add your worker bots as Admins for maximum speed.")
                except Exception: pass

        if not await check_disk_space():
            return web.json_response({"status": "error", "message": "Server disk is almost full (<500MB). Please wait."})

        if user_id not in ADMINS and batch_temp.ACTIVE_TASKS[user_id] >= MAX_CONCURRENT_TASKS_PER_USER:
            return web.json_response({"status": "error", "message": f"Task limit reached ({MAX_CONCURRENT_TASKS_PER_USER} max). Wait for existing tasks to finish."})

        is_restricted, _ = await check_link_restriction(user_id, link)
        if is_restricted is None: is_restricted = False

        task_uuid = uuid.uuid4().hex
        batch_temp.ACTIVE_TASKS[user_id] += 1
        batch_temp.IS_BATCH[user_id] = False

        if user_id not in ACTIVE_PROCESSES: ACTIVE_PROCESSES[user_id] = {}
        ACTIVE_PROCESSES[user_id][task_uuid] = {
            "user": f"WebUI({user_id})",
            "dest_title_name": dest_title,
            "item": link,
            "started": time.time(),
            "total": 0,
            "current": 0
        }

        asyncio.create_task(
            process_links_logic(
                client=app,
                message=None,
                text=link,
                dest_chat_id=dest_chat_id,
                dest_thread_id=dest_thread_id,
                dest_title=dest_title,
                delay=delay,
                acc_user_id=user_id,
                task_uuid=task_uuid,
                is_restricted=is_restricted,
                allowed_types=allowed_types
            )
        )
        return web.json_response({"status": "success"})
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)}, status=500)

async def _api_cancel_task(request):
    try:
        data = await request.json()
        task_id = data.get("task_id")
        user_id = int(data.get("user_id", 0))
        if task_id:
            CANCEL_FLAGS[task_id] = True
            try: await db.remove_active_task(task_id)
            except: pass
            return web.json_response({"status": "success"})
    except: pass
    return web.json_response({"status": "error"}, status=400)

async def _api_add_watcher(request):
    try:
        data = await request.json()
        user_id = int(data.get("user_id"))
        link = data.get("link")
        dest_str = data.get("dest", "")
        delay = max(3, min(int(data.get("delay", 3)), 3600))
        allowed_types = data.get("filters", ["Video", "Document"])
        if not isinstance(allowed_types, list):
            allowed_types = ["Video", "Document"]
        allowed_types = [t for t in allowed_types if t in ALL_MSG_TYPES]

        dest_chat_id = user_id
        dest_thread_id = None
        if dest_str:
            dest_chat_id, dest_thread_id = _parse_chat_target(dest_str)

        is_restricted, _ = await check_link_restriction(user_id, link)
        if is_restricted is None: is_restricted = False

        parsed = _parse_source_link(link)
        source_thread = parsed.get("topic_id")
        
        user_client = USER_CLIENTS.get(user_id, app)
        try:
            if parsed["kind"] == "public":
                try: await user_client.resolve_peer(parsed["join_target"])
                except Exception: pass
                chat = await user_client.get_chat(parsed["join_target"])
            else:
                try: await user_client.resolve_peer(parsed["chat_id"])
                except Exception: pass
                chat = await user_client.get_chat(parsed["chat_id"])
            source_id = chat.id
            source_title = chat.title or str(source_id)
            if parsed.get("topic_id"): 
                source_title += await get_topic_title(user_client, source_id, parsed["topic_id"])
        except Exception:
            source_id = parsed.get("chat_id")
            source_title = "Watched Source"
            
        dest_title = "Saved Messages" if dest_chat_id == user_id else str(dest_chat_id)
        if dest_chat_id != user_id:
            try:
                try: await user_client.resolve_peer(dest_chat_id)
                except Exception: pass
                d_chat = await user_client.get_chat(dest_chat_id)
                dest_title = d_chat.title or d_chat.first_name or str(dest_chat_id)
                if dest_thread_id: 
                    dest_title += await get_topic_title(user_client, dest_chat_id, dest_thread_id)
            except: pass

        # 🟢 NEW: Check Worker Bots access and warn via PM if missing!
        worker_bots = USER_TASK_BOTS.get(user_id, [])
        is_dm = str(dest_chat_id).lstrip("-").isdigit() and not str(dest_chat_id).startswith("-100") and int(dest_chat_id) > 0
        if worker_bots and not is_dm:
            has_worker_access = False
            for wb in worker_bots:
                try:
                    if not getattr(wb, "is_connected", False): await wb.connect()
                    wb_member = await wb.get_chat_member(dest_chat_id, "me")
                    if wb_member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
                        has_worker_access = True
                        break
                except Exception: pass
            if not has_worker_access:
                try: await app.send_message(user_id, f"⚠️ **Worker Bot Warning:** You just started a Live Watcher to `{dest_title}` via the Web UI, but your Worker Bots are not Admins there!\n\nI will fallback to your User Session. Add your worker bots as Admins for maximum forwarding speed.")
                except Exception: pass

        if user_id not in USER_CLIENTS:
            user_session = await db.get_session(user_id)
            if user_session:
                u_api = await db.get_api_id(user_id) or API_ID
                u_hash = await db.get_api_hash(user_id) or API_HASH
                new_client = Client(f"User_{user_id}", session_string=user_session, api_id=u_api, api_hash=u_hash, workers=4, ipv6=False)
                new_client.add_handler(MessageHandler(user_watcher_handler, is_watched_chat))
                await new_client.start()
                USER_CLIENTS[user_id] = new_client

        last_msg_id = 0
        try:
            async for m in USER_CLIENTS.get(user_id, app).get_chat_history(source_id, limit=1):
                last_msg_id = m.id
        except: pass

        await db.add_watcher(
            user_id=user_id,
            source_id=source_id,
            dest_id=dest_chat_id,
            source_thread=source_thread,
            dest_thread=dest_thread_id,
            delay=delay,
            is_restricted=is_restricted,
            source_title=source_title,
            dest_title=dest_title,
            allowed_types=allowed_types,
            last_msg_id=last_msg_id
        )
        GLOBAL_WATCHER_SOURCES.add(source_id) # 🟢 UPDATE CACHE
        return web.json_response({"status": "success"})
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)}, status=500)

async def _api_cancel_watcher(request):
    try:
        data = await request.json()
        watcher_id = data.get("watcher_id")
        user_id = int(data.get("user_id", 0))
        if watcher_id:
            await db.db.watchers.delete_one({"_id": ObjectId(watcher_id), "user_id": user_id})
            return web.json_response({"status": "success"})
    except: pass
    return web.json_response({"status": "error"}, status=400)

def _read_logs_sync():
    """Reads logs safely in a background thread so the server doesn't freeze."""
    if not os.path.exists("bot.log"): return "Log file not created yet."
    with open("bot.log", "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    return "".join(lines[-150:])

async def _api_logs_handler(request):
    try:
        uid = int(request.query.get("user_id", 0))
    except:
        uid = 0
        
    # 🟢 TOKEN CHECK
    token = request.query.get("token", "")
    user_doc = await db.col.find_one({"id": uid})
    if not user_doc or user_doc.get("web_token") != token:
        return web.json_response({"logs": "⚠️ Unauthorized: Invalid or expired Web Token. Please log in again."})
        
    if uid not in ADMINS and uid not in SUDOS:
        return web.json_response({"logs": "⚠️ ACCESS DENIED: You must be a Bot Admin to view server logs."})
        
    try:
        logs = await asyncio.to_thread(_read_logs_sync)
        return web.json_response({"logs": logs})
    except Exception as e:
        return web.json_response({"logs": f"Error reading logs: {e}"})

async def _api_download_log_handler(request):
    try:
        uid = int(request.query.get("user_id", 0))
    except:
        uid = 0
        
    if uid not in ADMINS and uid not in SUDOS:
        return web.Response(text="ACCESS DENIED: Admins Only", status=403)
        
    try:
        if os.path.exists("bot.log"):
            return web.FileResponse("bot.log", headers={"Content-Disposition": "attachment; filename=bot.log"})
        return web.Response(text="Log file not found.", status=404)
    except Exception:
        return web.Response(text="Error downloading logs.", status=500)

WEB_AUTH_CACHE = {}

async def _api_tg_send_code(request):
    data = await request.json()
    uid = int(data.get("user_id"))
    phone = data.get("phone")
    
    client = Client(f"web_auth_{uid}_{uuid.uuid4().hex}", in_memory=True, api_id=API_ID, api_hash=API_HASH)
    await client.connect()
    try:
        code = await client.send_code(phone)
        WEB_AUTH_CACHE[uid] = {"client": client, "phone": phone, "hash": code.phone_code_hash}
        return web.json_response({"status": "success"})
    except Exception as e:
        await client.disconnect()
        return web.json_response({"status": "error", "message": str(e)})

async def _api_tg_verify_code(request):
    data = await request.json()
    uid = int(data.get("user_id"))
    code = data.get("code")
    
    cache = WEB_AUTH_CACHE.get(uid)
    if not cache: return web.json_response({"status": "error", "message": "Session expired. Try again."})
    
    client = cache["client"]
    try:
        await client.sign_in(cache["phone"], cache["hash"], code)
        
        # 🟢 ENFORCE ID MATCH: Prevent cross-account chat leaks!
        me = await client.get_me()
        if me.id != uid:
            await client.disconnect()
            del WEB_AUTH_CACHE[uid]
            return web.json_response({"status": "error", "message": f"⚠️ ID Mismatch! You logged into the Web UI as {uid}, but this phone number belongs to {me.id}. Please use your own Telegram account."})
            
        session_str = await client.export_session_string()
        await client.disconnect()
        del WEB_AUTH_CACHE[uid]
        
        await db.set_session(uid, session_str)
        await db.set_api_id(uid, API_ID)
        await db.set_api_hash(uid, API_HASH)
        return web.json_response({"status": "success"})
        
    except SessionPasswordNeeded:
        return web.json_response({"status": "2fa_required"})
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)})

async def _api_tg_verify_2fa(request):
    data = await request.json()
    uid = int(data.get("user_id"))
    pwd = data.get("password")
    
    cache = WEB_AUTH_CACHE.get(uid)
    if not cache: return web.json_response({"status": "error", "message": "Session expired."})
    
    client = cache["client"]
    try:
        await client.check_password(pwd)
        
        # 🟢 ENFORCE ID MATCH: Prevent cross-account chat leaks!
        me = await client.get_me()
        if me.id != uid:
            await client.disconnect()
            del WEB_AUTH_CACHE[uid]
            return web.json_response({"status": "error", "message": f"⚠️ ID Mismatch! You logged into the Web UI as {uid}, but this phone number belongs to {me.id}. Please use your own Telegram account."})
            
        session_str = await client.export_session_string()
        await client.disconnect()
        del WEB_AUTH_CACHE[uid]
        
        await db.set_session(uid, session_str)
        await db.set_api_id(uid, API_ID)
        await db.set_api_hash(uid, API_HASH)
        return web.json_response({"status": "success"})
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)})

async def _api_tg_logout(request):
    data = await request.json()
    uid = int(data.get("user_id", 0))
    
    uclient = USER_CLIENTS.pop(uid, None)
    if uclient:
        try: await uclient.log_out()
        except: pass
        try: await uclient.stop()
        except: pass
        
    await db.set_session(uid, None)
    await db.set_api_id(uid, None)
    await db.set_api_hash(uid, None)
    
    user_tasks = list(ACTIVE_PROCESSES.get(uid, {}).keys())
    for tid in user_tasks: CANCEL_FLAGS[tid] = True
    batch_temp.IS_BATCH[uid] = True
    try: await db.db.active_tasks.delete_many({"user_id": uid})
    except: pass
    
    return web.json_response({"status": "success"})

async def _api_chats_handler(request):
    uid = int(request.query.get("user_id", 0))
    
    # 🟢 TOKEN CHECK
    token = request.query.get("token", "")
    user_doc = await db.col.find_one({"id": uid})
    if not user_doc or user_doc.get("web_token") != token:
        return web.json_response({"status": "error", "message": "Unauthorized: Invalid or expired Web Token."})
        
    session_str = await db.get_session(uid)
    
    if not session_str:
        return web.json_response({"status": "error", "message": "Not connected to Telegram. Please login."})

    uclient = USER_CLIENTS.get(uid)
    
    # 🟢 DYNAMIC WAKE-UP: Keep the main user session alive so we don't lose Access Hashes!
    if not uclient or not uclient.is_connected:
        try:
            api_id = await db.get_api_id(uid) or API_ID
            api_hash = await db.get_api_hash(uid) or API_HASH
            uclient = Client(f"User_{uid}", session_string=session_str, api_id=api_id, api_hash=api_hash, workers=100, ipv6=False)
            uclient.add_handler(MessageHandler(user_watcher_handler, is_watched_chat))
            await uclient.start()
            USER_CLIENTS[uid] = uclient
        except Exception as e:
            return web.json_response({"status": "error", "message": f"Session invalid: {e}"})

    dialog_collection = []

    try:
        async def execute_raw_pagination(target_folder_id):
            import pyrogram.raw.types as raw_types
            from pyrogram.raw.functions.messages import GetDialogs
            
            offset_date = 0
            offset_id = 0
            offset_peer = raw_types.InputPeerEmpty()

            while True:
                try:
                    response = await uclient.invoke(
                        GetDialogs(
                            offset_date=offset_date,
                            offset_id=offset_id,
                            offset_peer=offset_peer,
                            limit=100,
                            hash=0,
                            folder_id=target_folder_id
                        ),
                        sleep_threshold=60
                    )
                    
                    if not getattr(response, "dialogs", None):
                        break

                    resolved_users = {u.id: u for u in getattr(response, "users", [])}
                    resolved_chats = {c.id: c for c in getattr(response, "chats", [])}

                    for dialog in response.dialogs:
                        peer = dialog.peer
                        raw_chat_id = getattr(peer, "channel_id", getattr(peer, "chat_id", getattr(peer, "user_id", None)))
                        if not raw_chat_id: continue

                        if hasattr(peer, "channel_id"):
                            chat_id = int(f"-100{raw_chat_id}")
                        elif hasattr(peer, "chat_id"):
                            chat_id = int(f"-{raw_chat_id}")
                        else:
                            chat_id = raw_chat_id
                        
                        title = "Unknown Object"
                        category_label = "Unknown"
                        is_forum = False
                        
                        if chat_id > 0:
                            u = resolved_users.get(chat_id)
                            if u:
                                title = getattr(u, "first_name", None)
                                if not title:
                                    title = "Unknown User"
                                if getattr(u, "last_name", None):
                                    title += f" {u.last_name}"
                                category_label = "🤖 Bot" if getattr(u, "bot", False) else "👤 User"
                        else:
                            c = resolved_chats.get(abs(chat_id)) or resolved_chats.get(getattr(peer, "channel_id", 0)) or resolved_chats.get(getattr(peer, "chat_id", 0))
                            if c:
                                title = getattr(c, "title", None)
                                if not title:
                                    title = "Unknown Group"
                                category_label = "📢 Channel" if getattr(c, "broadcast", False) else "👥 Group"
                                is_forum = getattr(c, "forum", False)

                        dialog_collection.append({
                            "id": str(chat_id), 
                            "name": f"[{category_label}] {title}", 
                            "is_forum": is_forum
                        })

                    if len(response.dialogs) < 100:
                        break
                        
                    last_dialog = response.dialogs[-1]
                    offset_id = getattr(last_dialog, "top_message", 0)
                    
                    offset_date = 0
                    for msg in response.messages:
                        if getattr(msg, "id", 0) == offset_id:
                            offset_date = getattr(msg, "date", 0)
                            break
                    if offset_date == 0 and response.messages:
                        offset_date = getattr(response.messages[-1], "date", 0)

                    last_peer = last_dialog.peer
                    raw_last_id = getattr(last_peer, "channel_id", getattr(last_peer, "chat_id", getattr(last_peer, "user_id", 0)))
                    
                    if hasattr(last_peer, "channel_id"):
                        last_peer_id = int(f"-100{raw_last_id}")
                    elif hasattr(last_peer, "chat_id"):
                        last_peer_id = int(f"-{raw_last_id}")
                    else:
                        last_peer_id = raw_last_id

                    try:
                        offset_peer = await uclient.resolve_peer(last_peer_id)
                    except Exception:
                        if hasattr(last_peer, "channel_id"):
                            c = resolved_chats.get(raw_last_id)
                            offset_peer = raw_types.InputPeerChannel(channel_id=raw_last_id, access_hash=getattr(c, "access_hash", 0)) if c else raw_types.InputPeerEmpty()
                        elif hasattr(last_peer, "chat_id"):
                            offset_peer = raw_types.InputPeerChat(chat_id=raw_last_id)
                        else:
                            u = resolved_users.get(raw_last_id)
                            offset_peer = raw_types.InputPeerUser(user_id=raw_last_id, access_hash=getattr(u, "access_hash", 0)) if u else raw_types.InputPeerEmpty()

                except FloodWait as e:
                    await asyncio.sleep(e.value + 1)
                except Exception as e:
                    logger.warning(f"Raw dialog pagination error: {e}")
                    break

        async def populate_web_dialogs():
            await execute_raw_pagination(0) # Standard Chats
            await execute_raw_pagination(1) # Archived Chats

        try:
            await asyncio.wait_for(populate_web_dialogs(), timeout=300.0)
        except asyncio.TimeoutError:
            logger.warning("Web dialog fetch reached the 300s timeout ceiling. Returning the partial payload.")
            
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)})

    # Deduplicate arrays safely before returning to web UI
    sanitized_collection = {c['id']: c for c in dialog_collection}.values()
    return web.json_response({"status": "success", "chats": list(sanitized_collection)})

async def _api_speedtest_handler(request):
    try:
        uid = int(request.query.get("user_id", 0))
    except:
        uid = 0
        
    # 🟢 TOKEN CHECK
    token = request.query.get("token", "")
    user_doc = await db.col.find_one({"id": uid})
    if not user_doc or user_doc.get("web_token") != token:
        return web.json_response({"status": "error", "message": "Unauthorized: Invalid or expired Web Token."})
    
    session_str = await db.get_session(uid)
    if not session_str and uid not in ADMINS:
        return web.json_response({"status": "error", "message": "Unauthorized"})

    def run_speedtest_sync():
        try:
            st = speedtest.Speedtest(secure=True)
            st.get_best_server()
            st.download()
            st.upload()
            try:
                st.results.share()
            except Exception:
                pass
            return st.results.dict(), None
        except Exception as e:
            return None, str(e)

    result, error = await asyncio.to_thread(run_speedtest_sync)
    if error or not result:
        return web.json_response({"status": "error", "message": error or "Speedtest failed"})

    dl_mbps = result['download'] / 1_000_000
    ul_mbps = result['upload'] / 1_000_000
    
    return web.json_response({
        "status": "success",
        "download": f"{dl_mbps:.2f} Mbps",
        "upload": f"{ul_mbps:.2f} Mbps",
        "ping": f"{result['ping']} ms",
        "server": f"{result['server']['name']} ({result['server']['country']})",
        "sponsor": result['server']['sponsor'],
        "share_image": result.get("share", "")
    })

def _get_sos_sync():
    """Fetches system OS and IO stats safely in a background thread."""
    try:
        with open("/etc/os-release") as f:
            os_info = dict(line.strip().split("=", 1) for line in f if "=" in line)
        os_name = os_info.get("PRETTY_NAME", f'"{platform.system()} {platform.release()}"').strip('"')
    except Exception:
        os_name = f"{platform.system()} {platform.release()}"
    return os_name, psutil.virtual_memory(), psutil.disk_usage('/'), psutil.net_io_counters()

async def _api_sos_handler(request):
    try:
        uid = int(request.query.get("user_id", 0))
    except:
        uid = 0
        
    # 🟢 TOKEN CHECK
    token = request.query.get("token", "")
    user_doc = await db.col.find_one({"id": uid})
    if not user_doc or user_doc.get("web_token") != token:
        return web.json_response({"status": "error", "message": "Unauthorized: Invalid or expired Web Token."})
        
    session_str = await db.get_session(uid)
    if not session_str and uid not in ADMINS:
        return web.json_response({"status": "error", "message": "Unauthorized"})

    m_down, m_up, m_total, month_name = await db.get_monthly_bandwidth()
    os_name, mem, disk, net = await asyncio.to_thread(_get_sos_sync)

    return web.json_response({
        "status": "success",
        "os": os_name,
        "hostname": socket.gethostname(),
        "kernel": platform.uname().release,
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "ram_percent": mem.percent,
        "ram_used": _pretty_bytes(mem.used),
        "ram_total": _pretty_bytes(mem.total),
        "disk_percent": disk.percent,
        "disk_free": _pretty_bytes(disk.free),
        "disk_total": _pretty_bytes(disk.total),
        "boot_download": _pretty_bytes(net.bytes_recv),
        "boot_upload": _pretty_bytes(net.bytes_sent),
        "month_name": month_name,
        "month_download": _pretty_bytes(m_down),
        "month_upload": _pretty_bytes(m_up),
        "month_total": _pretty_bytes(m_total)
    })

PWA_MANIFEST = {
    "name": "Destiny TG Forwarder",
    "short_name": "TG Portal",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#000000",
    "theme_color": "#000000",
    "orientation": "portrait-primary",
    "icons": [
        {
            "src": "https://cdn-icons-png.flaticon.com/512/2111/2111646.png",
            "sizes": "192x192",
            "type": "image/png"
        },
        {
            "src": "https://cdn-icons-png.flaticon.com/512/2111/2111646.png",
            "sizes": "512x512",
            "type": "image/png"
        }
    ]
}

async def _manifest_handler(request):
    return web.json_response(PWA_MANIFEST)

async def _sw_handler(request):
    sw_code = "self.addEventListener('fetch', function(e) {});"
    return web.Response(text=sw_code, content_type='application/javascript')

async def _api_topics_handler(request):
    uid = int(request.query.get("user_id", 0))
    chat_id = request.query.get("chat_id", "")
    try: chat_id = int(chat_id)
    except: pass
    
    session_str = await db.get_session(uid)
    if not session_str:
        return web.json_response({"status": "error", "message": "Not connected to Telegram."})

    uclient = USER_CLIENTS.get(uid)

    # 🟢 DYNAMIC WAKE-UP
    if not uclient or not uclient.is_connected:
        try:
            api_id = await db.get_api_id(uid) or API_ID
            api_hash = await db.get_api_hash(uid) or API_HASH
            uclient = Client(f"User_{uid}", session_string=session_str, api_id=api_id, api_hash=api_hash, workers=100, ipv6=False)
            uclient.add_handler(MessageHandler(user_watcher_handler, is_watched_chat))
            await uclient.start()
            USER_CLIENTS[uid] = uclient
        except Exception as e:
            return web.json_response({"status": "error", "message": f"Session invalid: {e}"})
    
    topics = []
    try:
        async def fetch_tg_topics():
            try:
                async for topic in uclient.get_forum_topics(chat_id, limit=300):
                    topics.append({"id": topic.id, "title": topic.title})
            except Exception as e:
                # Graceful handling of Pyrogram pagination bug
                if "'NoneType'" not in str(e):
                    logger.warning(f"Topic pagination interrupted: {e}")
            
        try:
            await asyncio.wait_for(fetch_tg_topics(), timeout=25.0)
        except asyncio.TimeoutError:
            logger.warning(f"Topics endpoint timed out. Returning {len(topics)} topics found so far.")
        except Exception as e:
            logger.warning(f"Topics endpoint exception: {repr(e)}")
                
    except Exception as e:
        logger.warning(f"Topics endpoint error: {repr(e)}")

    return web.json_response({"status": "success", "topics": topics})

# 🟢 NEW: Deep Chat Details & MetaData Fetcher
import traceback

async def _api_chat_details_handler(request):
    uid = int(request.query.get("user_id", 0))
    raw_chat_string = request.query.get("chat_id", "").strip()
    
    # 🟢 TOKEN CHECK
    token = request.query.get("token", "")
    user_doc = await db.col.find_one({"id": uid})
    if not user_doc or user_doc.get("web_token") != token:
        return web.json_response({"status": "error", "message": "Unauthorized: Invalid or expired Web Token."})
    
    if not raw_chat_string:
        return web.json_response({"status": "error", "message": "Missing required chat_id parameter."})
        
    try: 
        chat_id = int(raw_chat_string)
    except ValueError: 
        chat_id = raw_chat_string if raw_chat_string.startswith("@") else f"@{raw_chat_string}"

    session_str = await db.get_session(uid)
    if not session_str:
        return web.json_response({"status": "error", "message": "Not logged in."})

    uclient = USER_CLIENTS.get(uid)
    
    # Wake up routine to prevent locks
    if not uclient or not uclient.is_connected:
        try:
            api_id = await db.get_api_id(uid) or API_ID
            api_hash = await db.get_api_hash(uid) or API_HASH
            uclient = Client(f"User_{uid}", session_string=session_str, api_id=api_id, api_hash=api_hash, workers=100, ipv6=False)
            uclient.add_handler(MessageHandler(user_watcher_handler, is_watched_chat))
            await uclient.start()
            USER_CLIENTS[uid] = uclient
        except Exception as e:
            logger.error(f"[CHAT DETAILS] Client connection failed: {e}")
            return web.json_response({"status": "error", "message": f"Session invalid: {e}"})

    try:
        # 🟢 FIX 1: Safely resolve ALL chat types (Users, Bots, Channels, Groups)
        try:
            chat = await asyncio.wait_for(uclient.get_chat(chat_id), timeout=12.0)
        except PeerIdInvalid:
            try:
                resolved_peer = await asyncio.wait_for(uclient.resolve_peer(chat_id), timeout=8.0)
                chat = await asyncio.wait_for(uclient.get_chat(resolved_peer), timeout=12.0)
            except Exception as inner_e:
                raise Exception(f"Fatal resolution failure. ({inner_e})")
        
        # Safely fetch total message count (Only works on Groups/Channels/PMs)
        try:
            total_msgs = await asyncio.wait_for(uclient.get_chat_history_count(chat_id), timeout=6.0)
        except Exception:
            total_msgs = "Unknown"

        topics = []
        is_forum = getattr(chat, "is_forum", False)
        
        # 🟢 FIX 2: Only fetch topics if it's explicitly a SUPERGROUP and a FORUM!
        # Prevents crashing on normal Groups, Channels, Bots, or Users.
        if is_forum and getattr(chat, "type", None) == enums.ChatType.SUPERGROUP:
            async def fetch_forum_topology():
                try:
                    # 🟢 FIX 3: HARD LIMIT to 250 topics so it finishes in 1-2 seconds and never times out!
                    async for t in uclient.get_forum_topics(chat_id, limit=250):
                        top_msg_data = getattr(t, "top_message", "?")
                        if hasattr(top_msg_data, "id"):
                            top_msg_val = str(top_msg_data.id)
                        else:
                            top_msg_val = str(top_msg_data)
                        topics.append({
                            "id": t.id,
                            "title": t.title,
                            "top_msg": top_msg_val
                        })
                except Exception as inner_e:
                    if "'NoneType'" not in str(inner_e):
                        logger.warning(f"[CHAT DETAILS] Topic pagination interrupted: {inner_e}")
                        
            try:
                # Give it 8 seconds to fetch the 250 topics
                await asyncio.wait_for(fetch_forum_topology(), timeout=8.0)
            except asyncio.TimeoutError:
                logger.warning(f"[CHAT DETAILS] Topic fetch timed out. Returning {len(topics)} topics found so far.")
            except Exception as e:
                logger.warning(f"[CHAT DETAILS] Could not fetch topics: {repr(e)}")

        return web.json_response({
            "status": "success",
            "id": str(chat.id),
            "title": chat.title or getattr(chat, "first_name", "Unknown"),
            "type": str(getattr(chat, "type", "Unknown")).replace("ChatType.", "").upper(),
            "members": getattr(chat, "members_count", 0),
            "total_messages": total_msgs,
            "description": getattr(chat, "description", getattr(chat, "bio", "")),
            "is_forum": is_forum,
            "topics": topics
        })
    except Exception as e:
        import traceback
        err_trace = traceback.format_exc()
        logger.error(f"[CHAT DETAILS ERROR] Traceback:\n{err_trace}")
        return web.json_response({"status": "error", "message": f"API Error: {str(e)}"})

async def _api_mediainfo_web_handler(request):
    data = await request.json()
    uid = int(data.get("user_id", 0))
    url = data.get("link", "")
    if not url: return web.json_response({"status": "error", "message": "No link provided"})
    
    file_path = Path(os.getcwd()) / f"web_mi_{uid}_{int(time.time())}.dat"
    file_name_display = "Unknown_File"
    file_size_display = 0
    
    try:
        # 🟢 FIX: Prioritize Telegram links FIRST so they don't get trapped by the HTTP downloader
        if "t.me" in url or "telegram.me" in url:
            parsed = _parse_source_link(url)
            chat_id = parsed.get("chat_id")
            msg_id = parsed.get("msg_id")
            
            # 🟢 DYNAMIC WAKE-UP: Automatically reconnect session if it fell asleep
            uclient = USER_CLIENTS.get(uid)
            if not uclient or not uclient.is_connected:
                session_str = await db.get_session(uid)
                if not session_str:
                    return web.json_response({"status": "error", "message": "Telegram session not active. Connect in Settings."})
                try:
                    api_id = await db.get_api_id(uid) or API_ID
                    api_hash = await db.get_api_hash(uid) or API_HASH
                    uclient = Client(f"User_{uid}", session_string=session_str, api_id=api_id, api_hash=api_hash, workers=100, ipv6=False)
                    uclient.add_handler(MessageHandler(user_watcher_handler, is_watched_chat))
                    await uclient.start()
                    USER_CLIENTS[uid] = uclient
                except Exception as e:
                    return web.json_response({"status": "error", "message": f"Session invalid: {e}"})
                
            try:
                msg = await uclient.get_messages(chat_id, msg_id)
            except Exception as e:
                return web.json_response({"status": "error", "message": f"Failed to fetch message: {e}"})
                
            if not msg or msg.empty: return web.json_response({"status": "error", "message": "Message not found or inaccessible"})
            
            media_obj = msg.document or msg.video or msg.audio or msg.photo
            if not media_obj: return web.json_response({"status": "error", "message": "No media found in the provided link"})
            
            file_name_display = getattr(media_obj, 'file_name', 'Telegram_Media')
            file_size_display = getattr(media_obj, 'file_size', 0)
            
            await partial_download_tg(uclient, msg, file_path, limit_mb=15)

        elif url.startswith("http"):
            file_size_display, detected_name = await partial_download_http(url, file_path, limit_mb=15)
            file_name_display = detected_name
        else:
            return web.json_response({"status": "error", "message": "Invalid link format"})
            
        real_ext = Path(file_name_display).suffix
        if real_ext:
            new_path = file_path.with_suffix(real_ext)
            file_path.rename(new_path)
            file_path = new_path
            
        cmd = ["mediainfo", str(file_path)]
        process = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        stdout, _ = await process.communicate()
        raw_output = stdout.decode('utf-8', errors='ignore').strip()
        
        if not raw_output:
            return web.json_response({"status": "error", "message": "Could not read media metadata. File might be empty or invalid."})
            
        raw_output = raw_output.replace(str(file_path), file_name_display).replace(str(file_path.absolute()), file_name_display)
        html_formatted = f"<div style='color:var(--accent); font-weight:bold; font-size:15px;'>📌 {html.escape(file_name_display)}</div><br>" + parseinfo(raw_output, file_size_display)
        
        return web.json_response({"status": "success", "html": html_formatted})
        
    except Exception as e:
        # 🟢 FIX: Force empty string errors to print their raw representation so the popup is never blank
        err_msg = str(e) if str(e).strip() else repr(e)
        return web.json_response({"status": "error", "message": f"Processing error: {err_msg}"})
    finally:
        if 'file_path' in locals() and file_path.exists():
            try: os.remove(file_path)
            except: pass

async def _api_spectrogram_web_handler(request):
    data = await request.json()
    uid = int(data.get("user_id", 0))
    url = data.get("link", "")
    if not url: return web.json_response({"status": "error", "message": "No link provided"})
    
    temp_dir = Path(f"./temp_sox_web_{uid}_{int(time.time())}")
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    original_file = temp_dir / "audio_input.dat"
    wav_file = temp_dir / "converted.wav"
    output_img = temp_dir / "spectrogram.png"
    
    try:
        # 1. DOWNLOAD FULL FILE
        if "t.me" in url or "telegram.me" in url:
            parsed = _parse_source_link(url)
            chat_id = parsed.get("chat_id")
            msg_id = parsed.get("msg_id")
            
            uclient = USER_CLIENTS.get(uid)
            if not uclient or not uclient.is_connected:
                return web.json_response({"status": "error", "message": "Telegram session not active. Connect in Settings."})
                
            msg = await uclient.get_messages(chat_id, msg_id)
            if msg.empty: return web.json_response({"status": "error", "message": "Message not found or inaccessible"})
            await uclient.download_media(msg, file_name=str(original_file))
        elif url.startswith("http"):
            await full_download_http(url, original_file)
        else:
            return web.json_response({"status": "error", "message": "Invalid link format"})

        # 2. FFMPEG
        ffmpeg_cmd = ["ffmpeg", "-i", str(original_file), "-vn", "-ac", "2", "-c:a", "pcm_f32le", str(wav_file), "-y"]
        process = await asyncio.create_subprocess_exec(*ffmpeg_cmd, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.PIPE)
        await process.wait()
        
        if not wav_file.exists(): return web.json_response({"status": "error", "message": "Audio Extraction Failed."})

        # 3. DSP & SOX
        stats = await asyncio.to_thread(generate_audio_stats_dsp, str(wav_file), str(original_file), "Web Audio")
        if not stats: return web.json_response({"status": "error", "message": "DSP Processing Failed."})

        sox_cmd = ["sox", str(wav_file), "-n", "spectrogram", "-o", str(output_img), "-x", "1000", "-Y", "800", "-c", "Audio", "-t", " "]
        process_sox = await asyncio.create_subprocess_exec(*sox_cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        await process_sox.communicate()

        if not output_img.exists(): return web.json_response({"status": "error", "message": "SoX Generation Failed."})

        # 4. CONVERT TO BASE64 & HTML
        with open(output_img, "rb") as img_f:
            img_b64 = base64.b64encode(img_f.read()).decode('utf-8')

        m = stats['mastering']
        mastering_html = ""
        if m:
            mastering_html = (
                f"<br><span style='color:var(--accent);'><b>— MASTERING ANALYSIS —</b></span><br>"
                f"🎚 <b>Dynamic Range:</b> DR {m['dr']}<br>"
                f"🔊 <b>Loudness:</b> {m['lufs']:.1f} LUFS<br>"
                f"📈 <b>Peak / RMS:</b> {m['peak']:.2f} dBFS / {m['rms']:.2f} dB<br>"
                f"🏷 <b>Score:</b> {m['grade']}"
            )

        html_stats = (
            f"<span style='color:#10b981;'><b>{stats['auth_badge']}</b></span><br>"
            f"<i>{stats['auth_desc']}</i><br><br>"
            f"📀 <b>Format:</b> {stats['format']} • {stats['channel_str']} • {stats['bit_depth']}-bit • {stats['sample_rate']/1000} kHz<br>"
            f"📈 <b>Cutoff:</b> {stats['cutoff']} kHz<br>"
            f"🧱 <b>Cliff Drop:</b> {stats['cliff_drop']:.1f} dB"
            f"{mastering_html}"
        )

        return web.json_response({"status": "success", "image": img_b64, "html": html_stats})

    except Exception as e:
        return web.json_response({"status": "error", "message": f"Processing error: {e}"})
    finally:
        import shutil
        try: shutil.rmtree(str(temp_dir), ignore_errors=True)
        except: pass

# ==============================================================================
from collections import defaultdict

USER_STREAM_BOTS = defaultdict(list)
USER_TASK_BOTS = defaultdict(list)

async def init_worker_bots(user_id=None):
    """Initializes isolated bot clients for streaming vs tasks."""
    user_ids_to_init = [user_id] if user_id else []
    if not user_id:
        # 🟢 FIX: Check all 3 arrays so it boots up perfectly on startup
        cursor = db.col.find({"$or": [
            {"stream_tokens": {"$exists": True, "$ne": []}}, 
            {"task_tokens": {"$exists": True, "$ne": []}},
            {"bot_tokens": {"$exists": True, "$ne": []}}
        ]})
        async for u in cursor:
            user_ids_to_init.append(u["id"])
            
    for uid in user_ids_to_init:
        # Stop existing Stream Bots
        for c in USER_STREAM_BOTS.get(uid, []):
            try: await c.stop()
            except Exception: pass
        USER_STREAM_BOTS[uid].clear()
        
        # Stop existing Task Bots
        for c in USER_TASK_BOTS.get(uid, []):
            try: await c.stop()
            except Exception: pass
        USER_TASK_BOTS[uid].clear()
        
        user_doc = await db.col.find_one({"id": uid})
        if not user_doc: continue
        
        # 🟢 Migrate old tokens to stream array if necessary
        stream_tokens = user_doc.get("stream_tokens", [])
        if not stream_tokens and user_doc.get("bot_tokens"):
            stream_tokens = user_doc.get("bot_tokens")
            
        task_tokens = user_doc.get("task_tokens", [])
        
        # 1. Initialize Stream Bots
        for idx, token in enumerate(stream_tokens, start=1):
            try:
                bot_client = Client(f"stream_bot_{uid}_{idx}", api_id=API_ID, api_hash=API_HASH, bot_token=token.strip(), workers=4, no_updates=True, ipv6=False)
                await bot_client.start()
                USER_STREAM_BOTS[uid].append(bot_client)
                logger.info(f"🚀 Stream Bot {idx} active for user {uid}")
            except Exception as e:
                logger.warning(f"Failed to load stream token {idx} for {uid}: {e}")

        # 2. Initialize Task Bots
        for idx, token in enumerate(task_tokens, start=1):
            try:
                bot_client = Client(f"task_bot_{uid}_{idx}", api_id=API_ID, api_hash=API_HASH, bot_token=token.strip(), workers=4, no_updates=True, ipv6=False)
                await bot_client.start()
                USER_TASK_BOTS[uid].append(bot_client)
                logger.info(f"🚀 Task Bot {idx} active for user {uid}")
            except Exception as e:
                logger.warning(f"Failed to load task token {idx} for {uid}: {e}")

async def _api_get_worker_tokens(request):
    uid = int(request.query.get("user_id", 0))
    
    # 🟢 TOKEN CHECK
    token = request.query.get("token", "")
    doc = await db.col.find_one({"id": uid})
    if not doc or doc.get("web_token") != token:
        return web.json_response({"status": "error", "message": "Unauthorized: Invalid or expired Web Token."})
        
    # 🟢 FIX: Auto-load your old "bot_tokens" into the streaming box if you haven't saved new ones yet!
    stream_tokens = doc.get("stream_tokens", [])
    if not stream_tokens and doc.get("bot_tokens"):
        stream_tokens = doc.get("bot_tokens")
        
    return web.json_response({
        "status": "success", 
        "stream_tokens": stream_tokens,
        "task_tokens": doc.get("task_tokens", []) if doc else []
    })

async def _api_save_worker_tokens(request):
    data = await request.json()
    uid = int(data.get("user_id", 0))
    
    stream_tokens = [t.strip() for t in data.get("stream_tokens", []) if ":" in t]
    task_tokens = [t.strip() for t in data.get("task_tokens", []) if ":" in t]
    
    # Save directly to the User's Database Object
    await db.col.update_one(
        {"id": uid}, 
        {"$set": {"stream_tokens": stream_tokens, "task_tokens": task_tokens}}, 
        upsert=True
    )
    asyncio.create_task(init_worker_bots(uid))
    
    # Clear access cache so the new bots are used immediately
    TG_ACCESS_CACHE.clear()
    
    return web.json_response({"status": "success", "message": f"Saved {len(stream_tokens)} Stream Bots and {len(task_tokens)} Task Bots. Pools reloading."})

async def _api_network_stats(request):
    try: uid = int(request.query.get("user_id", 0))
    except: uid = 0
    
    # 🟢 TOKEN CHECK
    token = request.query.get("token", "")
    user_doc = await db.col.find_one({"id": uid})
    if not user_doc or user_doc.get("web_token") != token:
        return web.json_response({"status": "error", "message": "Unauthorized: Invalid or expired Web Token."})
        
    # 🟢 PRIVACY FIX: Filter streams so normal users only see their own!
    is_admin = await db.is_user_admin(uid)
    active_list = list(GLOBAL_NETWORK_STATS["active"].values())
    recent_list = GLOBAL_NETWORK_STATS["recent"]

    if not is_admin:
        active_list = [s for s in active_list if str(s.get("user_id", "")) == str(uid)]
        recent_list = [s for s in recent_list if str(s.get("user_id", "")) == str(uid)]
        
    return web.json_response({
        "status": "success",
        "active": active_list,
        "recent": recent_list,
        "worker_bots_count": len(USER_STREAM_BOTS.get(uid, [])) + len(USER_TASK_BOTS.get(uid, []))
    })

# --- NEW: NATIVE IMAGE PROXY TO BYPASS HUGGINGFACE CSP ---
async def _api_bg_proxy(request):
    url = request.query.get("url", "")
    if not url: return web.Response(status=400)
    import aiohttp
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers={"User-Agent": "Mozilla/5.0"}) as resp:
                body = await resp.read()
                return web.Response(body=body, headers={"Content-Type": "image/jpeg", "Cache-Control": "public, max-age=8640000"})
    except Exception:
        return web.Response(status=500)

async def _api_playlist_handler(request):
    """Extracts playlist array from ZIPs and Split ZIPs for continuous album playback."""
    try: user_id = int(request.query.get("user_id", 0))
    except: user_id = 0
    link = request.query.get("link", "").strip()
    if not link: return web.json_response({"status": "error"})
    
    is_tg = _is_tg_link(link)
    playlist = []
    try:
        if is_tg:
            parsed = _parse_source_link(link)
            chat_id = parsed.get("chat_id")
            msg_id = parsed.get("msg_id")
            pool, _ = await _get_working_tg_pool(user_id, chat_id, msg_id)
            primary_client = pool[0]
            
            msg = await get_client_msg(primary_client, chat_id, msg_id)
            media = msg.document or msg.video or msg.audio
            filename = str(getattr(media, "file_name", "")).lower()
            
            # 🟢 FIX: Support all major archive extensions for the playlist extractor (.zip.001, .7z.001, etc)
            is_zip = bool(re.search(r'\.(zip|7z|rar|tar|gz)(\.\d{3})?$', filename))
            if not is_zip: return web.json_response({"status": "success", "playlist": []})
            
            parts_map = []
            global_offset = 0
            match = re.search(r'\.(\d{2,3})$', filename)
            if match and int(match.group(1)) == 1:
                current_id = msg_id
                while True:
                    try:
                        m = await get_client_msg(primary_client, chat_id, current_id)
                        doc = m.document or m.video or m.audio
                        if not doc: break
                        psz = int(doc.file_size or 0)
                        parts_map.append({"msg_id": m.id, "start": global_offset, "end": global_offset + psz, "size": psz})
                        global_offset += psz
                        current_id += 1
                        next_m = await get_client_msg(primary_client, chat_id, current_id)
                        next_doc = next_m.document or next_m.video or next_m.audio
                        if not next_doc or not re.search(r'\.\d{2,3}$', next_doc.file_name or ""): break
                    except Exception: break
            else:
                part_size = int(getattr(media, "file_size", 0) or 0)
                parts_map.append({"msg_id": msg_id, "start": 0, "end": part_size, "size": part_size})
                global_offset = part_size
                
            async def zip_read_tg(off, length):
                buf = bytearray()
                async for chunk in parallel_stream_generator(primary_client, chat_id, parts_map, off, length):
                    buf.extend(chunk)
                    if len(buf) >= length: break
                return bytes(buf[:length])
                
            playlist = await get_zip_playlist(zip_read_tg, global_offset)
        else:
            actual_url = await resolve_direct_link(link)
            filename = _guess_filename_from_url(actual_url).lower()
            is_zip = filename.endswith(".zip") or ".zip." in filename
            if not is_zip: return web.json_response({"status": "success", "playlist": []})
            
            session = await _get_direct_http_session()
            async with session.head(actual_url, allow_redirects=True) as h_resp:
                raw_size = int(h_resp.headers.get("Content-Length", 0))
                
            async def zip_read_http(off, length):
                headers = {"Range": f"bytes={off}-{off+length-1}", "User-Agent": "Mozilla/5.0"}
                async with session.get(actual_url, headers=headers) as r:
                    return await r.read()
                    
            playlist = await get_zip_playlist(zip_read_http, raw_size)
            
        return web.json_response({"status": "success", "playlist": playlist})
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)})

# ==============================================================================
# --- NEW: WORLD EXPLORER PROXY ENDPOINTS ---
# ==============================================================================
async def _api_proxy_country(request):
    iso = request.query.get("iso", "").strip()
    name = request.query.get("name", "").strip()
    import aiohttp
    import json
    from urllib.parse import quote

    async def fetch_api(url):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        try:
            # 🟢 FIX: Increased timeout to 10s and disabled strict SSL to prevent Koyeb blocks
            timeout = aiohttp.ClientTimeout(total=10)
            connector = aiohttp.TCPConnector(ssl=False)
            async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
                async with session.get(url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if isinstance(data, list) and len(data) > 0: return data
                        if isinstance(data, dict): return [data] # Always format as list
        except Exception as e:
            print(f"[Globe API] Backend failed: {e}")
        return None

    try:
        data = None
        # Attempt 1: Try ISO Code
        if iso and iso != "-99":
            data = await fetch_api(f"https://restcountries.com/v3.1/alpha/{iso}")
        
        # Attempt 2: Fallback to Exact Name Search
        if not data and name:
            data = await fetch_api(f"https://restcountries.com/v3.1/name/{quote(name)}?fullText=true")
            
        # Attempt 3: Fallback to Partial Name Search
        if not data and name:
            data = await fetch_api(f"https://restcountries.com/v3.1/name/{quote(name)}")

        # Attempt 4: Fallback to V2 API if V3 is rate-limited
        if not data and iso and iso != "-99":
            data = await fetch_api(f"https://restcountries.com/v2/alpha/{iso}")

        if data:
            return web.json_response(data)
        else:
            # 🟢 FIX: Return real Earth icon if API fails
            mock_data = {
                "name": {"common": name or "Unknown Country"},
                "capital": ["Unavailable"],
                "region": "Unavailable",
                "population": "Unavailable",
                "timezones": ["UTC"],
                "flags": {"png": "https://cdn-icons-png.flaticon.com/512/44/44386.png"} 
            }
            return web.json_response([mock_data])
            
    except Exception as e:
        mock_data = {
            "name": {"common": name or "Unknown Country"},
            "capital": ["Unavailable"],
            "region": "Unavailable",
            "population": "Unavailable",
            "timezones": ["UTC"],
            "flags": {"png": "https://cdn-icons-png.flaticon.com/512/44/44386.png"}
        }
        return web.json_response([mock_data])

async def _api_proxy_wiki(request):
    q = request.query.get("q", "").strip()
    import aiohttp
    from urllib.parse import quote
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        async with aiohttp.ClientSession() as session:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(q)}"
            async with session.get(url, headers=headers) as resp:
                text = await resp.text()
                return web.Response(status=resp.status, text=text, content_type="application/json")
    except Exception as e:
        return web.Response(status=500, text=str(e))

# ==============================================================================
# --- MEDIA EDITOR PROGRESS TRACKER ---
# ==============================================================================
EDITOR_UI_STATE = {}

async def _api_editor_progress(request):
    task_uuid = request.query.get("task_uuid")
    if not task_uuid or task_uuid not in EDITOR_UI_STATE:
        return web.json_response({"status": "error", "message": "Task not found"})
    
    state = EDITOR_UI_STATE[task_uuid]
    resp = {"status": "success", "phase": state["phase"], "done": state["done"], "error": state["error"]}
    
    # Bridge the Telegram progress stats into the Web Dashboard
    if state["status_msg_id"]:
        typ = "down" if state["phase"] == "Downloading" else ("up" if state["phase"] == "Uploading" else None)
        if typ:
            prog = PROGRESS.get(f"{task_uuid}:{typ}")
            if prog:
                resp["percent"] = prog.get("percent", 0)
                resp["speed"] = prog.get("speed", 0)
                resp["current"] = prog.get("current", 0)
                resp["total"] = prog.get("total", 0)
                resp["eta"] = prog.get("eta", 0)
                
    return web.json_response(resp)
    
async def _api_edit_media_handler(request):
    data = await request.json()
    uid = int(data.get("user_id", 0))
    link = data.get("link", "")
    config = data.get("config", [])
    new_name = data.get("new_name", "output.mkv")
    dest = data.get("dest", "tg")
    thumb_b64 = data.get("thumb", "")
    global_tags = data.get("global_tags", {})
    
    if not link or not config:
        return web.json_response({"status": "error", "message": "Missing link or config"})
        
    import time
    from pathlib import Path
    import shutil
    import base64
    
    task_uuid = uuid.uuid4().hex[:8]
    temp_dir = Path(f"./temp_remux_{uid}_{task_uuid}")
    EDITOR_UI_STATE[task_uuid] = {"phase": "Starting...", "status_msg_id": None, "error": None, "done": False}
    
    async def background_editor():
        temp_dir.mkdir(parents=True, exist_ok=True)
        input_file = temp_dir / "input_media.dat"
        output_file = temp_dir / sanitize_filename(new_name)
        thumb_path = None
        
        try:
            status_msg = await app.send_message(uid, f"⚙️ **Media Editor Task Started!**\n\n**Target:** `{new_name}`\n⏳ Downloading sources...")
            EDITOR_UI_STATE[task_uuid]["status_msg_id"] = status_msg.id
            
            if thumb_b64:
                try:
                    thumb_data = base64.b64decode(thumb_b64.split(",")[1] if "," in thumb_b64 else thumb_b64)
                    thumb_path = temp_dir / "thumb.jpg"
                    with open(thumb_path, "wb") as f:
                        f.write(thumb_data)
                except Exception as e:
                    logger.warning(f"Thumb decode failed: {e}")

            # 🟢 DOWNLOAD EXTERNAL TRACKS
            EDITOR_UI_STATE[task_uuid]["phase"] = "Downloading"
            for idx, track in enumerate(config):
                if track.get("type") in ["ext_audio", "ext_sub"]:
                    ext_path = temp_dir / f"ext_track_{idx}_{track['type']}.dat"
                    if track.get("b64"):
                        try:
                            b64_data = track["b64"].split(",")[1] if "," in track["b64"] else track["b64"]
                            with open(ext_path, "wb") as f:
                                f.write(base64.b64decode(b64_data))
                        except Exception: pass
                    elif track.get("url"):
                        ext_link = track["url"]
                        try:
                            if _is_tg_link(ext_link):
                                eparsed = _parse_source_link(ext_link)
                                wp, _ = await _get_working_tg_pool(uid, eparsed["chat_id"], eparsed["msg_id"])
                                eclient = wp[0] if wp else app
                                emsg = await get_client_msg(eclient, eparsed["chat_id"], eparsed["msg_id"])
                                await eclient.download_media(emsg, file_name=str(ext_path))
                            else:
                                await full_download_http(ext_link, str(ext_path))
                        except Exception: pass
                    if ext_path.exists():
                        track["local_path"] = str(ext_path)

            # 🟢 DOWNLOAD MAIN FILE
            is_tg = _is_tg_link(link)
            if is_tg:
                parsed = _parse_source_link(link)
                working_pool, _ = await _get_working_tg_pool(uid, parsed["chat_id"], parsed["msg_id"])
                client_to_use = working_pool[0] if working_pool else app
                
                msg = await get_client_msg(client_to_use, parsed["chat_id"], parsed["msg_id"])
                await client_to_use.download_media(msg, file_name=str(input_file), progress=progress, progress_args=["down", task_uuid])
            else:
                await full_download_http(link, str(input_file))
                
            EDITOR_UI_STATE[task_uuid]["phase"] = "Remuxing"
            await status_msg.edit_text("⚙️ **Remuxing Tracks (Instant Copy)...**")
            await process_remux(str(input_file), str(output_file), config, global_tags)
            
            if dest == "gofile":
                EDITOR_UI_STATE[task_uuid]["phase"] = "Uploading"
                await status_msg.edit_text("☁️ **Uploading to GoFile...**")
                url = await upload_to_gofile(str(output_file))
                await status_msg.edit_text(f"✅ **Success! Uploaded to GoFile.**\n\n🔗 **Link:** {url}", disable_web_page_preview=True)
            else:
                upload_chat_id = uid if dest == "tg" else dest
                try: upload_chat_id = int(upload_chat_id)
                except: pass
                
                kwargs = {
                    "chat_id": upload_chat_id,
                    "document": str(output_file),
                    "caption": f"**{new_name}**"
                }
                if thumb_path and thumb_path.exists():
                    kwargs["thumb"] = str(thumb_path)

                # 🟢 SMART UPLOAD ENGINE (>2GB & Premium Logic)
                file_size = os.path.getsize(output_file)
                split_limit = 2000 * 1024 * 1024 
                
                uclient = USER_CLIENTS.get(uid)
                is_premium = False
                
                # Wake up user session if asleep to check Premium status
                if not uclient or not uclient.is_connected:
                    session_str = await db.get_session(uid)
                    if session_str:
                        u_api = await db.get_api_id(uid) or API_ID
                        u_hash = await db.get_api_hash(uid) or API_HASH
                        uclient = Client(
                            f"User_{uid}", 
                            session_string=session_str, 
                            api_id=u_api, 
                            api_hash=u_hash, 
                            ipv6=False,
                            sleep_threshold=120,
                            **get_transmission_kwargs(workers=4, is_bot=False) # 🟢 Force 1 concurrent
                        )
                        await uclient.start()
                        USER_CLIENTS[uid] = uclient
                        
                if uclient and uclient.is_connected:
                    try:
                        me = uclient.me or await uclient.get_me()
                        is_premium = getattr(me, "is_premium", False)
                    except: pass
                
                EDITOR_UI_STATE[task_uuid]["phase"] = "Uploading"

                if file_size > split_limit and not is_premium:
                    EDITOR_UI_STATE[task_uuid]["phase"] = "Splitting"
                    await status_msg.edit_text(f"✂️ **Splitting large file ({_pretty_bytes(file_size)})...**")
                    parts = await split_file_python(str(output_file), chunk_size=1900*1024*1024)
                    
                    EDITOR_UI_STATE[task_uuid]["phase"] = "Uploading"
                    for i, part in enumerate(parts):
                        await status_msg.edit_text(f"☁️ **Uploading Part {i+1}/{len(parts)}...**")
                        kwargs["document"] = str(part)
                        kwargs["caption"] = f"**{part.name}**"
                        await safe_send(app, uid, upload_chat_id, task_uuid, True, app.send_document, progress=progress, progress_args=["up", task_uuid], **kwargs)
                        try: os.remove(part)
                        except: pass
                        
                elif file_size > split_limit and is_premium:
                    await status_msg.edit_text(f"☁️ **Uploading via Premium Session ({_pretty_bytes(file_size)})...**")
                    await safe_send(uclient, uid, upload_chat_id, task_uuid, False, uclient.send_document, progress=progress, progress_args=["up", task_uuid], **kwargs)
                else:
                    await status_msg.edit_text("☁️ **Uploading to Destination...**")
                    await safe_send(app, uid, upload_chat_id, task_uuid, True, app.send_document, progress=progress, progress_args=["up", task_uuid], **kwargs)
                    
                await status_msg.delete()
                
                if str(upload_chat_id) != str(uid):
                    await app.send_message(uid, f"✅ **Media Editor Completed!**\nFile `{new_name}` was successfully uploaded to your selected chat.")
                    
            EDITOR_UI_STATE[task_uuid]["done"] = True
        except Exception as e:
            logger.error(f"Background Edit Error: {e}", exc_info=True)
            EDITOR_UI_STATE[task_uuid]["error"] = str(e)
            EDITOR_UI_STATE[task_uuid]["done"] = True
            try: await app.send_message(uid, f"❌ **Media Editor Failed:**\n`{str(e)}`")
            except: pass
        finally:
            shutil.rmtree(str(temp_dir), ignore_errors=True)
            
    asyncio.create_task(background_editor())
    return web.json_response({"status": "success", "task_uuid": task_uuid})

async def start_koyeb_health_check(host: str = "0.0.0.0"):
    if web is None: return
    global PORT
    
    # 🟢 FIX: 500MB Payload Limit for High-Res Audio/Thumbnails
    app_web = web.Application(client_max_size=1024**2 * 500)
    
    # Core & Dashboard
    app_web.router.add_get("/", _dashboard_ui_handler)
    app_web.router.add_get("/health", _dashboard_ui_handler)
    app_web.router.add_get("/manifest.json", _manifest_handler)
    app_web.router.add_get("/sw.js", _sw_handler)
    
    # Stats & Logs
    app_web.router.add_get("/api/stats", _api_stats_handler)
    app_web.router.add_get("/api/logs", _api_logs_handler)
    app_web.router.add_get("/api/logs/download", _api_download_log_handler)
    app_web.router.add_get("/api/network", _api_network_stats)
    app_web.router.add_get("/api/sos", _api_sos_handler)
    app_web.router.add_get("/api/speedtest", _api_speedtest_handler)
    
    # Auth & Settings
    app_web.router.add_post("/api/auth/login", _api_login_handler)
    app_web.router.add_post("/api/auth/forgot", _api_forgot_password_handler)
    app_web.router.add_post("/api/auth/password", _api_password_handler)
    app_web.router.add_get("/api/settings/tokens", _api_get_worker_tokens)
    app_web.router.add_post("/api/settings/tokens", _api_save_worker_tokens)
    
    # Telegram Connect
    app_web.router.add_post("/api/tg/send_code", _api_tg_send_code)
    app_web.router.add_post("/api/tg/verify", _api_tg_verify_code)
    app_web.router.add_post("/api/tg/verify_2fa", _api_tg_verify_2fa)
    app_web.router.add_post("/api/tg/logout", _api_tg_logout)
    
    # Media & Streams
    app_web.router.add_get("/api/chats", _api_chats_handler)
    app_web.router.add_get("/api/topics", _api_topics_handler)
    app_web.router.add_post("/api/mediainfo", _api_mediainfo_web_handler)
    app_web.router.add_post("/api/spectrogram", _api_spectrogram_web_handler)
    app_web.router.add_get("/api/media_probe", _api_media_probe_handler)
    app_web.router.add_get("/api/playlist", _api_playlist_handler)
    app_web.router.add_get("/api/stream", _api_stream_handler)
    app_web.router.add_get("/api/direct_stream", _api_direct_stream_handler)
    app_web.router.add_get("/api/tg_stream", _api_tg_stream_handler)
    app_web.router.add_get("/api/subtitles", _api_subtitles_handler)
    app_web.router.add_get("/api/cover", _api_cover_handler)
    
    # Tasks & Watchers
    app_web.router.add_post("/api/task/add", _api_add_task)
    app_web.router.add_post("/api/task/cancel", _api_cancel_task)
    app_web.router.add_post("/api/watcher/add", _api_add_watcher)
    app_web.router.add_post("/api/watcher/cancel", _api_cancel_watcher)
    
    # Editor & Proxies
    app_web.router.add_post("/api/edit_media", _api_edit_media_handler)
    app_web.router.add_get("/api/editor_progress", _api_editor_progress)
    app_web.router.add_get("/api/bg", _api_bg_proxy)
    app_web.router.add_get("/api/proxy/country", _api_proxy_country)
    app_web.router.add_get("/api/proxy/wiki", _api_proxy_wiki)
    app_web.router.add_get("/api/chat_details", _api_chat_details_handler)
    
    # Admin Controls API
    async def _api_admin_get_users(request):
        try: uid = int(request.query.get("user_id", 0))
        except: uid = 0
        
        # 🟢 TOKEN CHECK
        token = request.query.get("token", "")
        user_doc = await db.col.find_one({"id": uid})
        if not user_doc or user_doc.get("web_token") != token:
            return web.json_response({"status": "error", "message": "Unauthorized: Invalid or expired Web Token."})
            
        if not await db.is_user_admin(uid):
            return web.json_response({"status": "error", "message": "Unauthorized"})
        
        effective_admins, effective_sudos, approved, _ = await db.get_access_control()
        
        # Consolidate users lowest-to-highest so highest privilege overwrites the dictionary
        users_dict = {}
        for x in approved: users_dict[x] = "User"
        for x in effective_sudos: users_dict[x] = "Sudo"
        for x in effective_admins: users_dict[x] = "Admin"
            
        user_data_list = []
        for a_id, role in users_dict.items():
            user_doc = await db.col.find_one({"id": a_id})
            name = user_doc.get("name", "Unknown User") if user_doc else "Unknown User"
            user_data_list.append({
                "id": a_id,
                "name": name,
                "role": role
            })
            
        return web.json_response({"status": "success", "users": user_data_list})

    async def _api_admin_add_user(request):
        data = await request.json()
        uid = int(data.get("user_id", 0))
        if not await db.is_user_admin(uid):
            return web.json_response({"status": "error", "message": "Unauthorized"})
        
        target = int(data.get("target_id", 0))
        role = data.get("role", "User")
        
        await db.add_approved_user(target, role)
        return web.json_response({"status": "success", "message": f"User {target} successfully assigned as {role}!"})

    async def _api_admin_remove_user(request):
        data = await request.json()
        uid = int(data.get("user_id", 0))
        if not await db.is_user_admin(uid):
            return web.json_response({"status": "error", "message": "Unauthorized"})
        target = int(data.get("target_id", 0))
        
        if target == uid:
            return web.json_response({"status": "error", "message": "You cannot remove yourself!"})
            
        await db.remove_user_access(target)
        return web.json_response({"status": "success", "message": f"User {target} removed!"})

    app_web.router.add_get("/api/admin/users", _api_admin_get_users)
    app_web.router.add_post("/api/admin/users/add", _api_admin_add_user)
    app_web.router.add_post("/api/admin/users/remove", _api_admin_remove_user)

    # Stop Media Task API
    async def _api_kill_stream(request):
        try:
            data = await request.json()
            uid = str(data.get("user_id", ""))
            
            if "GLOBAL_STREAM_TASKS" in globals() and uid:
                keys_to_delete = []
                for key, task in list(GLOBAL_STREAM_TASKS.items()):
                    if key.startswith(f"{uid}_"):
                        if not task.done():
                            task.cancel()
                        keys_to_delete.append(key)
                
                for k in keys_to_delete:
                    GLOBAL_STREAM_TASKS.pop(k, None)
                    
            return web.json_response({"status": "success", "message": "User streams killed cleanly."})
        except Exception as e:
            return web.json_response({"status": "error", "message": str(e)})

    app_web.router.add_post("/api/stream/kill", _api_kill_stream)
        
    # 🟢 FIX: 'access_log=None' officially kills the terminal web spam!
    runner = web.AppRunner(app_web, access_log=None) 
    await runner.setup()
    
    # 👇 CHANGE EXACTLY THIS LINE: Replace 'host' with '"0.0.0.0"'
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    
    await site.start()
    logger.info(f"🌐 Full-Stack Destiny TG Forwarder started on port {PORT}...")

# ==============================================================================
