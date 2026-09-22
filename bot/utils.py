# ==============================================================================
# --- HELPERS ---
# ==============================================================================

def parse_chat_topic(value):
    if not value:
        return None, None
    value = str(value).strip()
    if "/" in value:
        chat_id, topic_id = value.split("/", 1)
        return int(chat_id), int(topic_id)
    return int(value), None

def _parse_chat_target(text: str):
    text = text.strip()
    if text.startswith("https://t.me/") or text.startswith("http://t.me/"):
        text = text.replace("https://", "").replace("http://", "")
        text = text.split("t.me/", 1)[-1].split("?", 1)[0].strip("/")
    if text.startswith("@"):
        return text, None
    if "/" in text:
        chat_part, topic_part = text.split("/", 1)
        chat_part = chat_part.strip()
        topic_part = topic_part.strip()
        return int(chat_part), int(topic_part) if topic_part.isdigit() else None
    if text.lstrip("-").isdigit():
        return int(text), None
    return text, None

def _parse_source_link(src_link: str):
    raw = (src_link or "").strip()
    msg_range = None

    # 1. First, extract the range if it exists (e.g. 190171 - 192592)
    if "," in raw:
        links = [l.strip() for l in raw.split(",")]
        raw = links[0] 
        last_link = links[-1]
        try:
            start_id = int(re.search(r"(\d+)(?:\?|$)", raw.rstrip("/").split("/")[-1]).group(1))
            end_id = int(re.search(r"(\d+)(?:\?|$)", last_link.rstrip("/").split("/")[-1]).group(1))
            if start_id <= end_id:
                msg_range = (start_id, end_id)
        except: pass
    else:
        # Catch formats like ...190171 - 192592
        m = re.search(r"(?:/|=|%3D)(\d+)\s*(?:-|to)\s*(\d+)$", raw, re.IGNORECASE)
        if m:
            try:
                start_id = int(m.group(1))
                end_id = int(m.group(2))
                if start_id <= end_id:
                    msg_range = (start_id, end_id)
                # Clean the tail so the base link works normally
                if "=" in m.group(0):
                    raw = raw[:m.start(0)] + f"={m.group(1)}"
                else:
                    raw = raw[:m.start(0)] + f"/{m.group(1)}"
            except: pass

    # 2. Handle native tg://openmessage?user_id=...&message_id=...
    if raw.startswith("tg://openmessage") or raw.startswith("tg://resolve"):
        from urllib.parse import urlparse, parse_qs
        parsed_url = urlparse(raw)
        qs = parse_qs(parsed_url.query)
        chat_target = qs.get("user_id", qs.get("domain", [None]))[0]
        msg_id = qs.get("message_id", qs.get("post", [None]))[0]
        
        if chat_target and str(chat_target).lstrip("-").isdigit():
            chat_target = int(chat_target)
            
        if msg_id and str(msg_id).isdigit():
            msg_id = int(msg_id)
            
        return {
            "kind": "private" if isinstance(chat_target, int) else "public",
            "join_target": chat_target,
            "chat_id": chat_target,
            "topic_id": None,
            "msg_id": msg_id,
            "msg_range": msg_range,
        }

    # 3. Standard HTTP t.me links
    if "t.me/" in raw:
        raw = raw.split("t.me/")[-1]
    elif "telegram.me/" in raw:
        raw = raw.split("telegram.me/")[-1]
        
    if raw.startswith("s/"):
        raw = raw[2:]
        
    raw = raw.split("?", 1)[0].strip("/")

    # Handle Private /c/ links
    is_private_c = raw.startswith("c/")
    if is_private_c:
        clean = raw[2:]
        parts = clean.split("/")
        source_id = int("-100" + parts[0])
        topic_id = int(parts[1]) if len(parts) >= 3 and parts[1].isdigit() else None
        
        msg_id = None
        last_segment = parts[-1].strip()
        if last_segment.isdigit():
            msg_id = int(last_segment)
            
        return {
            "kind": "private_c",
            "join_target": None,
            "chat_id": source_id,
            "topic_id": topic_id,
            "msg_id": msg_id,
            "msg_range": msg_range, 
        }

    parts = raw.split("/")
    
    # Catch alternative t.me/b/BotName links
    if parts[0] == "b" and len(parts) > 1:
        parts.pop(0)

    username_or_id = parts[0]
    topic_id = int(parts[1]) if len(parts) >= 3 and parts[1].isdigit() else None
    
    msg_id = None
    last_segment = parts[-1].strip()
    if last_segment.isdigit():
        msg_id = int(last_segment)

    # 🟢 CRITICAL FIX: Convert numeric strings to actual integers for User/Bot IDs
    if str(username_or_id).lstrip("-").isdigit():
        chat_target = int(username_or_id)
    else:
        chat_target = username_or_id

    if str(username_or_id).startswith("+") or "joinchat" in str(username_or_id):
        return {
            "kind": "invite",
            "join_target": f"https://t.me/{raw}",
            "chat_id": None,
            "topic_id": topic_id,
            "msg_id": msg_id,
            "msg_range": msg_range,
        }

    return {
        "kind": "public",
        "join_target": chat_target,
        "chat_id": chat_target,
        "topic_id": topic_id,
        "msg_id": msg_id,
        "msg_range": msg_range,
    }

def _pretty_bytes(n: float) -> str:
    try:
        n = float(n)
    except Exception:
        return "0 B"
    if n == 0: return "0 B"
    units = ("B", "KB", "MB", "GB", "TB", "PB")
    i = 0
    while n >= 1024 and i < len(units) - 1:
        n /= 1024
        i += 1
    unit = units[i]
    if unit == "B": return f"{int(n)} {unit}"
    else: return f"{n:.1f} {unit}"

import unicodedata

def get_readable_time(seconds: int) -> str:
    try:
        seconds = int(seconds)
    except (TypeError, ValueError):
        seconds = 0
    if seconds <= 0: return "0s"
    
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    
    time_parts = []
    if days > 0: time_parts.append(f"{days}d")
    if hours > 0: time_parts.append(f"{hours}h")
    if minutes > 0: time_parts.append(f"{minutes}m")
    if seconds > 0 or not time_parts: time_parts.append(f"{seconds}s")
    return " ".join(time_parts)

def generate_bar(percent: float, length: int = 12) -> str:
    percent = max(0.0, min(100.0, percent)) 
    filled_length = int(length * percent / 100)
    fraction = (percent / 100 * length) - filled_length
    has_half = fraction >= 0.5
    
    bar = '⬤' * filled_length
    if has_half and filled_length < length:
        bar += '◔'
        bar += '○' * (length - filled_length - 1)
    else:
        bar += '○' * (length - filled_length)
        
    return f"〘{bar}〙 {percent:.1f}%"
    
def sanitize_filename(filename: str) -> str:
    if not filename: return "unnamed_file"
    filename = unicodedata.normalize("NFC", filename)
    filename = re.sub(r'[:]', "-", filename)
    filename = re.sub(r'[\\/*?"<>|\[\]]', "", filename)
    name, ext = os.path.splitext(filename)
    if len(name) > 60:
        name = name[:60]
        
    reserved = {"CON", "PRN", "AUX", "NUL", "COM1", "LPT1"}
    if name.upper() in reserved:
        name += "_"
        
    if not ext:
        ext = ".dat"
    return f"{name}{ext}"

async def get_topic_title(client, chat_id, topic_id):
    """Dynamically fetches the real name of a Telegram Forum Topic."""
    if not topic_id: return ""
    
    # 1. High-Level Method (Kurigram/Pyrofork Native)
    try:
        if hasattr(client, "get_forum_topic"):
            topic = await client.get_forum_topic(chat_id, int(topic_id))
            if isinstance(topic, list) and topic and getattr(topic[0], "title", None): 
                return f" ({topic[0].title})"
            elif getattr(topic, "title", None):
                return f" ({topic.title})"
    except Exception: pass

    # 2. Raw MTProto API Method (Bulletproof for all topics)
    try:
        from pyrogram.raw.functions.channels import GetForumTopicsByID
        peer = await client.resolve_peer(chat_id)
        res = await client.invoke(GetForumTopicsByID(channel=peer, topics=[int(topic_id)]))
        if getattr(res, "topics", None) and len(res.topics) > 0:
            return f" ({res.topics[0].title})"
    except Exception: pass

    # 3. Last-Resort Message Fallback
    try:
        msg = await client.get_messages(chat_id, int(topic_id))
        if msg:
            if getattr(msg, "forum_topic", None) and getattr(msg.forum_topic, "title", None):
                return f" ({msg.forum_topic.title})"
            if getattr(msg, "action", None) and getattr(msg.action, "title", None):
                return f" ({msg.action.title})"
            if getattr(msg, "reply_to_message", None) and getattr(msg.reply_to_message, "forum_topic", None):
                if getattr(msg.reply_to_message.forum_topic, "title", None):
                    return f" ({msg.reply_to_message.forum_topic.title})"
    except Exception: pass

    return f" (Topic {topic_id})"

async def check_link_restriction(user_id, link_text):
    if link_text.startswith("+") or "joinchat" in link_text:
        return False, "🔗 **Invite link detected.** Join the chat first before checking restrictions."

    parsed = _parse_source_link(link_text)
    if not parsed:
        return None, "⚠️ **Could not analyze link format.**"

    chat_id = parsed.get("chat_id")
    msg_id = parsed.get("msg_id")

    if not chat_id:
        return None, "⚠️ **Could not determine Chat ID.**"

    is_private = False
    
    # 🟢 Force User Session if it's a private group, a numeric user/bot ID, or a bot username
    if parsed.get("kind") == "private_c" or isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id.lower().endswith("bot")):
        is_private = True
        
    # Additional safety for positive numeric IDs (Direct DMs)
    if isinstance(chat_id, int) and chat_id > 0:
        is_private = True

    is_temp_client = False
    check_client = app 
    user_session = await db.get_session(user_id)
    
    if is_private:
        existing_client = USER_CLIENTS.get(user_id)
        if existing_client and existing_client.is_connected:
            check_client = existing_client
        elif user_session:
            api_id = await db.get_api_id(user_id) or API_ID
            api_hash = await db.get_api_hash(user_id) or API_HASH
            check_client = Client(":memory:", session_string=user_session, api_id=api_id, api_hash=api_hash, no_updates=True, ipv6=False)
            is_temp_client = True
    
    is_restricted = False
    status_msg = ""

    try:
        if is_temp_client:
            await check_client.connect()

        # For resolving Usernames/IDs to actual entities before checking
        if isinstance(chat_id, str) and not chat_id.lstrip('-').isdigit():
            try: await check_client.resolve_peer(chat_id)
            except Exception: pass

        if msg_id:
            msg = None
            bot_err_saved = None
            try:
                msg = await check_client.get_messages(chat_id, msg_id)
            except Exception as e:
                bot_err_saved = e

            if (bot_err_saved or not msg or msg.empty) and check_client == app and user_session:
                api_id = await db.get_api_id(user_id) or API_ID
                api_hash = await db.get_api_hash(user_id) or API_HASH
                check_client = Client(":memory:", session_string=user_session, api_id=api_id, api_hash=api_hash, no_updates=True, ipv6=False)
                await check_client.connect()
                is_temp_client = True
                try:
                    msg = await check_client.get_messages(chat_id, msg_id)
                    bot_err_saved = None
                except Exception as user_err:
                    bot_err_saved = user_err
                    
            if bot_err_saved:
                raise bot_err_saved

            if not msg or msg.empty:
                raise Exception("Message not found or inaccessible.")

            if getattr(msg.chat, "has_protected_content", False) or getattr(msg, "has_protected_content", False):
                is_restricted = True
                status_msg = "🔒 **Source is RESTRICTED** (Will use Download Mode)"
            else:
                is_restricted = False
                status_msg = "🔓 **Source is PUBLIC/UNRESTRICTED** (Will use Fast Forward)"
        else:
            try:
                chat = await check_client.get_chat(chat_id)
            except Exception as bot_err:
                if check_client == app and user_session:
                    api_id = await db.get_api_id(user_id) or API_ID
                    api_hash = await db.get_api_hash(user_id) or API_HASH
                    check_client = Client(":memory:", session_string=user_session, api_id=api_id, api_hash=api_hash, no_updates=True, ipv6=False)
                    await check_client.connect()
                    is_temp_client = True
                    try:
                        chat = await check_client.get_chat(chat_id)
                    except Exception as user_err:
                        raise user_err
                else:
                    raise bot_err

            if getattr(chat, "has_protected_content", False):
                is_restricted = True
                status_msg = "🔒 **Chat is RESTRICTED** (Will use Download Mode)"
            else:
                is_restricted = False
                status_msg = "🔓 **Chat is PUBLIC/UNRESTRICTED**"

    except Exception as e:
        err_str = str(e).lower()
        if "channel_private" in err_str or "user_not_participant" in err_str:
            status_msg = "⚠️ **Private Chat:** I can't check yet (You need to join first)."
        elif "username_not_occupied" in err_str or "username_invalid" in err_str or "peer_id_invalid" in err_str:
            if check_client != app:
                return None, f"❌ **Telegram Blocked Access:** Even your logged account cannot see this! It may be geo-blocked or deleted."
            else:
                return None, f"❌ **Bot Blocked:** The bot cannot see this source. \n\n💡 **FIX:** Please use `/login` to link your account, and I will resolve it using your session!"
        elif "authkeyunregistered" in err_str or "sessionrevoked" in err_str:
            return None, f"❌ **Session Expired:** Your login session is invalid. Please run `/logout` and then `/login` again."
        else:
            return None, f"❌ **Check Failed:** `{str(e)[:50]}...`\nPlease ensure the link is active and valid."
    finally:
        if is_temp_client:
            try: await check_client.disconnect()
            except: pass
        
    return is_restricted, status_msg

async def split_file_python(file_path, chunk_size=2000*1024*1024):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(io_executor, _split_file_smart, file_path, chunk_size)

def _split_file_smart(file_path, chunk_size):
    file_path = Path(file_path)
    if not file_path.exists():
        return []

    file_size = os.path.getsize(file_path)
    if file_size <= chunk_size:
        return [file_path]

    # Attempt High-Speed Linux Binary Split
    if shutil.which("split"):
        try:
            output_prefix = f"{file_path}."
            # Split normally creates .000, .001...
            cmd = ["split", "-b", str(chunk_size), "-d", "-a", "3", str(file_path), output_prefix]
            subprocess.run(cmd, check=True, capture_output=True)
            
            # Shift extensions to match MKV.001, MKV.002
            split_files = sorted(list(file_path.parent.glob(f"{file_path.name}.[0-9][0-9][0-9]")), reverse=True)
            for sf in split_files:
                try:
                    idx = int(sf.suffix.replace('.', ''))
                    new_sf = sf.with_suffix(f".{idx + 1:03d}")
                    sf.rename(new_sf)
                except ValueError:
                    pass
                    
            parts = sorted(list(file_path.parent.glob(f"{file_path.name}.[0-9][0-9][0-9]")))
            if parts: return parts
        except Exception as e: 
            logger.debug(f"Linux 'split' failed, falling back to python... Error: {e}")

    # Fallback to Pure Python Binary Splitter
    part_num = 1
    parts = []
    buffer_size = 2 * 1024 * 1024 
    
    with open(file_path, 'rb') as source:
        while True:
            # Slices into .mkv.001, .mkv.002
            part_name = file_path.parent / f"{file_path.name}.{part_num:03d}"
            current_chunk_size = 0
            with open(part_name, 'wb') as dest:
                while current_chunk_size < chunk_size:
                    read_size = min(buffer_size, chunk_size - current_chunk_size)
                    data = source.read(read_size)
                    if not data: break
                    dest.write(data)
                    current_chunk_size += len(data)
            if current_chunk_size == 0:
                if part_name.exists(): part_name.unlink()
                break
            parts.append(part_name)
            part_num += 1
            
    return parts
    
def progress(current, total, typ, task_uuid=None):
    if task_uuid and CANCEL_FLAGS.get(task_uuid):
        raise Exception("CANCELLED_BY_USER")

    key = f"{task_uuid}:{typ}" if task_uuid else "unknown"
    now = time.time()
    if key not in PROGRESS:
        PROGRESS[key] = {
            "current": 0, "total": int(total), "percent": 0.0,
            "last_time": now, "last_current": 0, "speed": 0.0, "eta": None
        }
    rec = PROGRESS[key]
    rec["current"] = int(current)
    rec["total"] = int(total)
    if total > 0:
        rec["percent"] = (current / total) * 100.0
    dt = now - rec["last_time"]
    if dt >= 1 or current == total:
        delta_bytes = current - rec["last_current"]
        if dt <= 0: dt = 0.1
        speed = delta_bytes / dt
        rec["speed"] = speed
        rec["last_time"] = now
        rec["last_current"] = current
        if speed > 0 and total > current:
            rec["eta"] = (total - current) / speed
            
def get_message_type(msg: Message):
    if msg.document: return "Document"
    if msg.video: return "Video"
    if msg.animation: return "Animation"
    if msg.sticker: return "Sticker"
    if msg.voice: return "Voice"
    if msg.audio: return "Audio"
    if msg.photo: return "Photo"
    if msg.text: return "Text"
    return None

