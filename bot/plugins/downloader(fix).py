# ==============================================================================
# --- HANDLERS (START/HELP/STATUS/CANCEL/etc.) ---
# ==============================================================================

CACHED_WEB_URL = None

@app.on_message(filters.command(["start"]) & (filters.private | filters.group))
async def send_start(client: Client, message: Message):
    global CACHED_WEB_URL
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    if message.from_user.last_name:
        user_name += f" {message.from_user.last_name}"
    
    try:
        if not await db.is_user_exist(user_id):
            await db.add_user(user_id, user_name)
            logger.info(f"New user {user_id} saved to database.") 
        else:
            await db.col.update_one({"id": int(user_id)}, {"$set": {"name": user_name}})
    except Exception as e:
        logger.error(f"Failed to save user {user_id}: {e}", exc_info=True)

    welcome_video_url = "https://files.catbox.moe/o9azww.mp4"
    
    # 🟢 UNIVERSAL URL AUTO-DETECTOR (HuggingFace, Render, Koyeb, Railway, Oracle/VPS, Custom)
    if not CACHED_WEB_URL:
        raw_url = (
            os.environ.get("WEB_URL") or 
            os.environ.get("SPACE_HOST") or 
            os.environ.get("RENDER_EXTERNAL_URL") or 
            os.environ.get("KOYEB_PUBLIC_DOMAIN") or
            os.environ.get("RAILWAY_STATIC_URL")
        )
        
        if raw_url:
            raw_url = raw_url.rstrip("/")
            # Force HTTP/HTTPS prefix to prevent Telegram inline button crash
            if not raw_url.startswith("http://") and not raw_url.startswith("https://"):
                CACHED_WEB_URL = f"https://{raw_url}"
            else:
                CACHED_WEB_URL = raw_url
        else:
            # 🟢 ORACLE / VPS PUBLIC IP DETECTOR
            try:
                import urllib.request
                # Fetches the VPS Public IP and caches it forever so it's instantly ready
                public_ip = urllib.request.urlopen('https://api.ipify.org', timeout=3).read().decode('utf8')
                CACHED_WEB_URL = f"http://{public_ip}:{PORT}"
            except Exception as e:
                logger.warning(f"Could not detect public IP automatically: {e}")
                CACHED_WEB_URL = f"http://127.0.0.1:{PORT}"

    web_url = CACHED_WEB_URL

    welcome_text = (
        f"<b>👋 Hi {message.from_user.mention}, I am the Restricted Content Bot.</b>\n\n"
        "<blockquote expandable>"
        "<b>🛡 Features:</b>\n"
        "• Download Restricted Content\n"
        "• Setup Live Auto-Forwarders (Watchers)\n"
        "• Fast, Multi-Threaded Processing\n\n"
        "<b>🔑 Note:</b> For downloading private restricted content, you need to <code>/login</code> first.\n\n"
        "<b>📚 Know how to use the bot by sending /help</b>\n"
        "</blockquote>\n\n"
        f"<b>🌐 Web Dashboard:</b>\n"
        f"Control the bot, add tasks, and monitor active downloads directly from your browser:\n"
        f"🔗 <code>{web_url}</code>"
    )
    
    buttons = [
        [InlineKeyboardButton("🌐 Open Web Dashboard", url=web_url)],
        [InlineKeyboardButton("❣️ Developer", url="https://t.me/DestinyM66"), InlineKeyboardButton('🔍 Support', url='https://t.me/DestinyM66')]
    ]

    try:
        await client.send_video(
            chat_id=message.chat.id, 
            video=welcome_video_url, 
            caption=welcome_text, 
            reply_markup=InlineKeyboardMarkup(buttons),
            reply_to_message_id=message.id,
            parse_mode=enums.ParseMode.HTML
        )
    except FloodWait as e:
        logger.warning(f"Blocked /start video due to FloodWait: {e.value}s")
    except Exception:
        try:
            await client.send_message(
                chat_id=message.chat.id,
                text=welcome_text,
                reply_markup=InlineKeyboardMarkup(buttons),
                reply_to_message_id=message.id,
                parse_mode=enums.ParseMode.HTML,
                disable_web_page_preview=True
            )
        except FloodWait: pass

@app.on_message(filters.command(["help"]) & (filters.private | filters.group))
async def send_help(client: Client, message: Message):
    user_id = message.from_user.id
    
    # 1. The bot checks if the user is an Admin
    is_admin = user_id in ADMINS or user_id in SUDOS

    try:
        # 2. It sends the normal help guide to everyone
        await client.send_message(
            message.chat.id, 
            text=HELP_TXT,
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True
        )
        
        # 3. IF the user is an admin, it sends this secret menu too!
        if is_admin:
            await client.send_message(
                message.chat.id, 
                text=ADMIN_HELP_TXT,  # <--- Here is where your text gets used!
                parse_mode=enums.ParseMode.HTML,
                disable_web_page_preview=True
            )
    except FloodWait as e:
        logger.warning(f"Blocked /help due to FloodWait: {e.value}s")

@app.on_message(filters.command(["cancel"]) & (filters.private | filters.group))
async def send_cancel(client: Client, message: Message):
    user_id = message.from_user.id

    try:
        if user_id in PENDING_TASKS:
            del PENDING_TASKS[user_id]
            await message.reply("✅ **Setup process cancelled.** You can send a new link now.")
            return

        user_tasks = ACTIVE_PROCESSES.get(user_id, {})
        if not user_tasks:
            await message.reply(
                "✅ **Nothing to cancel!**\n\n"
                "You currently have no active downloads, setups, or background tasks running.\n\n"
                "💡 **Tip:** If you want to start a new download, just send `/dl <link>`."
            )
            return

        buttons = []
        for tid, info in list(user_tasks.items()):
            label = info.get("item", "Task")
            label_short = (label[:26] + "...") if len(label) > 29 else label
            buttons.append([InlineKeyboardButton(f"🛑 {label_short}", callback_data=f"cancel_task:{tid}")])
        buttons.append([InlineKeyboardButton("🛑 Cancel ALL My Tasks", callback_data="cancel_all")])
        buttons.append([InlineKeyboardButton("❌ Close Menu", callback_data="close_menu")])

        await message.reply(
            "**🚫 Cancel Tasks**\n\nSelect the task you want to cancel:",
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True
        )
    except FloodWait as e:
        logger.warning(f"Blocked /cancel menu due to FloodWait: {e.value}s")
    
@app.on_callback_query(filters.regex(r"^cancel_") | filters.regex(r"^cancel_task:"))
async def cancel_callback(client: Client, query):
    user_id = query.from_user.id
    data = query.data

    if data == "cancel_setup":
        if user_id in PENDING_TASKS:
            del PENDING_TASKS[user_id]
        cancel_text = (
            "❌ **Task Setup Cancelled**\n\n"
            "**What happened?**\n"
            "The configuration for this link has been discarded and cleared from my memory. No files were downloaded.\n\n"
            "💡 **Next Steps:**\n"
            "• Reply to a new link with `/dl` to start a new download.\n"
            "• Use `/watch` to set up an auto-forwarder.\n"
            "• Type `/help` for the master guide."
        )
        try: await query.message.edit(cancel_text)
        except Exception: pass
        return

    if data == "cancel_all":
        user_tasks = list(ACTIVE_PROCESSES.get(user_id, {}).keys())
        if not user_tasks:
            await query.answer("No active tasks to cancel.", show_alert=True)
            try: await query.message.delete()
            except: pass
            return
            
        for tid in user_tasks:
            CANCEL_FLAGS[tid] = True
        batch_temp.IS_BATCH[user_id] = True
        
        # 🟢 [DB WIPE] Failsafe: instantly remove from auto-resume DB
        try: await db.db.active_tasks.delete_many({"user_id": user_id})
        except: pass
        
        cancel_all_text = (
            "🛑 **Cancelling ALL Active Tasks...**\n\n"
            "**What is happening?**\n"
            "I am intercepting all your active downloads and uploads. It may take a few seconds to safely sever the TCP connections to Telegram's servers.\n\n"
            "🛡 **Why is this useful?**\n"
            "Cancelling heavy, stuck, or accidental batches frees up the server's bandwidth and clears your queue so you can start fresh."
        )
        try: await query.message.edit(cancel_all_text)
        except Exception: pass
        return

    if data.startswith("cancel_task:"):
        task_uuid = data.split(":",1)[1]
        user_tasks = ACTIVE_PROCESSES.get(user_id, {})
        if task_uuid not in user_tasks:
            await query.answer("Task not found or already finished.", show_alert=True)
            try: await query.message.delete()
            except: pass
            return
            
        CANCEL_FLAGS[task_uuid] = True
        task_name = user_tasks[task_uuid].get('item','Unknown Task')
        
        # 🟢 [DB WIPE] Failsafe: instantly remove this specific task from DB
        try: await db.remove_active_task(task_uuid)
        except: pass
        
        cancel_single_text = (
            f"🛑 **Task Cancelled Successfully!**\n\n"
            f"**Target:** `{task_name}`\n\n"
            f"**What happens now?**\n"
            f"The current file chunk will finish, and then the process will cleanly abort. Your other queued tasks (if any) will now speed up!"
        )
        try: await query.message.edit(cancel_single_text)
        except Exception: pass
        return
        
@app.on_callback_query(filters.regex("^close_menu"))
async def close_menu(client, query):
    try:
        await query.message.delete()
    except Exception:
        help_text = (
            "❌ **Menu Closed.**\n\n"
            "💡 **Quick Tips:**\n"
            "• `/dl` - Download from a link\n"
            "• `/watchers` - Manage live forwards\n"
            "• `/help` - Open the master guide"
        )
        try: await query.message.edit(help_text)
        except Exception: pass
    try: await query.answer("Closed.", show_alert=False)
    except Exception: pass

# --- LOGIN / LOGOUT (async login handler inserted) ---
# ==============================================================================

@app.on_message(filters.private & ~filters.forwarded & filters.command(["logout"]))
async def logout_cmd(client, message):
    user_id = message.from_user.id
    
    if not await db.is_user_exist(user_id):
        return await message.reply_text("You are not logged in.")
        
    user_session = await db.get_session(user_id)
    if not user_session:
        return await message.reply_text("You are not currently logged in. Nothing to log out of!")

    # 🎛 Create the Inline Confirmation Buttons
    buttons = [
        [InlineKeyboardButton("✅ Yes, Logout", callback_data="confirm_logout")],
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel_logout")]
    ]

    await message.reply(
        "⚠️ **Confirm Logout**\n\n"
        "Are you sure you want to log out? This will terminate your session and stop any active live watchers you have running.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_callback_query(filters.regex("^cancel_logout$"))
async def cancel_logout_cb(client, query):
    cancel_logout_text = (
        "✅ **Logout Cancelled!**\n\n"
        "**What does this mean?**\n"
        "Your Telegram session remains securely linked to the bot's database. \n\n"
        "🔒 **Security Note:** Because you did not log out, your active `/watch` monitors will continue running seamlessly in the background without interruption."
    )
    try: await query.message.edit(cancel_logout_text)
    except Exception: pass
    try: await query.answer("Session kept active.", show_alert=False)
    except Exception: pass

@app.on_callback_query(filters.regex("^confirm_logout$"))
async def confirm_logout_cb(client, query):
    user_id = query.from_user.id
    
    try: await query.message.edit("📡 **Connecting to Telegram to terminate session...**")
    except Exception: pass

    session_string = await db.get_session(user_id)
    api_id = await db.get_api_id(user_id)
    api_hash = await db.get_api_hash(user_id)

    if session_string:
        user_client = None
        try:
            use_api_id = int(api_id) if api_id else API_ID
            use_api_hash = api_hash if api_hash else API_HASH
            
            user_client = Client(
                ":memory:", 
                session_string=session_string, 
                api_id=use_api_id, 
                api_hash=use_api_hash,
                no_updates=True
            )
            
            await user_client.connect()
            
            try:
                await user_client.log_out()
                try: await query.message.edit("✅ **Session successfully removed from Telegram Devices.**")
                except Exception: pass
            except Exception as e:
                if "terminated" in str(e) or "Connection" in str(e):
                    try: await query.message.edit("✅ **Session terminated successfully.**")
                    except Exception: pass
                else:
                    raise e
            
        except AuthKeyUnregistered:
            try: await query.message.edit("⚠️ **Session was already invalid.** Cleaning local database...")
            except Exception: pass
        except Exception as e:
            logger.warning(f"Remote logout warning for {user_id}: {e}")
            try: await query.message.edit("✅ **Local session cleared.** (Remote session might already be gone)")
            except Exception: pass
        finally:
            try:
                if user_client and user_client.is_connected:
                    await user_client.disconnect()
            except Exception as e:
                logger.debug(f"Logout disconnect cleanup failed for {user_id}: {e}")

    # Shut down the running Pyrogram client if it's currently actively listening
    runtime_client = USER_CLIENTS.pop(user_id, None)
    if runtime_client:
        try:
            await runtime_client.stop()
        except Exception: pass

    # 🟢 Cancel all active batch tasks in memory
    user_tasks = list(ACTIVE_PROCESSES.get(user_id, {}).keys())
    for tid in user_tasks:
        CANCEL_FLAGS[tid] = True
    batch_temp.IS_BATCH[user_id] = True

    # 🟢 Wipe auto-resume tasks from the database so they don't resurrect
    try:
        await db.db.active_tasks.delete_many({"user_id": user_id})
    except Exception:
        pass

    # Clear the database
    await db.set_session(user_id, session=None)
    await db.set_api_id(user_id, api_id=None)
    await db.set_api_hash(user_id, api_hash=None)
    
    try: await query.message.reply("**Logout Complete** ♦\n(You are now disconnected. All active batch tasks have been cleanly cancelled.)")
    except Exception: pass
    try: await query.answer()
    except Exception: pass

from pyrogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

# --- UNIVERSAL LISTENER EXCEPTION MAPPING ---
try:
    from pyromod.exceptions import ListenerStopped
except ImportError:
    class ListenerStopped(Exception): pass

try:
    from pyrogram.errors import ListenerCanceled as NativeListenerStopped
except ImportError:
    class NativeListenerStopped(Exception): pass
# --------------------------------------------

@app.on_callback_query(filters.regex("^cancel_login$"))
async def cancel_login_cb(client, query):
    user_id = query.from_user.id
    
    # Attempt to kill the Pyromod or Native .ask() listener instantly
    try:
        if hasattr(client, "stop_listening"):
            await client.stop_listening(chat_id=user_id)
        elif hasattr(client, "cancel_listener"):
            client.cancel_listener(user_id)
        elif hasattr(client, "listen") and hasattr(client.listen, "cancel"):
            client.listen.cancel(user_id)
    except Exception:
        pass
        
    cancel_login_text = (
        "<b>❌ Login Process Aborted</b>\n\n"
        "<i>What happened?</i>\n"
        "You stopped the login setup. I have stopped waiting for your phone number or OTP. Your account remains completely safe, and no data was saved to the database.\n\n"
        "<i>What next?</i>\n"
        "You can continue using public bot features, or send <code>/login</code> whenever you are ready to try linking your account again."
    )
    try: await query.message.edit(cancel_login_text, parse_mode=enums.ParseMode.HTML)
    except Exception: pass
    try: await query.answer("Login Cancelled", show_alert=False)
    except Exception: pass
    
@app.on_message(filters.private & ~filters.forwarded & filters.command(["login"]))
async def login_handler(bot: Client, message: Message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        
    user_data = await db.get_session(message.from_user.id)
    if user_data is not None:
        await message.reply("⚠️ **You are already logged in!**\nPlease run `/logout` first if you want to switch accounts.")
        return  
        
    user_id = int(message.from_user.id)
    cancel_kb = InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel_login")]])
    client_auth = None

    try:
        # --- API CREDENTIALS ---
        if API_ID != 0 and API_HASH:
            await message.reply("🔑 **Specific API ID and HASH found in variables. Using them automatically...**")
            api_id, api_hash = API_ID, API_HASH
        else:
            api_id_msg = await bot.ask(user_id, "<b>Send Your API ID.</b>", filters=filters.text, timeout=300, reply_markup=cancel_kb)
            if api_id_msg.text.startswith('/'): return await api_id_msg.reply('<b>Process cancelled!</b>')
            try:
                api_id = int(api_id_msg.text)
                if api_id < 1000000 or api_id > 99999999:
                    return await api_id_msg.reply("**❌ Invalid API ID**\n\nPlease start again with /login.", quote=True)
            except ValueError:
                return await api_id_msg.reply("**❌ API ID must be a number!** Start over with /login.", quote=True)
            
            api_hash_msg = await bot.ask(user_id, "**Now Send Me Your API HASH**", filters=filters.text, timeout=300, reply_markup=cancel_kb)
            if api_hash_msg.text.startswith('/'): return await api_hash_msg.reply('<b>Process cancelled!</b>')
            api_hash = api_hash_msg.text.strip()
            
            if not re.fullmatch(r"[a-fA-F0-9]{32}", api_hash):
                return await api_hash_msg.reply("**❌ Invalid API HASH (Must be 32 Hex Characters)**\n\nPlease start again with /login.", quote=True)

        # --- PHONE NUMBER ---
        login_text = (
            "🔐 **Login Process Initiated**\n\n"
            "Please send your **Phone Number** in international format.\n"
            "Example: `+1234567890`\n\n"
            "🛡️ *Your session is stored securely locally.*"
        )
        phone_number_msg = await bot.ask(chat_id=user_id, text=login_text, filters=filters.text, timeout=300, reply_markup=cancel_kb)
        if phone_number_msg.text.startswith('/'): return await phone_number_msg.reply('<b>Process cancelled!</b>')
        
        phone_number = phone_number_msg.text.strip()
        if not re.fullmatch(r"\+\d{8,15}", phone_number):
            return await phone_number_msg.reply('❌ **Invalid phone number format.** Use international format (e.g., +1234567890).')
        
        # --- CONNECT TO TELEGRAM ---
        client_auth = Client(":memory:", api_id=api_id, api_hash=api_hash)
        await client_auth.connect()
        await phone_number_msg.reply("🔄 **Sending OTP request to Telegram...**")
        
        try:
            code = await client_auth.send_code(phone_number)
        except PhoneNumberInvalid:
            await phone_number_msg.reply('❌ **Phone Number is invalid!** Start over with /login.')
            await client_auth.disconnect()
            return
            
        # --- OTP RETRY LOOP ---
        while True:
            phone_code_msg = await bot.ask(
                user_id, 
                "Please check for an OTP in your official Telegram account. If you got it, send OTP here after reading the below format. \n\nIf OTP is `12345`, **please send it as** `1 2 3 4 5`.", 
                filters=filters.text, 
                timeout=300, 
                reply_markup=cancel_kb
            )
            
            if phone_code_msg.text.startswith('/'):
                await client_auth.disconnect()
                return await phone_code_msg.reply('<b>Process cancelled!</b>')
                
            raw_code = phone_code_msg.text.strip()
            
            # Catch the Telegram expiration instantly without the hacking explanation
            if raw_code.isdigit() and len(raw_code) >= 4:
                await phone_code_msg.reply("❌ **You sent the code without spaces!**\nTelegram has expired your code. You must run `/login` again to get a new code, and remember to use spaces (e.g., `1 2 3 4 5`).")
                await client_auth.disconnect()
                return
                
            phone_code = raw_code.replace(" ", "")
            
            try:
                await client_auth.sign_in(phone_number, code.phone_code_hash, phone_code)
                break # Success! Exit the OTP loop.
                
            except PhoneCodeInvalid:
                await phone_code_msg.reply('❌ **OTP is incorrect!** Please double-check the code and try again (with spaces).')
                continue # Loops back to ask for OTP again!
                
            except PhoneCodeExpired:
                await phone_code_msg.reply('⏳ **OTP Expired!** The official Telegram API only keeps auth codes valid for 5 minutes. Please run /login again to get a new code.')
                await client_auth.disconnect()
                return
                
            except SessionPasswordNeeded:
                # --- 2FA RETRY LOOP ---
                while True:
                    two_step_msg = await bot.ask(user_id, '**🔒 Account is protected by 2FA. Please enter your Two-Step Verification Password:**', filters=filters.text, timeout=300, reply_markup=cancel_kb)
                    
                    if two_step_msg.text.startswith('/'):
                        await client_auth.disconnect()
                        return await two_step_msg.reply('<b>Process cancelled!</b>')
                        
                    password = two_step_msg.text
                    try:
                        await client_auth.check_password(password=password)
                        break # Success! Exit 2FA loop.
                    except PasswordHashInvalid:
                        await two_step_msg.reply('❌ **Incorrect Password!** Please try again.')
                        continue # Loops back to ask for 2FA again!
                break # Break out of outer OTP loop since we solved 2FA

        # --- SUCCESSFUL LOGIN ---
        try:
            me_auth = await client_auth.get_me()
            # 🟢 ENFORCE ID MATCH: Prevent cross-account chat leaks!
            if me_auth.id != user_id:
                await bot.send_message(user_id, f"⚠️ **Telegram ID Mismatch!**\n\nYou are chatting with me using ID `{user_id}`, but the phone number you entered belongs to ID `{me_auth.id}`.\n\nTo prevent cross-account chat mix-ups, you must log in using the exact same account you are chatting from!")
                await client_auth.disconnect()
                return
            is_prem = getattr(me_auth, "is_premium", False)
            first_name = me_auth.first_name or "User"
        except Exception:
            is_prem = False
            first_name = "User"

        string_session = await client_auth.export_session_string()
        await client_auth.disconnect()
        
        if len(string_session) < SESSION_STRING_SIZE:
            return await bot.send_message(user_id, '❌ **Fatal Error:** Invalid session string generated.')
            
        await db.set_session(user_id, session=string_session)
        await db.set_api_id(user_id, api_id=api_id)
        await db.set_api_hash(user_id, api_hash=api_hash)
        
        prem_text = "⭐ <b>Telegram Premium:</b> <code>Active (4GB Uploads Enabled)</code>" if is_prem else "🔹 <b>Account Type:</b> <code>Standard (2GB Upload Limit)</code>"

        success_msg = (
            f"✅ <b>Account Login Successful!</b>\n\n"
            f"👤 <b>Logged in as:</b> <code>{first_name}</code>\n"
            f"{prem_text}\n\n"
            f"<i>If you encounter any AUTH KEY errors later, run /logout and /login again.</i>"
        )
        await bot.send_message(user_id, success_msg, parse_mode=enums.ParseMode.HTML)

    # --- ERROR HANDLERS ---
    except (ListenerStopped, NativeListenerStopped, asyncio.CancelledError):
        # Silently caught when Cancel button is pressed or task is natively cancelled by the fork
        if client_auth and client_auth.is_connected:
            try: await client_auth.disconnect()
            except: pass
        return
        
    except asyncio.TimeoutError:
        # 5 Minute Limit Reached
        timeout_msg = (
            "⏱ **Login Session Timed Out!**\n\n"
            "**Why did this happen?**\n"
            "You took longer than 5 minutes to reply to a prompt. To save server RAM and maintain security, the bot automatically closed the login listener.\n\n"
            "🔄 **Fix:** Please gather your API ID, Hash, and Phone Number, and send `/login` to start fresh."
        )
        await bot.send_message(user_id, timeout_msg)
        if client_auth and client_auth.is_connected:
            try: await client_auth.disconnect()
            except: pass
        return
        
    except Exception as e:
        await bot.send_message(user_id, f"<b>❌ ERROR IN LOGIN:</b> `{e}`", parse_mode=enums.ParseMode.HTML)
        if client_auth and client_auth.is_connected:
            try: await client_auth.disconnect()
            except: pass

# ==============================================================================
# --- CORE: receive links / start tasks / processing / cancel checks ---
# ==============================================================================

@app.on_message((filters.text | filters.caption) & filters.private & ~filters.command(ALL_COMMANDS))
async def save(client: Client, message: Message):
    # 🟢 WZGRAM FALLBACK FIX: Prevent capturing unknown commands as links!
    text_content = message.text or message.caption or ""
    if text_content.startswith("/"):
        return
        
    user_id = message.from_user.id
    if user_id in PENDING_TASKS:
        if PENDING_TASKS[user_id].get("status") == "waiting_id":
            await process_custom_destination(client, message)
            return
        if PENDING_TASKS[user_id].get("status") == "waiting_speed_input": # <<< FIX
            await process_speed_input(client, message)
            return

    link_text = message.text or message.caption
    if not link_text or "https://t.me/" not in link_text:
        return

    try:
        wait_msg = await message.reply("🔎 **Analyzing Link...**", quote=True)
    except FloodWait as e:
        logger.warning(f"Silently blocked link analysis due to FloodWait: {e.value}s")
        return

    is_restricted, status_text = await check_link_restriction(user_id, link_text)
    try: await wait_msg.delete()
    except Exception: pass

    if is_restricted is None:
        return await message.reply(status_text, quote=True)

    PENDING_TASKS[user_id] = {
        "link": link_text, 
        "status": "waiting_choice",
        "is_restricted": is_restricted 
    }
    
    buttons = [
        [InlineKeyboardButton("📂 Send to DM (Here)", callback_data="dest_dm")],
        [InlineKeyboardButton("📢 Send to Channel/Group", callback_data="dest_custom")],
        [InlineKeyboardButton("🛠 Inspect & Edit Media", callback_data="dest_remux")],
        [InlineKeyboardButton("❌ Cancel Setup", callback_data="cancel_setup")]
    ]

@app.on_callback_query(filters.regex("^dest_remux$"))
async def remux_tg_callback(client: Client, query):
    user_id = query.from_user.id
    if user_id not in PENDING_TASKS: return await query.answer("Expired.", show_alert=True)
    link = PENDING_TASKS[user_id]["link"]
    
    await query.message.edit("🔎 **Probing Media Tracks...**")
    
    try:
        is_tg = _is_tg_link(link)
        if is_tg:
            parsed = _parse_source_link(link)
            probe_url = f"http://127.0.0.1:{PORT}/api/tg_stream?user_id={user_id}&chat_id={parsed['chat_id']}&msg_id={parsed['msg_id']}"
        else:
            from urllib.parse import quote
            probe_url = f"http://127.0.0.1:{PORT}/api/direct_stream?user_id={user_id}&url={quote(link, safe='')}"
            
        pdata = await _run_ffprobe_json(probe_url, fast=True)
        streams = pdata.get("streams", [])
        
        text = "🛠 **Media Inspector & Editor**\n\n**Available Tracks:**\n"
        for s in streams:
            idx = s.get("index")
            c_type = s.get("codec_type", "unknown").upper()
            c_name = s.get("codec_name", "")
            lang = s.get("tags", {}).get("language", "")
            title = s.get("tags", {}).get("title", "")
            text += f"• `{idx}` : **{c_type}** ({c_name}) {lang} *{title}*\n"
            
        text += "\n✏️ **Reply with your configuration.**\nFormat: `index: title=New Name, delay=500` separated by `|`.\n*Example:* `0 | 1: title=English Dub, delay=-200 | 2`\n\n*(Send /cancel to abort)*"
        
        config_msg = await app.ask(user_id, text, timeout=300)
        if config_msg.text.startswith('/'): return await config_msg.reply("Cancelled.")
        
        raw_config = config_msg.text.split('|')
        parsed_config = []
        for track in raw_config:
            parts = track.split(':')
            track_dict = {"index": parts[0].strip()}
            if len(parts) > 1:
                opts = parts[1].split(',')
                for opt in opts:
                    if '=' in opt:
                        k, v = opt.split('=', 1)
                        track_dict[k.strip().lower()] = v.strip()
            parsed_config.append(track_dict)
            
        name_msg = await app.ask(user_id, "✏️ **Send the NEW File Name (with extension like .mkv):**\n*(Or send `skip` to keep the original name)*", timeout=120)
        if name_msg.text.startswith('/'): return await name_msg.reply("Cancelled.")
        
        PENDING_TASKS[user_id]["remux_config"] = parsed_config
        PENDING_TASKS[user_id]["remux_name"] = name_msg.text.strip()
        
        up_btns = [
            [InlineKeyboardButton("📤 Send to Telegram DM", callback_data="up_tg_remux")],
            [InlineKeyboardButton("☁️ Upload to GoFile.io", callback_data="up_gf_remux")]
        ]
        await name_msg.reply("🚀 **Where do you want to upload the finished file?**", reply_markup=InlineKeyboardMarkup(up_btns))
        
    except Exception as e:
        await query.message.reply(f"❌ Error: {e}")

@app.on_callback_query(filters.regex(r"^up_(tg|gf)_remux$"))
async def execute_remux_callback(client: Client, query):
    user_id = query.from_user.id
    dest_type = query.data.split("_")[1]
    task_data = PENDING_TASKS.get(user_id)
    if not task_data: return await query.answer("Expired.", show_alert=True)
    
    status_msg = await query.message.edit("⚙️ **Processing Media...**\n1️⃣ Downloading...\n2️⃣ Remuxing...\n3️⃣ Uploading...")
    
    import time
    from pathlib import Path
    import shutil
    
    temp_dir = Path(f"./temp_remux_{user_id}_{int(time.time())}")
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    new_name = task_data["remux_name"] if task_data["remux_name"].lower() != "skip" else "Edited_Media.mkv"
    input_file = temp_dir / "input_media.dat"
    output_file = temp_dir / sanitize_filename(new_name)
    
    try:
        is_tg = _is_tg_link(task_data["link"])
        if is_tg:
            parsed = _parse_source_link(task_data["link"])
            uclient = USER_CLIENTS.get(user_id)
            if not uclient or not uclient.is_connected:
                session_str = await db.get_session(user_id)
                u_api = await db.get_api_id(user_id) or API_ID
                u_hash = await db.get_api_hash(user_id) or API_HASH
                uclient = Client(f"User_{user_id}", session_string=session_str, api_id=u_api, api_hash=u_hash, ipv6=False)
                await uclient.start()
                USER_CLIENTS[user_id] = uclient
            msg = await uclient.get_messages(parsed["chat_id"], parsed["msg_id"])
            await uclient.download_media(msg, file_name=str(input_file))
        else:
            await full_download_http(task_data["link"], str(input_file))
            
        await status_msg.edit("⚙️ **Remuxing Tracks (Instant Copy)...**")
        await process_remux(str(input_file), str(output_file), task_data["remux_config"])
        
        await status_msg.edit("☁️ **Uploading to Destination...**")
        if dest_type == "gf":
            url = await upload_to_gofile(str(output_file))
            await status_msg.edit(f"✅ **Success! Uploaded to GoFile.**\n\n🔗 **Link:** {url}", disable_web_page_preview=True)
        else:
            await app.send_document(chat_id=user_id, document=str(output_file), caption=f"✅ **Remuxed:** {new_name}")
            await status_msg.delete()
            
    except Exception as e:
        await status_msg.edit(f"❌ **Error:** {str(e)}")
    finally:
        shutil.rmtree(str(temp_dir), ignore_errors=True)
    
    await message.reply(
        f"✨ **Link Detected!**\n\n"
        f"{status_text}\n\n"
        "Where should I send the files?",
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True
    )

@app.on_message(filters.command(["chats"]) & filters.private)
async def chats_cmd(client: Client, message: Message):
    user_id = message.from_user.id
    args = message.command[1:] if len(message.command) > 1 else []
    
    # 🟢 1. CLEAN WARNING IF NOT LOGGED IN / NO SESSION IN DB
    session_str = await db.get_session(user_id)
    if not session_str:
        not_logged_in_text = (
            "<b>⚠️ TELEGRAM SESSION NOT CONNECTED</b>\n\n"
            "<blockquote expandable>"
            "You cannot fetch your chat IDs because your personal Telegram account is not linked to this bot yet!\n\n"
            "💡 <b>How to Connect:</b>\n"
            "• <b>Via Telegram:</b> Send <code>/login</code> and follow the prompts.\n"
            "• <b>Via Web Portal:</b> Open <b>Settings</b> and enter your phone number to sign in.\n\n"
            "<i>Once connected, send <code>/chats</code> again to explore all your chat IDs.</i>"
            "</blockquote>"
        )
        return await message.reply(not_logged_in_text, parse_mode=enums.ParseMode.HTML)

    # 🟢 2. BEAUTIFUL HELP MENU (WHEN RUN WITHOUT ARGUMENTS)
    if not args:
        help_menu = (
            "<b>💬 CHATS & CHANNELS EXPLORER</b>\n"
            "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬✘▬\n"
            "<blockquote expandable>"
            "Quickly extract chat, channel, group, and bot IDs associated with your logged-in account. You can copy these IDs directly to use in <code>/watch</code> or <code>/dl</code>!\n\n"
            "<b>📑 COMMAND ARGUMENTS</b>\n"
            "• <code>/chats all</code> - <i>Fetch all categories</i>\n"
            "• <code>/chats group</code> - <i>Fetch Groups & Supergroups only</i>\n"
            "• <code>/chats channel</code> - <i>Fetch Broadcast Channels only</i>\n"
            "• <code>/chats bot</code> - <i>Fetch Direct Bots only</i>\n"
            "• <code>/chats user</code> - <i>Fetch Direct User PMs only</i>\n\n"
            "🛡 <b>Flood Protection:</b> Results are delivered in pages of 50 with an automated 6-second interval between pages."
            "</blockquote>\n"
            "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬✘▬"
        )
        return await message.reply(help_menu, parse_mode=enums.ParseMode.HTML)

    filter_type = args[0].lower()
    if filter_type not in ["all", "user", "bot", "group", "channel"]:
        return await message.reply("❌ **Invalid argument.** Please use: `all`, `group`, `channel`, `bot`, or `user`.")

    uclient = USER_CLIENTS.get(user_id)
    
    # 🟢 3. DYNAMIC WAKE-UP FOR INTERRUPTED SESSIONS
    if not uclient or not uclient.is_connected:
        status = await message.reply("🔄 <b>Connecting your Telegram session...</b>", parse_mode=enums.ParseMode.HTML)
        try:
            api_id = await db.get_api_id(user_id) or API_ID
            api_hash = await db.get_api_hash(user_id) or API_HASH
            uclient = Client(f"User_{user_id}", session_string=session_str, api_id=api_id, api_hash=api_hash, workers=4, ipv6=False)
            uclient.add_handler(MessageHandler(user_watcher_handler, is_watched_chat))
            await uclient.start()
            USER_CLIENTS[user_id] = uclient
            await status.edit("🔄 <b>Session Active! Fetching your dialogs...</b>", parse_mode=enums.ParseMode.HTML)
        except Exception as e:
            return await status.edit(f"❌ <b>Session Expired or Broken:</b> <code>{e}</code>\nPlease run <code>/logout</code> and <code>/login</code> again.")
    else:
        status = await message.reply("🔄 <b>Fetching your chats... Please wait</b>", parse_mode=enums.ParseMode.HTML)

    users, groups, channels, bots = [], [], [], []

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
                    category = ""
                    
                    if chat_id > 0:
                        u = resolved_users.get(chat_id)
                        if u:
                            title = getattr(u, "first_name", None)
                            if not title:
                                title = "Unknown User"
                            if getattr(u, "last_name", None):
                                title += f" {u.last_name}"
                            category = "bot" if getattr(u, "bot", False) else "private"
                    else:
                        c = resolved_chats.get(abs(chat_id)) or resolved_chats.get(getattr(peer, "channel_id", 0)) or resolved_chats.get(getattr(peer, "chat_id", 0))
                        if c:
                            title = getattr(c, "title", None)
                            if not title:
                                title = "Unknown Group"
                            category = "channel" if getattr(c, "broadcast", False) else "group"

                    line = f"• <b>{html.escape(title)}</b> │ <code>{chat_id}</code>"
                    
                    if "group" in category or "supergroup" in category: groups.append(line)
                    elif "channel" in category: channels.append(line)
                    elif "bot" in category: bots.append(line)
                    elif "private" in category: users.append(line)

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

    try:
        await execute_raw_pagination(0) # Standard Chats
        await execute_raw_pagination(1) # Archived Chats
    except Exception as e:
        return await status.edit(f"❌ <b>Error reading dialogs:</b> <code>{e}</code>", parse_mode=enums.ParseMode.HTML)

    await status.delete()

    def chunk_list(items, chunk_size=50):
        return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]
        
    categories = []
    if filter_type in ["all", "group"]: categories.append(("👥 Groups & Supergroups List", "👥", groups))
    if filter_type in ["all", "channel"]: categories.append(("📢 Channels List", "📢", channels))
    if filter_type in ["all", "bot"]: categories.append(("🤖 Telegram Bots List", "🤖", bots))
    if filter_type in ["all", "user"]: categories.append(("👤 Users List", "👤", users))

    found_any = False
    for title, emoji, items in categories:
        if not items:
            continue
        found_any = True
        chunks = chunk_list(items, 50)
        total_pages = len(chunks)
        
        for i, chunk in enumerate(chunks, 1):
            text = (
                f"<b>{emoji} {title} (Page {i}/{total_pages})</b>\n"
                f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬✘▬\n"
                f"<blockquote expandable>\n"
                + "\n".join(chunk) +
                f"\n</blockquote>\n"
                f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬✘▬"
            )
            await message.reply(text, parse_mode=enums.ParseMode.HTML)
            if i < total_pages or len(categories) > 1:
                await asyncio.sleep(6) # Safe 6-second rate limit pause

    if not found_any:
        await message.reply(f"⚠️ No active dialogs found matching filter: <b>{filter_type}</b>", parse_mode=enums.ParseMode.HTML)

@app.on_message(filters.command(["dl"]) & (filters.private | filters.group))
async def dl_handler(client: Client, message: Message):
    user_id = message.from_user.id
    link_text = ""
    
    reply = message.reply_to_message
    if reply and (reply.text or reply.caption):
        link_text = reply.text or reply.caption
    elif len(message.command) > 1:
        link_text = message.text.split(None, 1)[1]
        
    if not link_text or "https://t.me/" not in link_text:
        try:
            await message.reply_text(
                "❌ **How to use the Downloader:**\n\n"
                "Use this command to download or forward files from any Telegram link.\n\n"
                "**Examples:**\n"
                "• Channel File: `/dl https://t.me/channel/100`\n"
                "• Batch Files: `/dl https://t.me/channel/101 - 120`\n"
                "• Bot/User PM: `/dl https://t.me/username/123` *(No @ symbol!)*\n"
                "• Quick Reply: Just **reply** to any message containing a link with `/dl`"
            )
        except FloodWait: pass
        return

    try:
        wait_msg = await message.reply("🔎 **Analyzing Link...**", quote=True)
    except FloodWait as e:
        logger.warning(f"Silently blocked /dl init due to FloodWait: {e.value}s")
        return

    is_restricted, status_text = await check_link_restriction(user_id, link_text)
    try: await wait_msg.delete()
    except Exception: pass

    if is_restricted is None:
        return await message.reply(status_text, quote=True)

    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        dest_title = message.chat.title or "This Group"
        if message.message_thread_id:
            dest_title += await get_topic_title(client, message.chat.id, message.message_thread_id)
            
        PENDING_TASKS[user_id] = {
            "link": link_text,
            "dest_chat_id": message.chat.id,
            "dest_thread_id": message.message_thread_id,
            "dest_title": dest_title,
            "status": "waiting_speed_choice", # <<< FIX
            "is_restricted": is_restricted
        }
        await message.reply(f"✨ **Link Analyzed!**\n{status_text}", quote=True)
        await ask_for_speed(message)
        return

    PENDING_TASKS[user_id] = {
        "link": link_text, 
        "status": "waiting_choice",
        "is_restricted": is_restricted
    }
    
    buttons = [
        [InlineKeyboardButton("📂 Send to DM (Here)", callback_data="dest_dm")],
        [InlineKeyboardButton("📢 Send to Channel/Group", callback_data="dest_custom")],
        [InlineKeyboardButton("❌ Cancel Setup", callback_data="cancel_setup")] 
    ]
    
    await message.reply(
        f"✨ **Link Detected!**\n\n"
        f"{status_text}\n\n"
        "I am ready to process this content. Please tell me where you want the files sent:",
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True
    )
    
@app.on_callback_query(filters.regex("^dest_"))
async def destination_callback(client: Client, query):
    user_id = query.from_user.id
    if user_id not in PENDING_TASKS:
        try: return await query.answer("❌ Task expired. Send link again.", show_alert=True)
        except Exception: return
    choice = query.data
    
    if choice == "dest_dm":
        PENDING_TASKS[user_id]["dest_chat_id"] = user_id
        PENDING_TASKS[user_id]["dest_thread_id"] = None
        PENDING_TASKS[user_id]["dest_title"] = "Saved Messages"
        PENDING_TASKS[user_id]["status"] = "waiting_speed_choice" # <<< FIX
        await ask_for_speed(query)
    elif choice == "dest_custom":
        PENDING_TASKS[user_id]["status"] = "waiting_id"
        buttons = [[InlineKeyboardButton("❌ Cancel", callback_data="cancel_setup")]]
        try:
            await query.message.edit_text(
                "📝 **Send the Target Chat ID**\n\n"
                "Examples:\n"
                "• Channel/Group: `-100123456789`\n"
                "• Specific Topic: `-100123456789/5`\n\n"
                "⚠️ __Make sure I am an admin in that chat!__",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        except Exception: pass

def get_filter_keyboard(current_types):
    buttons = []
    row = []
    for t in ALL_MSG_TYPES:
        icon = "✅" if t in current_types else "❌"
        row.append(InlineKeyboardButton(f"{icon} {t}", callback_data=f"filter_toggle:{t}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row: buttons.append(row)
    buttons.append([
        InlineKeyboardButton("✅ Select All", callback_data="filter_all"), 
        InlineKeyboardButton("❌ Clear All", callback_data="filter_none")
    ])
    buttons.append([InlineKeyboardButton("🚀 Proceed / Save Setup", callback_data="filter_start")])
    buttons.append([InlineKeyboardButton("🛑 Cancel Setup", callback_data="cancel_setup")])
    return InlineKeyboardMarkup(buttons)

async def show_filter_menu(message_or_query, user_id):
    task_data = PENDING_TASKS.get(user_id)
    if not task_data:
        return

    if "allowed_types" not in task_data:
        task_data["allowed_types"] = ALL_MSG_TYPES.copy()
    task_data["status"] = "waiting_filter"

    kb = get_filter_keyboard(task_data["allowed_types"])
    text = "🎛 **Content Filter**\n\nSelect the media types you want to forward or download.\n*(Default: Strictly Videos & Documents)*"

    if hasattr(message_or_query, "message") and hasattr(message_or_query, "data"):
        await message_or_query.message.edit_text(text, reply_markup=kb)
    else:
        await message_or_query.reply(text, reply_markup=kb, quote=True)

@app.on_callback_query(filters.regex("^filter_toggle:(.+)"))
async def filter_toggle_cb(client, query):
    user_id = query.from_user.id
    if user_id not in PENDING_TASKS: return await query.answer("Expired.", show_alert=True)
    mtype = query.data.split(":")[1]
    allowed = PENDING_TASKS[user_id].get("allowed_types", ["Video", "Document"])
    if mtype in allowed: allowed.remove(mtype)
    else: allowed.append(mtype)
    PENDING_TASKS[user_id]["allowed_types"] = allowed
    try: await query.message.edit_reply_markup(get_filter_keyboard(allowed))
    except: pass
    await query.answer()

@app.on_callback_query(filters.regex("^filter_all$"))
async def filter_all_cb(client, query):
    user_id = query.from_user.id
    if user_id not in PENDING_TASKS: return await query.answer("Expired.", show_alert=True)
    PENDING_TASKS[user_id]["allowed_types"] = ALL_MSG_TYPES.copy()
    try: await query.message.edit_reply_markup(get_filter_keyboard(ALL_MSG_TYPES))
    except: pass
    await query.answer()

@app.on_callback_query(filters.regex("^filter_none$"))
async def filter_none_cb(client, query):
    user_id = query.from_user.id
    if user_id not in PENDING_TASKS: return await query.answer("Expired.", show_alert=True)
    PENDING_TASKS[user_id]["allowed_types"] = []
    try: await query.message.edit_reply_markup(get_filter_keyboard([]))
    except: pass
    await query.answer()

@app.on_callback_query(filters.regex("^filter_start$"))
async def filter_start_cb(client, query):
    user_id = query.from_user.id
    if user_id not in PENDING_TASKS: return await query.answer("Expired.", show_alert=True)
    
    task_data = PENDING_TASKS.pop(user_id)
    allowed_types = task_data.get("allowed_types", ["Video", "Document"])
    
    if not allowed_types: 
        PENDING_TASKS[user_id] = task_data 
        return await query.answer("❌ Select at least one type!", show_alert=True)
        
    delay = max(3, min(int(task_data.get("delay", 3) or 3), 3600))
    if task_data.get("mode") == "WATCHER":
        await finalize_watcher_setup(client, query.message, task_data, delay, user_id=user_id)
    else:
        await start_task_final(client, query.message, task_data, delay, user_id=user_id)

async def process_custom_destination(client: Client, message: Message):
    user_id = message.from_user.id
    text = (message.text or "").strip()

    try:
        if message.reply_to_message and message.reply_to_message.from_user and message.reply_to_message.from_user.is_self:
            await message.reply_to_message.delete()
    except Exception:
        pass

    try:
        dest_chat_id, dest_thread_id = _parse_chat_target(text)

        try:
            # 🟢 FIX: Resolve peer before fetching info so custom destinations work after restarts
            try: await client.resolve_peer(dest_chat_id)
            except Exception: pass
            
            # Resolve basic info
            chat = await client.get_chat(dest_chat_id)
            title = chat.title or chat.first_name or "Target Chat"
            if dest_thread_id: 
                title += await get_topic_title(client, dest_chat_id, dest_thread_id)

            # 🟢 CHECK ACCESS ACROSS ALL CLIENTS (Main Bot, Workers, User)
            main_bot_access = False
            try:
                bot_member = await client.get_chat_member(chat.id, "me")
                main_bot_access = bot_member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]
            except Exception: pass

            worker_bots = USER_WORKER_BOTS.get(user_id, [])
            worker_access_count = 0
            for wb in worker_bots:
                try:
                    if not getattr(wb, "is_connected", False): await wb.connect()
                    wb_member = await wb.get_chat_member(chat.id, "me")
                    if wb_member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
                        worker_access_count += 1
                except Exception: pass

            user_access = False
            uclient = USER_CLIENTS.get(user_id)
            if uclient and getattr(uclient, "is_connected", False):
                try:
                    await uclient.get_chat(chat.id)
                    user_access = True
                except Exception: pass

            # Failsafe: if it's a DM, bots/users can usually write to it without admin rights
            is_dm = str(dest_chat_id).lstrip("-").isdigit() and not str(dest_chat_id).startswith("-100") and int(dest_chat_id) > 0
            
            if not is_dm and not main_bot_access and worker_access_count == 0 and not user_access:
                await message.reply(
                    "❌ **Destination Error:** Neither I, your Worker Bots, nor your User Session have admin access to that chat!\n\n"
                    "Please add us to the destination chat/channel and promote us to **Admin**."
                )
                return

            if not is_dm and worker_bots and worker_access_count == 0:
                await message.reply(
                    f"⚠️ **Worker Bot Warning:** You have `{len(worker_bots)}` Worker Bots configured, but **none** of them are Admins in the destination.\n\n"
                    "I will automatically fallback to your User Session for uploads. To maximize speed, please add your Worker Bots to the destination and make them Admins."
                )

            # --- ACTIVE DESTINATION TEST (using the best available client) ---
            test_client = None
            if worker_access_count > 0:
                for wb in worker_bots:
                    if getattr(wb, "is_connected", False):
                        test_client = wb
                        break
            if not test_client and main_bot_access: test_client = client
            if not test_client and user_access: test_client = uclient

            if test_client:
                try:
                    test_msg = await test_client.send_message(
                        chat_id=dest_chat_id,
                        text="🔄 Testing Destination Accessibility...\n*(This message will self-destruct)*",
                        message_thread_id=dest_thread_id
                    )
                    await asyncio.sleep(1.5)
                    await test_msg.delete()
                except Exception as e:
                    await message.reply(f"❌ **Destination Write Error:** Access granted, but I cannot send messages to that specific topic/chat! (Check topic permissions)\nError: `{e}`")
                    return
            
        except Exception as e:
            await message.reply(f"❌ **Could not access Destination.**\nMake sure I am added to the chat and given admin rights.\nError: `{e}`")
            return

        PENDING_TASKS[user_id]["dest_chat_id"] = chat.id
        PENDING_TASKS[user_id]["dest_thread_id"] = dest_thread_id
        PENDING_TASKS[user_id]["dest_title"] = title
        PENDING_TASKS[user_id]["status"] = "waiting_speed_choice"
        await ask_for_speed(message)

    except ValueError:
        await message.reply("❌ Invalid ID format. Send `-100...`, `-100.../5`, `@username`, or a `t.me` link.")

async def ask_for_speed(message_or_query):
    user_id = message_or_query.from_user.id
    task_data = PENDING_TASKS.get(user_id, {})
    mode = task_data.get("mode")

    buttons = []
    if mode == "WATCHER":
                buttons.append([InlineKeyboardButton("⏳ Default (3s)", callback_data="speed_3")])
    else:
        buttons.append([InlineKeyboardButton("⚡ Default (3s)", callback_data="speed_3")])
        
    buttons.append([InlineKeyboardButton("⚙️ Manual Speed", callback_data="speed_manual")])
    buttons.append([InlineKeyboardButton("❌ Cancel", callback_data="cancel_setup")])
    
    text = "**🚀 Select Forwarding Speed**\n\nHow fast should I process messages?"

    if hasattr(message_or_query, "message") and hasattr(message_or_query, "data"):
        await message_or_query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await message_or_query.reply(text, reply_markup=InlineKeyboardMarkup(buttons), quote=True)

@app.on_callback_query(filters.regex("^speed_"))
async def speed_callback(client: Client, query):
    user_id = query.from_user.id
    if user_id not in PENDING_TASKS:
        try: await query.answer("❌ Task expired.", show_alert=True)
        except Exception: pass
        return
    
    choice = query.data
    task_data = PENDING_TASKS[user_id]
    
    if choice == "speed_manual":
        PENDING_TASKS[user_id]["status"] = "waiting_speed_input"
        try:
            await query.message.edit(
                "⏱ **Enter Delay (Seconds)**\n\n"
                "Every time a new message arrives, I will wait this long before forwarding it.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel_setup")]])
            )
        except Exception: pass
        return

    if choice in ["speed_3", "speed_default"]:
        PENDING_TASKS[user_id]["delay"] = 3
        await show_filter_menu(query, user_id)
        return

async def process_speed_input(client: Client, message: Message):
    user_id = message.from_user.id
    text = message.text.strip()
    if not text.isdigit(): return await message.reply("❌ Numbers only.")
    
    delay = max(3, min(int(text), 3600)) 
    if user_id in PENDING_TASKS:
        PENDING_TASKS[user_id]["delay"] = delay
        await show_filter_menu(message, user_id)

async def finalize_watcher_setup(client, message, data, delay, user_id=None):
    delay = max(3, min(int(delay or 3), 3600))
    if user_id is None:
        user_id = message.from_user.id if message.from_user else message.chat.id
    src_link = data["link"]

    user_session = await db.get_session(user_id)
    
    api_id = await db.get_api_id(user_id) or API_ID
    api_hash = await db.get_api_hash(user_id) or API_HASH

    if user_session and user_id not in USER_CLIENTS:
        status_msg = await message.reply("🔄 **Starting your Listener Client...**")
        try:
            u_api = api_id or API_ID
            u_hash = api_hash or API_HASH

            new_client = Client(
                f"User_{user_id}",
                session_string=user_session,
                api_id=u_api,
                api_hash=u_hash,
                workers=100, # 🟢 FIX: Prevent queue overload
                ipv6=False
            )
            new_client.add_handler(MessageHandler(user_watcher_handler, is_watched_chat))
            await new_client.start()
            USER_CLIENTS[user_id] = new_client
            await status_msg.delete()
        except Exception as e:
            return await status_msg.edit(f"❌ **Session Error:** `{e}`\n\nTry /logout and /login again.")

    # Use user session if available, otherwise default to the Bot!
    user_client = USER_CLIENTS.get(user_id, app) 
    
    try:
        parsed = _parse_source_link(src_link)
        source_id = parsed["chat_id"]
        source_title = "Unknown Source"

        if parsed["kind"] == "invite":
            try: await user_client.join_chat(parsed["join_target"])
            except: pass
            chat = await user_client.get_chat(parsed["join_target"])
            source_id = chat.id
            source_title = chat.title or str(source_id)

        elif parsed["kind"] == "public":
            try:
                # Try Bot first
                chat = await app.get_chat(parsed["join_target"])
            except Exception:
                # Fallback to User Session
                chat = await user_client.get_chat(parsed["join_target"])
                
            source_id = chat.id
            source_title = chat.title or str(source_id)

        else:
            chat = await user_client.get_chat(source_id)
            source_title = chat.title or str(source_id)

        if parsed.get("topic_id"):
            source_title += await get_topic_title(user_client, source_id, parsed["topic_id"])

    except Exception as e:
        is_pub = parsed.get("kind") == "public" if 'parsed' in locals() else False
        reason = "The public username might be incorrect/banned." if is_pub else "I am not inside this private chat."
        return await message.reply(
            f"❌ **Could not access Source.**\n\n"
            f"You are not logged in, and I cannot read this chat directly.\n"
            f"💡 **Reason:** {reason}\n"
            f"**Fix:** Please use `/login` to route through your own account, OR add me to the source chat (**as an Admin for Channels, or a normal Member for Groups**).\n\n"
            f"**Error:** `{e}`"
        )

    # 🟢 Fetch the latest message ID to serve as our starting point
    last_msg_id = 0
    try:
        async for m in user_client.get_chat_history(source_id, limit=1):
            last_msg_id = m.id
    except Exception:
        try:
            async for m in app.get_chat_history(source_id, limit=1):
                last_msg_id = m.id
        except: pass

    await db.add_watcher(
        user_id=user_id,
        source_id=source_id,
        dest_id=data.get("dest_chat_id"),
        source_thread=data.get("source_thread_id"),
        dest_thread=data.get("dest_thread_id"),
        delay=delay,
        is_restricted=data["is_restricted"],
        source_title=source_title,
        dest_title=data.get("dest_title", str(data.get("dest_chat_id"))),
        allowed_types=data.get("allowed_types"),
        dashboard_chat=message.chat.id,
        dashboard_msg=message.id,
        last_msg_id=last_msg_id   # 🟢 PASS THE ID HERE
    )
    
    GLOBAL_WATCHER_SOURCES.add(source_id) # 🟢 UPDATE CACHE

    initial_text = (
        f"📡 **Live Watcher Started!**\n\n"
        f"**Source:** `{source_title}`\n"
        f"**Destination:** `{data.get('dest_title', str(data.get('dest_chat_id')))}`\n"
        f"**Filters:** `{', '.join(data.get('allowed_types', []))}`\n\n"
        f"🌐 **Track live statistics for this Watcher in the Web Dashboard!**"
    )
    
    try:
        if hasattr(message, "edit_text"):
            await message.edit_text(initial_text)
        else:
            new_msg = await message.reply(initial_text)
            # Failsafe if it couldn't edit
            await db.db.watchers.update_one(
                {
                    "user_id": user_id, 
                    "source_id": source_id, 
                    "source_thread": data.get("source_thread_id"),
                    "dest_id": data.get("dest_chat_id"),
                    "dest_thread": data.get("dest_thread_id")
                },
                {"$set": {"dashboard_chat": new_msg.chat.id, "dashboard_msg": new_msg.id}}
            )
    except Exception:
        pass
    
