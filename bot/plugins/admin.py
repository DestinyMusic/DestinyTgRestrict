@app.on_message(filters.command(["log"]) & (filters.user(ADMINS) | filters.user(SUDOS)))
async def send_log_handler(client: Client, message: Message):
    try:
        if os.path.exists("bot.log"):
            await message.reply_document("bot.log", caption="📄 **Bot Logs**\n(Updates automatically)")
        else:
            await message.reply("⚠️ Log file not found yet.")
    except FloodWait as e:
        logger.warning(f"Blocked /log due to FloodWait: {e.value}s")

@app.on_message(filters.command(["pixel"]) & (filters.user(ADMINS) | filters.user(SUDOS)))
async def pixel_bypass_handler(client: Client, message: Message):
    if len(message.command) < 2:
        try:
            return await message.reply(
                "❌ **How to bypass Pixeldrain links:**\n\n"
                "Send a valid Pixeldrain link to get a high-speed direct download link that bypasses limits.\n\n"
                "**Examples:**\n"
                "• Single Link: `/pixel https://pixeldrain.com/u/xxxx`\n"
                "• Multiple Links: `/pixel link1, link2, link3`"
            )
        except FloodWait: return

    input_text = message.text.split(None, 1)[1]
    matches = re.findall(r"pixeldrain\.com/u/([a-zA-Z0-9_-]+)", input_text)
    
    if not matches:
        try:
            return await message.reply(
                "❌ **No valid Pixeldrain links found.**\n"
                "Please ensure the links follow the format: `https://pixeldrain.com/u/XXXX`"
            )
        except FloodWait: return

    lines = []
    for match in matches:
        orig = f"https://pixeldrain.com/u/{match}"
        byp = f"https://cdn.pixeldrain.eu.cc/{match}"
        lines.append(f"🔗 **Original:** {orig}\n🔓 **Bypassed:** `{byp}`\n")
        
    bypassed_text = "\n".join(lines)
    
    reply_text = (
        "✨ **Pixeldrain Bypass Successful!** ✨\n\n"
        "**📥 Bypassed Links:**\n\n"
        f"{bypassed_text}\n"
        "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
        "🌐 **Original Bypass Website:** [Click Here](https://pixeldrain-bypass.gamedrive.org/)\n"
        "📜 **Userscript:** [Install Script](https://pixeldrain-bypass.gamedrive.org/pixeldrain-bypass.user.js)"
    )
    try: await message.reply(reply_text, disable_web_page_preview=True)
    except FloodWait: pass

# ==============================================================================
# --- SPEEDTEST HANDLER ---
# ==============================================================================

@app.on_message(filters.command(["speedtest"]) & (filters.user(ADMINS) | filters.user(SUDOS)))
async def speedtest_handler(client: Client, message: Message):
    try:
        status_msg = await message.reply("<i>Initiating Speedtest...</i>", parse_mode=enums.ParseMode.HTML)
    except FloodWait as e:
        return logger.warning(f"Silently blocked /speedtest init due to FloodWait: {e.value}s")
    
    def run_speedtest_sync():
        try:
            # secure=True forces HTTPS to bypass datacenter port blocks
            st = speedtest.Speedtest(secure=True)
            st.get_best_server()
            st.download()
            st.upload()
            try:
                # Silently ignore image generation if Speedtest blocks the datacenter IP
                st.results.share() 
            except Exception:
                pass 
            return st.results.dict(), None
        except Exception as e:
            return None, str(e)

    try:
        # Run blocking speedtest in a separate thread to avoid freezing bot
        result, error = await asyncio.to_thread(run_speedtest_sync)
        
        if error or not result:
            await status_msg.edit_text(f"<b>ERROR:</b> <i>Can't connect to Server.</i>\n<code>{error}</code>", parse_mode=enums.ParseMode.HTML)
            return

        # --- THE FIX: Convert directly to Mbps to match the generated image exactly! ---
        dl_mbps = result['download'] / 1_000_000
        ul_mbps = result['upload'] / 1_000_000
        ping_ms = result['ping']
        
        string_speed = (
            f"➲ <b><i>SPEEDTEST INFO</i></b>\n"
            f"┠ <b>Download:</b> <code>{dl_mbps:.2f} Mbps</code>\n"
            f"┠ <b>Upload:</b> <code>{ul_mbps:.2f} Mbps</code>\n"
            f"┠ <b>Ping:</b> <code>{ping_ms} ms</code>\n"
            f"┖ <b>Data Sent/Recv:</b> <code>{_pretty_bytes(result['bytes_sent'])} / {_pretty_bytes(result['bytes_received'])}</code>\n\n"
            f"➲ <b><i>SPEEDTEST SERVER</i></b>\n"
            f"┠ <b>Name:</b> <code>{result['server']['name']}</code>\n"
            f"┠ <b>Location:</b> <code>{result['server']['country']}, {result['server']['cc']}</code>\n"
            f"┖ <b>Sponsor:</b> <code>{result['server']['sponsor']}</code>"
        )

        try:
            if result.get("share"):
                await message.reply_photo(photo=result["share"], caption=string_speed, parse_mode=enums.ParseMode.HTML)
                await status_msg.delete()
            else:
                await status_msg.edit_text(string_speed, parse_mode=enums.ParseMode.HTML)
        except FloodWait: pass

    except Exception as e:
        logger.error(f"Speedtest error: {e}")
        try: await status_message.edit_text(f"❌ An error occurred: {e}")
        except: pass
        
@app.on_message(filters.command(["status"]) & (filters.user(ADMINS) | filters.user(SUDOS)))
async def status_style_handler(client, message):
    uptime_seconds = int(time.time() - BOT_START_TIME)
    uptime_str = get_readable_time(uptime_seconds)
    mem = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent()
    
    total, used, free = shutil.disk_usage(".")
    disk_free = free / (1024**3)
    
    active_count = 0
    queue_list = []
    
    for uid, tasks in ACTIVE_PROCESSES.items():
        for t_id, info in tasks.items():
            active_count += 1
            src = info.get("source_title", "Source")
            dst = info.get("dest_title_name", "Destination")
            queue_list.append(f"• {src} → {dst}")
    
    watcher_count = await db.db.watchers.count_documents({})
    queue_text = "\n".join(queue_list) if queue_list else "😴 No active downloads."

    msg = (
        f"<b>🔰 SYSTEM DASHBOARD</b>\n\n"
        f"<blockquote>"
        f"⏱ <b>Uptime:</b> <code>{uptime_str}</code>\n"
        f"🧠 <b>RAM:</b> <code>{mem}%</code>  │  ⚙️ <b>CPU:</b> <code>{cpu}%</code> \n"
        f"💿 <b>Disk Free:</b> <code>{disk_free:.1f} GB</code> \n\n"
        f"👀 <b>Live Watchers:</b> <code>{watcher_count}</code> running\n"
        f"📉 <b>Active Downloads ({active_count})</b>\n"
        f"{queue_text}"
        f"</blockquote>"
    )
    try:
        await message.reply(msg, quote=True, parse_mode=enums.ParseMode.HTML)
    except FloodWait as e:
        logger.warning(f"Silently blocked /status reply due to FloodWait: {e.value}s")
    
@app.on_message(filters.command(["botstats"]) & filters.user(ADMINS))
async def bot_stats_handler(client: Client, message: Message):
    try:
        wait = await message.reply("<b>📊 Generating detailed stats...</b>", parse_mode=enums.ParseMode.HTML)
    except FloodWait as e:
        logger.warning(f"Silently blocked /botstats init due to FloodWait: {e.value}s")
        return

    total_users = await db.total_users_count()
    all_users_cursor = await db.get_all_users()
    
    logged_in_list = []
    async for user in all_users_cursor:
        if user.get("session"):
            user_id = user['id']
            name = user.get("name") or f"User:{user_id}"
            user_tasks = ACTIVE_PROCESSES.get(user_id, {})
            
            if user_tasks:
                task_details = []
                for t_id, info in user_tasks.items():
                    src = info.get("source_title", "Source")
                    dst = info.get("dest_title", "Dest")
                    tot = info.get("total", 0)
                    curr = info.get("current", 0)
                    start_t = info.get("started", time.time())
                    
                    percent = (curr / tot * 100) if tot > 0 else 0
                    
                    elapsed = time.time() - start_t
                    eta_str = "Calculating..."
                    if curr > 0 and elapsed > 0:
                        eta_str = get_readable_time(int(((tot - curr) / (curr / elapsed))))

                    task_details.append(
                        f"      └ 🏃 {src} → {info.get('dest_title_name', 'Destination')}"
                    )
                    
                tasks_str = "\n" + "\n".join(task_details)
                logged_in_list.append(f"• <b>{name}</b> [<code>{user_id}</code>]{tasks_str}")
            else:
                logged_in_list.append(f"• <b>{name}</b> [<code>{user_id}</code>] (IDLE 😴)")

    logged_in_text = "\n\n".join(logged_in_list) if logged_in_list else "No users logged in."
    stats_msg = (
        "<b>📊 DETAILED BOT STATISTICS</b>\n"
        "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
        "<blockquote expandable>\n"
        f"👥 <b>Total Users:</b> <code>{total_users}</code>\n"
        f"🔑 <b>Logged-in Users:</b> <code>{len(logged_in_list)}</code>\n\n"
        f"📝 <b>User & Task Breakdown:</b>\n\n{logged_in_text}\n"
        "</blockquote>"
    )
    try:
        await wait.edit(stats_msg, parse_mode=enums.ParseMode.HTML)
    except FloodWait:
        pass # UI rate-limited, safely ignore

# ==============================================================================
# --- SOS SYSTEM STATS COMMAND ---
# ==============================================================================

def generate_sos_text(m_down=0, m_up=0, m_total=0, month_name=""):
    def make_bar(percent, length=12):
        filled = int((percent / 100) * length)
        filled = max(0, min(length, filled))
        return f"[{'◙' * filled}{'◘' * (length - filled)}]"

    try:
        with open("/etc/os-release") as f:
            os_info = dict(line.strip().split("=", 1) for line in f if "=" in line)
        os_name = os_info.get("PRETTY_NAME", f'"{platform.system()} {platform.release()}"').strip('"')
    except Exception:
        os_name = f"{platform.system()} {platform.release()}"

    host = socket.gethostname()
    kernel = platform.uname().release
    
    os_uptime_seconds = time.time() - psutil.boot_time()
    os_uptime = get_readable_time(os_uptime_seconds)
    
    try:
        b_uptime = time.time() - BOT_START_TIME
    except NameError:
        b_uptime = os_uptime_seconds
    bot_uptime = get_readable_time(b_uptime)

    try:
        pkg_count = subprocess.check_output("dpkg-query -f '.\\n' -W | wc -l", shell=True).decode().strip()
        pkg_str = f"{pkg_count} (dpkg)"
    except Exception:
        pkg_str = "Unknown"
    shell = os.environ.get('SHELL', 'bash')

    try:
        with open("/proc/cpuinfo") as f:
            cpu_name = [line.split(":")[1].strip() for line in f if "model name" in line][0]
    except Exception:
        cpu_name = platform.processor() or "Unknown Processor"
    
    cpu_percent = psutil.cpu_percent(interval=0.2)
    cpu_cores = psutil.cpu_count(logical=False) or 0
    cpu_logical = psutil.cpu_count(logical=True) or 0
    
    freq = psutil.cpu_freq()
    freq_str = f"{round(freq.current)} MHz" if freq and getattr(freq, 'current', None) else "Disabled"

    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    disk = psutil.disk_usage('/')

    net = psutil.net_io_counters()
    down_bw = net.bytes_recv
    up_bw = net.bytes_sent
    total_bw = down_bw + up_bw

    try:
        with open("/etc/timezone") as f:
            tz = f.read().strip()
    except Exception:
        tz = "UTC"

    return (
        f"<b>🖥 SYSTEM STATISTICS</b>\n"
        f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬✘▬\n"
        f"<blockquote expandable>\n"
        f"<b>OS:</b> <code>{os_name}</code>\n"
        f"<b>Host:</b> <code>{host}</code>\n"
        f"<b>Kernel:</b> <code>{kernel}</code>\n"
        f"<b>Uptime:</b> <code>{os_uptime}</code>\n"
        f"<b>Packages:</b> <code>{pkg_str}</code>\n"
        f"<b>Shell:</b> <code>{shell}</code>\n"
        f"<b>CPU:</b> <code>{cpu_name}</code>\n\n"
        
        f"<b>SERVER AREA:</b> <code>{tz}</code>\n"
        f"<b>BOT UPTIME :</b> <code>{bot_uptime}</code>\n\n"
        
        f"「 <b>DISK</b> 」\n"
        f"<code>{make_bar(disk.percent)}</code> | {disk.percent}%\n"
        f"Available : <code>{_pretty_bytes(disk.free)}</code>\n"
        f"Used      : <code>{_pretty_bytes(disk.used)}</code> of <code>{_pretty_bytes(disk.total)}</code>\n\n"
        
        f"「 <b>CPU</b> 」\n"
        f"<code>{make_bar(cpu_percent)}</code> | {cpu_percent}%\n"
        f"Cores     : <code>{cpu_cores}</code>\n"
        f"Logical   : <code>{cpu_logical}</code>\n"
        f"Frequency : <code>{freq_str}</code>\n\n"
        
        f"「 <b>MEMORY</b> 」\n"
        f"<code>{make_bar(mem.percent)}</code> | {mem.percent}%\n"
        f"Available : <code>{_pretty_bytes(mem.available)}</code>\n"
        f"Used      : <code>{_pretty_bytes(mem.used)}</code> of <code>{_pretty_bytes(mem.total)}</code>\n\n"
        
        f"「 <b>SWAP</b> 」\n"
        f"Total     : <code>{_pretty_bytes(swap.total) if swap.total > 0 else 'Not Set'}</code>\n"
        f"Used      : <code>{_pretty_bytes(swap.used) if swap.total > 0 else 'Not Set'}</code>\n\n"
        
        f"「 <b>CURRENT BOOT BANDWIDTH</b> 」\n"
        f"Download  : <code>{_pretty_bytes(down_bw)}</code>\n"
        f"Upload    : <code>{_pretty_bytes(up_bw)}</code>\n"
        f"Boot Total: <code>{_pretty_bytes(total_bw)}</code>\n\n"
        
        f"「 <b>MONTHLY BANDWIDTH ({month_name})</b> 」\n"
        f"Downloaded: <code>{_pretty_bytes(m_down)}</code>\n"
        f"Uploaded  : <code>{_pretty_bytes(m_up)}</code>\n"
        f"Total Used: <code>{_pretty_bytes(m_total)} / 10.00 TB</code>\n"
        f"</blockquote>\n"
        f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬✘▬"
    )

@app.on_message(filters.command(["sos"]) & (filters.user(ADMINS) | filters.user(SUDOS)))
async def sos_handler(client: Client, message: Message):
    try:
        status_msg = await message.reply("<i>Fetching System Stats...</i>", parse_mode=enums.ParseMode.HTML)
    except FloodWait as e:
        return logger.warning(f"Silently blocked /sos init due to FloodWait: {e.value}s")
        
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔄 Refresh", callback_data="refresh_sos"),
            InlineKeyboardButton("❌ Cancel", callback_data="close_sos")
        ]
    ])
    try:
        m_down, m_up, m_total, month_name = await db.get_monthly_bandwidth()
        text = await asyncio.to_thread(generate_sos_text, m_down, m_up, m_total, month_name)
        await status_msg.edit_text(text, parse_mode=enums.ParseMode.HTML, reply_markup=keyboard)
    except FloodWait: pass
    except Exception as e:
        try: await status_msg.edit_text(f"❌ Error fetching system stats: {e}")
        except: pass

@app.on_callback_query(filters.regex("^refresh_sos$"))
async def refresh_sos_callback(client: Client, callback_query: CallbackQuery):
    if callback_query.from_user.id not in ADMINS and callback_query.from_user.id not in SUDOS:
        return await callback_query.answer("❌ Admins only.", show_alert=True)
        
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔄 Refresh", callback_data="refresh_sos"),
            InlineKeyboardButton("❌ Cancel", callback_data="close_sos")
        ]
    ])
    try:
        m_down, m_up, m_total, month_name = await db.get_monthly_bandwidth()
        text = await asyncio.to_thread(generate_sos_text, m_down, m_up, m_total, month_name)
        await callback_query.message.edit_text(text, parse_mode=enums.ParseMode.HTML, reply_markup=keyboard)
        await callback_query.answer("✅ System Stats Refreshed!")
    except Exception:
        await callback_query.answer("⚠️ Stats are exactly the same or an error occurred.")

@app.on_callback_query(filters.regex("^close_sos$"))
async def close_sos_callback(client: Client, callback_query: CallbackQuery):
    if callback_query.from_user.id not in ADMINS and callback_query.from_user.id not in SUDOS:
        return await callback_query.answer("❌ Admins only.", show_alert=True)
    await callback_query.message.delete()
    await callback_query.answer()
        
# ==============================================================================
# ==============================================================================
# --- BROADCAST ---
# ==============================================================================

async def broadcast_messages(user_id, message):
    start_time = time.time()
    try:
        await USER_FLOOD_LOCKS[user_id].wait_if_locked()
        await message.copy(chat_id=user_id)
        elapsed = time.time() - start_time
        await asyncio.sleep(max(0, 1.5 - elapsed)) 
        return True, "Success"
    except FloodWait as e:
        if e.value > 60:
            return False, "Error"
        USER_FLOOD_LOCKS[user_id].set_lock(e.value + 5)
        await asyncio.sleep(e.value + 5)
        return await broadcast_messages(user_id, message)
    except InputUserDeactivated:
        await db.delete_user(int(user_id))
        return False, "Deleted"
    except UserIsBlocked:
        await db.delete_user(int(user_id))
        return False, "Blocked"
    except PeerIdInvalid:
        await db.delete_user(int(user_id))
        return False, "Error"
    except Exception as e:
        logger.error(f"Broadcast completely failed for user {user_id}: {e}", exc_info=True)
        return False, "Error"

@app.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
async def broadcast(bot, message):
    users = await db.get_all_users()
    b_msg = message.reply_to_message
    if not b_msg:
        try:
            return await message.reply_text(
                "❌ **How to Broadcast:**\n\n"
                "1. Send the message you want to broadcast (text, photo, or video).\n"
                "2. **Reply** to that specific message with `/broadcast`.\n\n"
                "The bot will then copy that message and send it to every user in the database."
            )
        except FloodWait: return
        
    try:
        sts = await message.reply_text(text='Broadcasting your messages...')
    except FloodWait as e:
        return logger.warning(f"Silently blocked broadcast init due to FloodWait: {e.value}s")
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    blocked = 0
    deleted = 0
    failed = 0
    success = 0
    async for user in users:
        if 'id' in user:
            pti, sh = await broadcast_messages(int(user['id']), b_msg)
            if pti:
                success += 1
            elif pti == False:
                if sh == "Blocked":
                    blocked += 1
                elif sh == "Deleted":
                    deleted += 1
                elif sh == "Error":
                    failed += 1
            done += 1
            if not done % 20:
                await sts.edit(f"Broadcast in progress:\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}")
        else:
            done += 1
            failed += 1
            if not done % 20:
                await sts.edit(f"Broadcast in progress:\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}")

    time_taken = str(datetime.timedelta(seconds=int(time.time()-start_time)))
    await sts.edit(f"Broadcast Completed:\nCompleted in {time_taken} seconds.\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}")

# --- MEDIAINFO HANDLER (Admin Only) ---
# ==============================================================================

section_dict = {"General": "🗒", "Video": "🎞", "Audio": "🔊", "Text": "🔠", "Menu": "🗃"}

def parseinfo(out, size):
    tc, trigger = "", False
    size_mb = size / (1024 * 1024)
    size_line = f"File size                                 : {size_mb:.2f} MiB"
    
    lines = out.split("\n")
    for line in lines:
        line = line.strip()
        if not line: continue
        
        found_section = False
        for section, emoji in section_dict.items():
            if line.startswith(section):
                trigger = True
                found_section = True
                if not line.startswith("General"):
                    tc += "</pre><br>"
                tc += f"<h4>{emoji} {line.replace('Text', 'Subtitle')}</h4>"
                break
        
        if found_section: continue

        if line.startswith("File size"):
            line = size_line
            
        if trigger:
            tc += "<br><pre>"
            trigger = False
        else:
            tc += html.escape(line) + "\n"
            
    tc += "</pre><br>"
    return tc

async def partial_download_tg(client, message, file_path, limit_mb=15):
    media_obj = message.document or message.video or message.audio or message.photo
    file_size = getattr(media_obj, 'file_size', 0)
    limit_bytes = max(1, int(limit_mb * 1024 * 1024))

    if file_size <= limit_bytes:
        await client.download_media(message, file_name=str(file_path))
        return

    # Preserve the original sparse-file strategy, but actually honor limit_mb.
    chunk_size = 1048576
    total_chunks = math.ceil(file_size / chunk_size)
    edge_chunks = max(1, math.ceil((limit_bytes / 2) / chunk_size))
    edge_chunks = min(edge_chunks, total_chunks // 2)

    with open(file_path, "wb") as f:
        # Start of file: container headers + stream declarations.
        async for chunk in client.stream_media(message, limit=edge_chunks):
            f.write(chunk)

        if total_chunks > edge_chunks:
            offset = max(edge_chunks, total_chunks - edge_chunks)
            tail_limit = total_chunks - offset
            if tail_limit > 0:
                f.seek(offset * chunk_size)
                async for chunk in client.stream_media(message, offset=offset, limit=tail_limit):
                    f.write(chunk)

async def partial_download_http(url, file_path, limit_mb=15):
    """Robust bounded HTTP sampler used by MediaInfo/probing.

    Important properties:
      * Never assumes the remote Content-Length equals the number of bytes that
        will actually arrive. Some CDNs/proxies close a response early.
      * Uses byte ranges for large files when supported.
      * Never calls response.read() without a size cap on a supposedly ranged
        response.
      * Rejects HTML pages early because a movie-page URL is not a media URL.
      * Returns gracefully with the bytes that were actually received when the
        remote server truncates a probe response.
    """
    limit_bytes = max(1, int(limit_mb * 1024 * 1024))
    ua = (
        "Mozilla/5.0 (Linux; Android 10; Mobile) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Mobile Safari/537.36"
    )
    headers = {
        "User-Agent": ua,
        "Accept": "video/*,audio/*,application/octet-stream,application/vnd.apple.mpegurl,*/*;q=0.8",
        "Accept-Encoding": "identity",
        "Connection": "close",
    }
    timeout = aiohttp.ClientTimeout(total=None, connect=20, sock_connect=20, sock_read=25)

    def filename_from_headers(resp):
        detected = "Stream_File.dat"
        cd = resp.headers.get("Content-Disposition", "")
        if cd:
            # RFC 5987 filename*=UTF-8''... first, then normal filename=.
            m = re.search(r"filename\\*=(?:UTF-8''|utf-8'')([^;]+)", cd, re.I)
            if m:
                detected = unquote(m.group(1).strip().strip('"'))
            else:
                m = re.search(r'filename="?([^";]+)"?', cd, re.I)
                if m:
                    detected = m.group(1).strip()
        if detected == "Stream_File.dat":
            path_name = os.path.basename(urlparse(url).path)
            if path_name:
                detected = unquote(path_name)
        return detected or "Stream_File.dat"

    async def consume_limited(resp, out_f, max_bytes):
        """Write at most max_bytes and tolerate premature upstream EOF."""
        written = 0
        try:
            async for chunk in resp.content.iter_chunked(256 * 1024):
                if not chunk:
                    continue
                remaining = max_bytes - written
                if remaining <= 0:
                    break
                if len(chunk) > remaining:
                    chunk = chunk[:remaining]
                out_f.write(chunk)
                written += len(chunk)
                if written >= max_bytes:
                    break
        except (aiohttp.ClientPayloadError,
                aiohttp.ServerDisconnectedError,
                asyncio.TimeoutError,
                ConnectionError,
                OSError) as exc:
            # A truncated probe is still useful to ffprobe if it contains enough
            # container headers/stream descriptors. Do not turn this into a fatal
            # ContentLengthError for the web player.
            logger.warning(f"[HTTP probe] Remote body ended early: {exc}")
        return written

    async with aiohttp.ClientSession(timeout=timeout, raise_for_status=False) as session:
        # First request: headers + content-type + filename. Do not consume its body.
        try:
            async with session.get(url, headers=headers, allow_redirects=True) as resp:
                if resp.status >= 400:
                    body = await resp.text(errors="ignore")
                    raise RuntimeError(f"HTTP {resp.status}: {body[:180]}")

                content_type = (resp.headers.get("Content-Type") or "").lower()
                detected_name = filename_from_headers(resp)
                declared_size = int(resp.headers.get("Content-Length", "0") or 0)
                final_url = str(resp.url)

                # A webpage is not a playable media stream. Give the UI a useful
                # message instead of feeding HTML to ffprobe/HTMLMediaElement.
                if "text/html" in content_type or content_type.startswith("text/plain") and not re.search(r"\.(?:m3u8|mpd)(?:$|\?)", final_url, re.I):
                    raise ValueError(
                        "This URL returned a webpage/text page, not a direct video/audio stream. "
                        "Use the direct .mp4/.webm/.mkv/.m3u8 media URL."
                    )
        except ValueError:
            raise

        # Small/unknown-size resource: read only the probe budget. Even if the
        # server advertises a larger Content-Length, we never require all bytes.
        if declared_size == 0 or declared_size <= limit_bytes:
            with open(file_path, "wb") as f:
                try:
                    async with session.get(url, headers=headers, allow_redirects=True) as resp:
                        if resp.status >= 400:
                            raise RuntimeError(f"HTTP {resp.status} while reading media")
                        await consume_limited(resp, f, limit_bytes)
                except (aiohttp.ClientPayloadError,
                        aiohttp.ServerDisconnectedError,
                        asyncio.TimeoutError,
                        ConnectionError,
                        OSError) as exc:
                    logger.warning(f"[HTTP probe] Body truncated after partial read: {exc}")
            return declared_size, detected_name

        # Large resource: make a sparse probe file from head + tail ranges.
        edge_bytes = max(1_000_000, limit_bytes // 2)
        edge_bytes = min(edge_bytes, max(1, declared_size // 2))
        head_expected = edge_bytes
        tail_start = max(0, declared_size - edge_bytes)

        with open(file_path, "wb") as f:
            # HEAD sample.
            head_headers = headers.copy()
            head_headers["Range"] = f"bytes=0-{head_expected - 1}"
            try:
                async with session.get(url, headers=head_headers, allow_redirects=True) as resp:
                    if resp.status >= 400:
                        raise RuntimeError(f"HTTP {resp.status} for initial probe range")
                    await consume_limited(resp, f, head_expected)
                    head_is_partial = resp.status == 206 or bool(resp.headers.get("Content-Range"))
            except (aiohttp.ClientPayloadError,
                    aiohttp.ServerDisconnectedError,
                    asyncio.TimeoutError,
                    ConnectionError,
                    OSError) as exc:
                logger.warning(f"[HTTP probe] Head range ended early: {exc}")
                head_is_partial = False

            # Tail sample only when the server really honors Range. If it ignores
            # the Range header and returns 200/full-body, do not corrupt the sparse
            # file by writing the beginning of the file at the tail offset.
            tail_headers = headers.copy()
            tail_headers["Range"] = f"bytes={tail_start}-{declared_size - 1}"
            try:
                async with session.get(url, headers=tail_headers, allow_redirects=True) as resp:
                    if resp.status == 206 or resp.headers.get("Content-Range"):
                        f.seek(tail_start)
                        await consume_limited(resp, f, edge_bytes)
                    else:
                        logger.info("[HTTP probe] Remote server ignored tail Range; using head sample only.")
            except (aiohttp.ClientPayloadError,
                    aiohttp.ServerDisconnectedError,
                    asyncio.TimeoutError,
                    ConnectionError,
                    OSError) as exc:
                logger.warning(f"[HTTP probe] Tail range ended early: {exc}")

        return declared_size, detected_name

async def download_audio_snippet_tg(client_to_use, message, file_path, limit_mb=15):
    """Continuous download of the first X MB so SoX/FFmpeg reads it as a valid truncated file."""
    with open(file_path, "wb") as f:
        current_bytes = 0
        async for chunk in client_to_use.stream_media(message):
            f.write(chunk)
            current_bytes += len(chunk)
            if current_bytes >= limit_mb * 1024 * 1024:
                break

async def download_audio_snippet_http(url, file_path, limit_mb=15):
    """Continuous HTTP download of the first X MB."""
    headers = {"User-Agent": "Mozilla/5.0"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            resp.raise_for_status()
            with open(file_path, "wb") as f:
                current_bytes = 0
                async for chunk in resp.content.iter_chunked(1024 * 1024):
                    f.write(chunk)
                    current_bytes += len(chunk)
                    if current_bytes >= limit_mb * 1024 * 1024:
                        break

async def full_download_http(url, file_path):
    """Full HTTP download utilizing the Direct Stream resolver for Terabox/Gdrive/etc."""
    resolved = await resolve_direct_link(url)
    session = await _get_direct_http_session()
    
    req_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    }
    
    # Apply cached security cookies and tokens
    cached_h = DIRECT_HEADER_CACHE.get(resolved) or DIRECT_HEADER_CACHE.get(url) or {}
    for h_key in ["Cookie", "Referer", "Authorization", "User-Agent"]:
        if h_key in cached_h:
            req_headers[h_key] = cached_h[h_key]

    # Robust redirect follower mimicking the live streaming engine
    max_redirects = 3
    current_url = resolved
    remote = None
    
    for _ in range(max_redirects):
        remote = await session.get(
            _safe_yarl(current_url), 
            headers=req_headers,
            allow_redirects=False
        )
        if remote.status in (301, 302, 303, 307, 308):
            new_url = remote.headers.get("Location")
            remote.release()
            if not new_url:
                break
            from urllib.parse import urljoin
            current_url = urljoin(current_url, new_url)
        else:
            break
            
    if not remote or remote.status >= 400:
        if remote: remote.release()
        raise Exception(f"HTTP Error: Download failed with status {remote.status if remote else 'Redirect Loop'}")

    # Safely stream actual media bytes to the editor's disk
    try:
        with open(file_path, "wb") as f:
            async for chunk in remote.content.iter_chunked(2 * 1024 * 1024):
                if chunk: f.write(chunk)
    finally:
        try: remote.release()
        except Exception: pass
                    
@app.on_message(filters.command(["mediainfo", "mi"]) & (filters.user(ADMINS) | filters.user(SUDOS)))
async def mediainfo_handler(client: Client, message: Message):
    url = None
    media_msg = None
    
    if len(message.command) > 1:
        potential_url = message.command[1]
        if potential_url.startswith("http"): url = potential_url

    if not url and message.reply_to_message:
        replied = message.reply_to_message
        if replied.text:
            match = re.search(r'https?://\S+', replied.text)
            if match: url = match.group(0)
        elif replied.document or replied.video or replied.audio or replied.photo:
            media_msg = replied

    if not url and not media_msg:
        try:
            return await message.reply(
                "❌ **How to use MediaInfo:**\n\n"
                "This command analyzes a media file and gives you a technical breakdown (resolution, codec, bitrate, etc.) published to Telegraph.\n\n"
                "**Examples:**\n"
                "• Quick Reply: Reply to any video or document with `/mi`\n"
                "• Direct Link: `/mi https://example.com/video.mp4`"
            )
        except FloodWait: return

    try:
        status_msg = await message.reply(f"<i>Generating MediaInfo...</i>", parse_mode=enums.ParseMode.HTML)
    except FloodWait as e:
        return logger.warning(f"Silently blocked /mi init due to FloodWait: {e.value}s")
    
    temp_filename = f"partial_{message.id}_{int(time.time())}.dat"
    file_path = Path(os.getcwd()) / temp_filename
    
    file_name_display = "Unknown File"
    file_size_display = 0

    try:
        if url:
            try:
                file_size_display, detected_name = await partial_download_http(url, file_path, limit_mb=15)
                file_name_display = detected_name
            except Exception as e:
                await status_msg.edit_text(f"❌ Link download failed: {e}")
                return
        else:
            media_obj = media_msg.document or media_msg.video or media_msg.audio or media_msg.photo
            file_name_display = getattr(media_obj, 'file_name', 'Telegram_Media')
            file_size_display = getattr(media_obj, 'file_size', 0)
            
            try:
                await partial_download_tg(client, media_msg, file_path, limit_mb=15)
            except Exception as e:
                logger.warning(f"MediaInfo stream failed, attempting full download: {e}", exc_info=True)
                await status_msg.edit_text("⚠️ Stream failed, trying full download...")
                await client.download_media(media_msg, file_name=str(file_path))

        real_ext = Path(file_name_display).suffix
        if real_ext:
            new_path = file_path.with_suffix(real_ext)
            file_path.rename(new_path)
            file_path = new_path

        cmd = ["mediainfo", str(file_path)]
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        raw_output = stdout.decode('utf-8', errors='ignore').strip()

        if not raw_output:
            await status_msg.edit_text("❌ Could not read metadata.")
            return

        raw_output = raw_output.replace(str(file_path), file_name_display)
        raw_output = raw_output.replace(str(file_path.absolute()), file_name_display)

        safe_file_name = html.escape(file_name_display)
        formatted_html = f"<h4>📌 {safe_file_name}</h4><br><br>"
        formatted_html += parseinfo(raw_output, file_size_display)

        try:
            token = load_telegraph_token()
            if not token:
                raise Exception("Telegraph token missing from config.")
                
            from telegraph.utils import html_to_nodes
            import socket
            
            conn = aiohttp.TCPConnector(family=socket.AF_INET, force_close=True, enable_cleanup_closed=True)
            async with aiohttp.ClientSession(connector=conn) as session:
                
                # FIX 1 & 2: Telegraph strictly requires Form-Data (data=) 
                # and the 'content' field MUST be a stringified JSON array!
                payload = {
                    "access_token": token,
                    "title": "MediaInfo X",
                    "content": json.dumps(html_to_nodes(formatted_html)), # <-- THE MAGIC FIX
                    "return_content": "false"
                }
                
                max_retries = 4
                resp_data = None
                for attempt in range(max_retries):
                    try:
                        # FIX 3: Route directly to api.graph.org to bypass server IP Blocks
                        async with session.post("https://api.graph.org/createPage", data=payload, timeout=30) as resp:
                            resp_data = await resp.json()
                            if resp_data.get("ok"):
                                break
                            else:
                                err_msg = resp_data.get("error", "Unknown Telegraph Error")
                                # FIX 4: Handle FloodWait Gracefully (Like WZML)
                                if "FLOOD_WAIT" in err_msg:
                                    wait_time = int(err_msg.split("_")[-1])
                                    await asyncio.sleep(wait_time + 1)
                                    continue # Retry the loop!
                                raise Exception(err_msg)
                    except Exception as api_err:
                        if attempt == max_retries - 1:
                            raise api_err
                        await asyncio.sleep(2)
                
                # No string replacement needed since we directly uploaded to graph.org!
                final_link = resp_data["result"]["url"]
                    
            await status_msg.edit_text(
                f"✅ <b>MediaInfo Generated</b> 🦥\n\n"
                f"📄 <b>File:</b> {safe_file_name}\n"
                f"➲ <b>Link :</b> {final_link}",
                disable_web_page_preview=False,
                parse_mode=enums.ParseMode.HTML
            )

        except Exception as e:
            txt_path = file_path.with_suffix(".txt")
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(raw_output)
            
            await client.send_document(
                chat_id=message.chat.id,
                document=str(txt_path),
                caption=f"✅ **MediaInfo Generated** 🦥\n(Telegraph API rejected connection. Sent as file)",
                reply_to_message_id=message.id
            )
            await status_msg.delete()
            if txt_path.exists(): os.remove(txt_path)

    except Exception as e:
        logger.error(f"MediaInfo generation crashed: {e}", exc_info=True)
        await status_msg.edit_text(f"❌ Error: {e}")
    finally:
        if file_path.exists():
            try: os.remove(file_path)
            except Exception as e: logger.debug(f"MediaInfo cleanup failed: {e}")

# ==============================================================================
@app.on_message(filters.command(["spectrogram", "spec"]) & (filters.user(ADMINS) | filters.user(SUDOS)))
async def tg_spectrogram_cmd(client: Client, message: Message):
    url = None
    media_msg = None
    
    if len(message.command) > 1:
        potential_url = message.command[1]
        if potential_url.startswith("http"): url = potential_url

    if not url and message.reply_to_message:
        replied = message.reply_to_message
        if replied.text:
            match = re.search(r'https?://\S+', replied.text)
            if match: url = match.group(0)
        elif replied.document or replied.video or replied.audio or replied.voice:
            media_msg = replied

    if not url and not media_msg:
        return await message.reply("❌ Usage: `/spec <link>` or reply to a file/link.")

    status_msg = await message.reply("📉 <b>Downloading & Analyzing Audio...</b>", parse_mode=enums.ParseMode.HTML)
    
    temp_dir = Path(f"./temp_sox_{message.from_user.id}_{int(time.time())}")
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    original_file = temp_dir / "audio_input.dat"
    wav_file = temp_dir / "converted.wav"
    output_img = temp_dir / "spectrogram.png"

    try:
        # 1. DOWNLOAD LOGIC (FULL FILE)
        if url:
            if "t.me" in url or "telegram.me" in url:
                parsed = _parse_source_link(url)
                chat_id = parsed.get("chat_id")
                msg_id = parsed.get("msg_id")
                
                uclient = USER_CLIENTS.get(message.from_user.id)
                if not uclient or not uclient.is_connected:
                    return await status_msg.edit_text("❌ Telegram session not active. Please /login.")
                    
                msg = await uclient.get_messages(chat_id, msg_id)
                if msg.empty: return await status_msg.edit_text("❌ Message not found or inaccessible.")
                await uclient.download_media(msg, file_name=str(original_file))
            else:
                await full_download_http(url, original_file)
        else:
            await client.download_media(media_msg, file_name=str(original_file))

        # 2. CONVERSION
        await status_msg.edit_text("📉 <b>Running DSP Mathematics...</b>", parse_mode=enums.ParseMode.HTML)
        ffmpeg_cmd = ["ffmpeg", "-i", str(original_file), "-vn", "-ac", "2", "-c:a", "pcm_f32le", str(wav_file), "-y"]
        process = await asyncio.create_subprocess_exec(*ffmpeg_cmd, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.PIPE)
        await process.wait()
        
        if not wav_file.exists(): return await status_msg.edit_text("❌ Audio Extraction Failed.")

        # 3. STATS & SOX
        stats = await asyncio.to_thread(generate_audio_stats_dsp, str(wav_file), str(original_file), "Audio Analysis")
        if not stats: return await status_msg.edit_text("❌ DSP Processing Failed.")

        sox_cmd = ["sox", str(wav_file), "-n", "spectrogram", "-o", str(output_img), "-x", "1000", "-Y", "800", "-c", "Audio", "-t", " "]
        process_sox = await asyncio.create_subprocess_exec(*sox_cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        await process_sox.communicate()

        if not output_img.exists(): return await status_msg.edit_text("❌ SoX Image Generation Failed.")

        # 4. CAPTION BUILDING
        m = stats['mastering']
        mastering_text = ""
        if m:
            phase_warn = "⚠️ Mono risk" if m['correlation'] < -0.2 else "Phase OK"
            dc_warn = "⚠️ Defect" if m['dc_offset'] > -60.0 else "Clean"
            mastering_text = (
                f"\n<b>— MASTERING ANALYSIS —</b>\n"
                f"🎚 <b>Dynamic Range:</b> <code>DR {m['dr']}</code>\n"
                f"🔊 <b>Loudness (LUFS):</b> <code>{m['lufs']:.1f} LUFS</code>\n"
                f"📈 <b>Peak / RMS:</b> <code>{m['peak']:.2f} dBFS</code> / <code>{m['rms']:.2f} dB</code>\n"
                f"💥 <b>Clipping Events:</b> <code>{m['clipping']}</code>\n"
                f"⚖️ <b>Stereo Correl:</b> <code>{m['correlation']:.2f} ({phase_warn})</code>\n"
                f"🔌 <b>DC Offset:</b> <code>{m['dc_offset']:.1f} dBFS ({dc_warn})</code>\n"
                f"🏷 <b>Score:</b> {m['grade']}\n"
            )

        caption = (
            f"📊 <b>Audio Analysis: Fidelity & Mastering</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"<blockquote expandable>"
            f"<b>— FIDELITY & AUTHENTICITY —</b>\n"
            f"📀 <b>Container:</b> <code>{stats['format']} • {stats['channel_str']} • {stats['bit_depth']}-bit • {stats['sample_rate']/1000} kHz</code>\n"
            f"📈 <b>Bandwidth Cutoff:</b> <code>{stats['cutoff']} kHz</code>\n"
            f"🧱 <b>Cliff Drop:</b> <code>{stats['cliff_drop']:.1f} dB</code>\n"
            f"🔍 <b>Authenticity:</b> {stats['auth_badge']}\n"
            f"<i>{stats['auth_desc']}</i>\n"
            f"{mastering_text}"
            f"</blockquote>\n"
            f"⚡ <b>RESULT:</b> {stats['auth_badge']}"
        )

        await message.reply_photo(photo=str(output_img), caption=caption, parse_mode=enums.ParseMode.HTML)
        await status_msg.delete()

    except Exception as e:
        await status_msg.edit_text(f"❌ Error: {e}")
    finally:
        import shutil
        try: shutil.rmtree(str(temp_dir), ignore_errors=True)
        except: pass
            
