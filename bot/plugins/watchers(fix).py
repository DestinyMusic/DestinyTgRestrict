# ==============================================================================
# --- WATCHER SETUP WIZARD ---
# ==============================================================================

@app.on_message(filters.command(["watch"]) & filters.private)
async def watch_setup(client: Client, message: Message):
    user_id = message.from_user.id
    if len(message.command) < 2:
        try:
            return await message.reply(
                "❌ **How to set up a Watcher:**\n\n"
                "This command tells the bot to monitor a channel, group, or PM and auto-forward new messages instantly.\n\n"
                "**Examples:**\n"
                "• Public Channel: `/watch https://t.me/channelname`\n"
                "• Private Chat: `/watch https://t.me/c/1234567890/1`\n"
                "• Bot/User PM: `/watch https://t.me/username/123` *(No @ symbol!)*\n"
                "• Specific Topic: `/watch https://t.me/channelname/5`"
            )
        except FloodWait: return
    
    link_text = message.command[1]
    try:
        wait_msg = await message.reply("🔎 **Analyzing Source...**", quote=True)
    except FloodWait as e:
        logger.warning(f"Silently blocked /watch init due to FloodWait: {e.value}s")
        return
        
    is_restricted, status_text = await check_link_restriction(user_id, link_text)
    try: await wait_msg.delete()
    except Exception: pass

    if is_restricted is None:
        return await message.reply(status_text, quote=True)
    
    parsed = _parse_source_link(link_text)
    source_thread_id = parsed.get("topic_id")
    
    PENDING_TASKS[user_id] = {
        "mode": "WATCHER", 
        "link": link_text,
        "source_thread_id": source_thread_id,
        "is_restricted": is_restricted,
        "status": "waiting_choice"
    }
    
    buttons = [
        [InlineKeyboardButton("📂 Send to DM (Here)", callback_data="dest_dm")],
        [InlineKeyboardButton("📢 Send to Channel/Group", callback_data="dest_custom")],
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel_setup")]
    ]
    
    await message.reply(
        f"👀 **Watcher Setup**\n\n"
        f"{status_text}\n"
        f"{(f'🔹 **Source Topic:** `{source_thread_id}` detected!' if source_thread_id else '')}\n\n"
        "**Where should new messages go?**",
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True
    )

@app.on_message(filters.command(["unwatch"]) & filters.private)
async def unwatch_handler(client, message):
    if len(message.command) not in (2, 3):
        try:
            return await message.reply(
                "❌ **How to stop a Live Watcher:**\n\n"
                "You need to provide the **Source ID** (the chat the bot is copying *from*).\n"
                "*(You can easily find this ID by sending the `/watchers` command!)*\n\n"
                "**Examples:**\n"
                "• Stop a channel/group: `/unwatch -100123456789`\n"
                "• Stop a specific topic: `/unwatch -100123456789 5`"
            )
        except FloodWait: return
    try:
        source_id = int(message.command[1])
        source_thread = int(message.command[2]) if len(message.command) == 3 else None
        user_id = message.from_user.id

        query = {"user_id": user_id, "source_id": source_id}
        if source_thread is not None:
            query["source_thread"] = source_thread
        else:
            query["$or"] = [{"source_thread": None}, {"source_thread": {"$exists": False}}]
            
        watcher = await db.db.watchers.find_one(query)

        if watcher and await db.remove_watcher(user_id, source_id, source_thread):
            stats = watcher.get("stats", {})
            cancelled_tasks = 0
            if user_id in ACTIVE_PROCESSES:
                for tid, info in list(ACTIVE_PROCESSES[user_id].items()):
                    if info.get("is_watcher") and info.get("source_id") == source_id:
                        CANCEL_FLAGS[tid] = True
                        cancelled_tasks += 1

            msg = (
                f"🛑 **Watcher Stopped & Removed!**\n\n"
                f"📊 **Final Session Statistics:**\n"
                f"├ 📡 **Total Detected:** `{stats.get('detected', 0)}`\n"
                f"├ ✅ **Successfully Processed:** `{stats.get('success', 0)}`\n"
                f"├ ⏭ **Skipped (Filtered):** `{stats.get('skipped', 0)}`\n"
                f"└ ❌ **Failed:** `{stats.get('failed', 0)}`"
            )
            if cancelled_tasks > 0:
                msg += f"\n\n🛑 Also intercepted and cancelled `{cancelled_tasks}` ongoing downloads from this watcher."
            try: await message.reply(msg)
            except FloodWait: pass
        else:
            try: await message.reply("⚠️ **Watcher not found.**\nMake sure you are providing the **Source ID** (where messages come *from*), not the Destination ID!")
            except FloodWait: pass
    except Exception as e:
        logger.error(f"Unwatch failed with input {message.command}: {e}", exc_info=True)
        try: await message.reply("❌ Invalid ID or Database Error.")
        except FloodWait: pass

@app.on_message(filters.command(["watchers"]) & filters.private)
async def list_watchers(client, message):
    user_id = message.from_user.id
    
    if user_id in ADMINS:
        cursor = await db.get_all_watchers()
    else:
        cursor = await db.get_user_watchers(user_id)
        
    user_watchers = await cursor.to_list(length=100)
    if not user_watchers:
        try: return await message.reply("💤 **No active watchers found.**")
        except FloodWait: return
    
    text = "**👀 Active Watchers Manager**\n\nSelect a watcher to remove:"
    buttons = []
    
    for w in user_watchers:
        src_id = w['source_id']
        src_display = w.get('source_title') or str(src_id)
        
        dest_id = w['dest_id']
        dst_display = w.get('dest_title') or str(dest_id)
        
        # 🟢 AUTO-RESOLVE DESTINATION NAME IF IT'S JUST A NUMERIC ID
        if dst_display == str(dest_id) or str(dst_display).lstrip("-").isdigit():
            if dest_id == user_id:
                dst_display = "Saved Messages"
            else:
                try:
                    # 🟢 FIX: Force peer resolution so the /watchers menu doesn't break after restart
                    try: await client.resolve_peer(dest_id)
                    except Exception: pass
                    
                    chat_info = await client.get_chat(dest_id)
                    dst_display = chat_info.title or chat_info.first_name or "Target Chat"
                except Exception:
                    # 🟢 FIX: If Main Bot is blind to the private group, ask the User Session!
                    owner_client = USER_CLIENTS.get(user_id)
                    if owner_client and getattr(owner_client, "is_connected", False):
                        try:
                            try: await owner_client.resolve_peer(dest_id)
                            except Exception: pass
                            
                            chat_info = await owner_client.get_chat(dest_id)
                            dst_display = chat_info.title or chat_info.first_name or "Target Chat"
                        except Exception:
                            pass
                            
                # Silently update DB so the name stays cached (Moved outside the try/except blocks)
                await db.db.watchers.update_one({"_id": w["_id"]}, {"$set": {"dest_title": dst_display}})
        
        if len(src_display) > 15: src_display = src_display[:12] + "..."
        if len(dst_display) > 15: dst_display = dst_display[:12] + "..."
        
        label = f"{src_display} ➔ {dst_display}"
        
        wid = str(w["_id"]) # Get unique DB ID
        callback = f"unwatch_{wid}"
        
        buttons.append([InlineKeyboardButton(f"🗑 {label}", callback_data=callback)])
    
    buttons.append([InlineKeyboardButton("🧨 Cancel All Watchers", callback_data="unwatch_all")])
    buttons.append([InlineKeyboardButton("❌ Close", callback_data="close_menu")])
    
    try: await message.reply(text, reply_markup=InlineKeyboardMarkup(buttons))
    except FloodWait as e: logger.warning(f"Blocked /watchers list due to FloodWait: {e.value}s")
    
@app.on_callback_query(filters.regex("^unwatch_"))
async def unwatch_callback(client, query):
    if query.data == "unwatch_all":
        user_id = query.from_user.id
        
        # Calculate combined stats before deleting
        cursor = db.db.watchers.find({'user_id': int(user_id)})
        t_det = t_suc = t_skip = t_fail = 0
        async for w in cursor:
            s = w.get("stats", {})
            t_det += s.get("detected", 0)
            t_suc += s.get("success", 0)
            t_skip += s.get("skipped", 0)
            t_fail += s.get("failed", 0)
            
        result = await db.db.watchers.delete_many({'user_id': int(user_id)})
        
        # Intercept and Cancel ALL Active Watcher Downloads
        cancelled_tasks = 0
        if user_id in ACTIVE_PROCESSES:
            for tid, info in list(ACTIVE_PROCESSES[user_id].items()):
                if info.get("is_watcher"):
                    CANCEL_FLAGS[tid] = True
                    cancelled_tasks += 1
                    
        msg = (
            f"🧨 **ALL Watchers Stopped & Removed!**\n"
            f"🗑 Removed `{result.deleted_count}` active watchers.\n\n"
            f"📊 **Combined Final Statistics:**\n"
            f"├ 📡 **Total Detected:** `{t_det}`\n"
            f"├ ✅ **Successfully Processed:** `{t_suc}`\n"
            f"├ ⏭ **Skipped (Filtered):** `{t_skip}`\n"
            f"└ ❌ **Failed:** `{t_fail}`"
        )
        if cancelled_tasks > 0:
            msg += f"\n\n🛑 Intercepted and Cancelled `{cancelled_tasks}` active watcher downloads."
        try: await query.message.edit(msg)
        except Exception: pass
        return

    # --- Delete Single Route by Unique MongoDB ID ---
    wid = query.data.split("_")[1]
    
    try:
        watcher = await db.db.watchers.find_one({"_id": ObjectId(wid)})
    except Exception:
        try: return await query.answer("Watcher not found or invalid ID.", show_alert=True)
        except Exception: return
        
    if not watcher:
        try: return await query.answer("Watcher already removed.", show_alert=True)
        except Exception: return

    owner_id = watcher["user_id"]
    source_id = watcher["source_id"]
    src_name = watcher.get('source_title') or str(source_id)
    dest_name = watcher.get('dest_title') or str(watcher.get('dest_id'))
    stats = watcher.get("stats", {})

    # Delete JUST this specific route!
    await db.db.watchers.delete_one({"_id": ObjectId(wid)})

    # Intercept and Cancel ongoing downloads tied to this source
    cancelled_tasks = 0
    if owner_id in ACTIVE_PROCESSES:
        for tid, info in list(ACTIVE_PROCESSES[owner_id].items()):
            if info.get("is_watcher") and info.get("source_id") == source_id:
                CANCEL_FLAGS[tid] = True
                cancelled_tasks += 1

    msg = (
        f"🛑 **Watcher Stopped & Removed!**\n\n"
        f"**From:** `{src_name}`\n"
        f"**To:** `{dest_name}`\n\n"
        f"📊 **Final Session Statistics:**\n"
        f"├ 📡 **Total Detected:** `{stats.get('detected', 0)}`\n"
        f"├ ✅ **Successfully Processed:** `{stats.get('success', 0)}`\n"
        f"├ ⏭ **Skipped (Filtered):** `{stats.get('skipped', 0)}`\n"
        f"└ ❌ **Failed:** `{stats.get('failed', 0)}`"
    )
    if cancelled_tasks > 0:
        msg += f"\n\n🛑 **Cancelled `{cancelled_tasks}` active ongoing downloads** originating from this watcher."
        
    try: await query.message.edit(msg)
    except Exception: pass

