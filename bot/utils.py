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

def _parse_source_link(link: str):
    if not link: return None
    link = str(link).strip()
    
    msg_id_end = None
    range_match = re.search(r"\s*-\s*(\d+)$", link)
    if range_match:
        msg_id_end = int(range_match.group(1))
        link = link[:range_match.start()].strip()

    link = link.split("?")[0].strip("/")
    has_c_prefix = "/c/" in link.lower() or "?c=" in link.lower()
    
    cleaned_link = re.sub(r"https?://(?:www\.)?t\.me/(?:c/)?", "", link)
    parts = cleaned_link.split("/")
    if not parts or not parts[0]: return None

    if parts[0] in ["joinchat", "+"]:
        return {"kind": "invite", "join_target": link, "chat_id": None, "topic_id": None, "msg_id": None, "msg_id_end": None}

    chat_id_raw = parts[0]
    is_numeric = chat_id_raw.lstrip("-").isdigit()
    
    if is_numeric:
        chat_id = int(chat_id_raw)
        if chat_id > 0 and has_c_prefix:
            chat_id = int(f"-100{chat_id}")
    else:
        chat_id = chat_id_raw 

    topic_id = int(parts[1]) if len(parts) >= 3 and parts[1].isdigit() else None
    msg_id = int(parts[2]) if len(parts) >= 3 and parts[2].isdigit() else (int(parts[1]) if len(parts) == 2 and parts[1].isdigit() else None)
        
    return {
        "kind": "private_c" if is_numeric else "public",
        "chat_id": chat_id,
        "join_target": chat_id,
        "topic_id": topic_id,
        "msg_id": msg_id,
        "msg_id_end": msg_id_end
    }

def _parse_chat_target(dest_str: str):
    if not dest_str: return None, None
    dest_str = str(dest_str).strip()
    
    has_c_prefix = "/c/" in dest_str.lower()
    cleaned = re.sub(r"https?://(?:www\.)?t\.me/(?:c/)?", "", dest_str)
    parts = cleaned.split("/")
    
    chat_id_raw = parts[0]
    thread_id = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else None
    
    if chat_id_raw.lstrip("-").isdigit():
        chat_id = int(chat_id_raw)
        if chat_id > 0 and has_c_prefix:
            chat_id = int(f"-100{chat_id}")
        return chat_id, thread_id
        
    if not chat_id_raw.startswith("@") and not chat_id_raw.lstrip("-").isdigit():
        chat_id_raw = f"@{chat_id_raw}"
        
    return chat_id_raw, thread_id

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


def clean_media_text(value: str, custom_tags=None) -> str:
    """Remove explicitly configured source tags from media text."""
    text = str(value or "")
    
    global_tags = CLEANUP_TAGS if 'CLEANUP_TAGS' in globals() else []
    all_tags = list(global_tags) + list(custom_tags or [])
    all_tags.sort(key=len, reverse=True)
    
    for tag in all_tags:
        if not str(tag).strip(): continue
        pattern = rf"(?i)\s*{re.escape(str(tag))}\s*"
        text = re.sub(pattern, " ", text)
        
    # 🟢 MAGIC FIX: Erase stray hyphens, spaces, and weird unicode symbols (°, ‧, ×) left behind
    garbage = r" \t\-~_°‧×|"
    text = re.sub(rf"^[{garbage}]+", "", text) # Removes from the very beginning
    text = re.sub(rf"[{garbage}]+(\.[a-zA-Z0-9]+)$", r"\1", text) # Removes right before the file extension
    text = re.sub(rf"[{garbage}]+$", "", text) # Removes from the very end
    
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"[ \t]+([,.;!?])", r"\1", text)
    text = re.sub(r"[\(\[\{][ \t]*[\)\]\}]", "", text)
    return text.strip()

def clean_caption(text, entities=None, custom_tags=None):
    original = text or ""
    # Pass the per-task tags down to the cleaner
    cleaned = clean_media_text(original, custom_tags=custom_tags)
    return cleaned, entities if cleaned == original else None


def filename_matches_filters(msg, include_keywords, exclude_keywords):
    if not include_keywords and not exclude_keywords:
        return True

    # Combine everything into one giant searchable string
    text_to_search = ""
    
    # 1. Text & Captions (Covers Photos, Text posts, and Media with captions)
    if getattr(msg, "caption", None):
        text_to_search += msg.caption.lower() + " "
    if getattr(msg, "text", None):
        text_to_search += msg.text.lower() + " "
        
    # 2. File Names (Covers all possible media types with file names)
    if getattr(msg, "document", None) and getattr(msg.document, "file_name", None):
        text_to_search += msg.document.file_name.lower() + " "
    elif getattr(msg, "video", None) and getattr(msg.video, "file_name", None):
        text_to_search += msg.video.file_name.lower() + " "
    elif getattr(msg, "audio", None) and getattr(msg.audio, "file_name", None):
        text_to_search += msg.audio.file_name.lower() + " "
    elif getattr(msg, "animation", None) and getattr(msg.animation, "file_name", None):
        text_to_search += msg.animation.file_name.lower() + " "
    elif getattr(msg, "voice", None) and getattr(msg.voice, "file_name", None):
        text_to_search += msg.voice.file_name.lower() + " "
        
    # 3. Stickers (Often have emojis instead of file names)
    if getattr(msg, "sticker", None):
        if getattr(msg.sticker, "file_name", None):
            text_to_search += msg.sticker.file_name.lower() + " "
        if getattr(msg.sticker, "emoji", None):
            text_to_search += msg.sticker.emoji.lower() + " "

    # If the message has absolutely no text/caption/filename and we HAVE include keywords, skip it.
    if not text_to_search.strip():
        if include_keywords:
            return False
        return True

    if include_keywords:
        # Must contain at least one of the include keywords
        if not any(inc.lower() in text_to_search for inc in include_keywords):
            return False
            
    if exclude_keywords:
        # Must NOT contain any exclude keywords
        if any(exc.lower() in text_to_search for exc in exclude_keywords):
            return False
            
    return True

def media_filename(message, fallback_id=None):
    for attr in ("document", "video", "audio", "animation", "voice", "sticker", "photo"):
        media = getattr(message, attr, None)
        if media:
            name = getattr(media, "file_name", None) or getattr(media, "title", None)
            if name:
                return clean_media_text(name)
            # 🟢 FIX: Removed the [:60] truncation so the full caption is used as the filename!
            if message.caption:
                return clean_media_text(message.caption.split('\n')[0])
    return f"message_{fallback_id}" if fallback_id is not None else "unknown_media"

def log_file_result(scope, user_id, task_id, source_id, message_id, filename, result, reason=None):
    status = str(result).upper()
    
    # 🟢 MINIMIZE LOGS: If it's not a failure, don't spam the console!
    if status in {"SUCCESS", "OK", "TRUE", "SKIPPED"}:
        return
        
    failed = status in {"FAIL", "FAILED", "ERROR"}
    level = logging.ERROR if failed else logging.INFO
    icon = "❌" if failed else "🛑" if status == "CANCELLED" else "⚠️"
    
    # Remove the ugly " -> 9347.jpg" artifact from the log name
    clean_name = clean_media_text(filename or "unknown_media")
    if " -> " in clean_name:
        clean_name = clean_name.split(" -> ")[0].strip()
        
    reason_text = str(reason or "")[:400]
    logger.log(
        level,
        "FILE_RESULT scope=%s user_id=%s task_id=%s msg_id=%s file='%s' result=%s %s reason=%r",
        scope, user_id, task_id or "-", message_id or "-", clean_name, status, icon, reason_text
    )
    
def sanitize_filename(filename: str) -> str:
    if not filename: return "unnamed_file"
    filename = unicodedata.normalize("NFC", filename)
    filename = clean_media_text(filename)
    filename = re.sub(r"\s+(\.[^.]+)$", r"\1", filename)
    filename = re.sub(r'[:]', "-", filename)
    filename = re.sub(r'[\\/*?"<>|\[\]]', "", filename)
    name, ext = os.path.splitext(filename)
    # 🟢 FIX: Expanded to 240 chars so long titles aren't truncated before zipping!
    if len(name) > 240:
        name = name[:240]
        
    reserved = {"CON", "PRN", "AUX", "NUL", "COM1", "LPT1"}
    if name.upper() in reserved:
        name += "_"
        
    if not ext:
        ext = ".dat"
    return f"{name}{ext}"


def build_media_filename(filename: str, message=None, index=1) -> str:
    safe_original = sanitize_filename(filename or "unnamed_file")
    original, ext = os.path.splitext(safe_original)
    media = None
    if message is not None:
        media = getattr(message, "audio", None) or getattr(message, "video", None) or getattr(message, "document", None)
    title = getattr(media, "title", None) or original
    message_id = getattr(message, "id", "") if message is not None else ""
    message_date = getattr(message, "date", None) if message is not None else None
    date = message_date.strftime("%Y-%m-%d") if hasattr(message_date, "strftime") else ""
    values = {
        "original": original,
        "title": clean_media_text(title),
        "id": str(message_id),
        "date": date,
        "index": str(index),
        "ext": ext,
    }
    try:
        rendered = FILENAME_TEMPLATE.format_map(values).strip()
    except (KeyError, ValueError):
        rendered = safe_original
    if not rendered:
        rendered = safe_original
    if not os.path.splitext(rendered)[1]:
        rendered += ext
    return sanitize_filename(rendered)

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

import traceback
from pyrogram.raw.functions.contacts import ResolveUsername

async def ensure_user_client(user_id: int):
    """Wakes up and keeps the persistent User Session alive in USER_CLIENTS."""
    if not user_id:
        return None
    uclient = USER_CLIENTS.get(user_id)
    if uclient and getattr(uclient, "is_connected", False):
        return uclient

    user_session = await db.get_session(user_id)
    if not user_session:
        return None

    try:
        from pyrogram import Client
        from pyrogram.handlers import MessageHandler
        api_id = await db.get_api_id(user_id) or API_ID
        api_hash = await db.get_api_hash(user_id) or API_HASH
        uclient = Client(
            f"User_{user_id}",
            session_string=user_session,
            api_id=api_id,
            api_hash=api_hash,
            workers=100,
            sleep_threshold=120,
            ipv6=False,
            no_updates=False,
            device_model="DestinyTgRestrict",
            app_version="DestinyTgRestrict 1.0",
            system_version="Linux",
            **get_transmission_kwargs(workers=100, is_bot=False)
        )
        if "user_watcher_handler" in globals() and "is_watched_chat" in globals():
            uclient.add_handler(MessageHandler(user_watcher_handler, is_watched_chat))
        await uclient.start()
        USER_CLIENTS[user_id] = uclient
        logger.info(f"✅ Woke up persistent User Session for user {user_id}")
        return uclient
    except Exception as e:
        logger.error(f"Failed to wake up User Session for {user_id}: {e}")
        return None


async def _safe_store_peer(client, peer_id, access_hash, peer_type, username=None, phone=None):
    """Safely writes peer to Pyrogram/Kurigram storage regardless of 4-tuple or 5-tuple signature."""
    for tuple_cand in (
        [(peer_id, access_hash, peer_type, username, phone)],
        [(peer_id, access_hash, peer_type, phone)],
    ):
        try:
            await client.storage.update_peers(tuple_cand)
            return
        except Exception:
            continue


async def resolve_and_cache_peer(client, target_ref):
    """
    Resolves a username or ID and caches its access_hash into Pyrogram storage
    without crashing. Returns (numeric_id, peer_kind).
    """
    if not client or target_ref is None:
        return target_ref, "unknown"

    if isinstance(target_ref, str) and not target_ref.lstrip("-").isdigit():
        clean_user = target_ref.replace("@", "").strip()

        # 1. Try native resolve_peer first (uses local cache if known)
        try:
            peer = await client.resolve_peer(clean_user)
            if hasattr(peer, "channel_id"):
                return int(f"-100{peer.channel_id}"), "channel"
            elif hasattr(peer, "user_id"):
                p_type = "bot" if clean_user.lower().endswith("bot") else "user"
                return int(peer.user_id), p_type
            elif hasattr(peer, "chat_id"):
                return int(f"-{peer.chat_id}"), "group"
        except Exception:
            pass

        # 2. Fallback to Raw ResolveUsername + safe tuple storage injection
        try:
            r = await client.invoke(ResolveUsername(username=clean_user))
            if getattr(r, "users", None):
                u = r.users[0]
                p_type = "bot" if getattr(u, "bot", False) else "user"
                await _safe_store_peer(
                    client, int(u.id), getattr(u, "access_hash", 0),
                    p_type, getattr(u, "username", None) or clean_user.lower(), getattr(u, "phone", None)
                )
                return int(u.id), p_type
            elif getattr(r, "chats", None):
                c = r.chats[0]
                is_ch = getattr(c, "broadcast", False) or getattr(c, "megagroup", False) or hasattr(c, "access_hash")
                full_id = int(f"-100{c.id}") if is_ch else int(f"-{c.id}")
                p_type = "channel" if getattr(c, "broadcast", False) else ("supergroup" if is_ch else "group")
                await _safe_store_peer(
                    client, full_id, getattr(c, "access_hash", 0),
                    p_type, getattr(c, "username", None) or clean_user.lower(), None
                )
                return full_id, p_type
        except Exception as raw_e:
            logger.warning(f"DEBUG: ResolveUsername failed on {getattr(client, 'name', 'client')} for {clean_user}: {raw_e}")

    if isinstance(target_ref, str) and target_ref.lstrip("-").isdigit():
        target_ref = int(target_ref)

    if isinstance(target_ref, int):
        if target_ref > 0:
            return target_ref, "user"
        elif str(target_ref).startswith("-100"):
            return target_ref, "channel"
        else:
            return target_ref, "group"

    return target_ref, "unknown"


async def check_link_restriction(user_id, link, is_watcher=False):
    """Returns (is_restricted, status_text_or_error_message)."""
    logger.info("========== DEBUG: LINK VALIDATION START ==========")
    logger.info(f"Target Link: {link} (is_watcher={is_watcher})")

    parsed = _parse_source_link(link)
    if not parsed:
        return None, "⚠️ **Could not analyze link format.**"

    raw_chat_id = parsed.get("chat_id")
    msg_id = parsed.get("msg_id")
    is_range = bool(parsed.get("msg_id_end"))
    logger.info(f"Parsed -> chat_id: {raw_chat_id} (Type: {type(raw_chat_id)}), msg_id: {msg_id}")

    if not raw_chat_id or (not msg_id and not is_watcher):
        logger.error("DEBUG: Invalid link parsed.")
        return None, "Invalid Telegram link."

    # 1. Always wake up and prefer the persistent User Session first!
    uclient = await ensure_user_client(user_id)
    primary_client = uclient if uclient else app
    logger.info(f"DEBUG: Primary validation client -> {getattr(primary_client, 'name', 'App')} (User Session Active: {bool(uclient)})")

    try:
        # 2. Resolve and properly cache the peer in storage
        chat_id, peer_kind = await resolve_and_cache_peer(primary_client, raw_chat_id)
        if primary_client != app and isinstance(raw_chat_id, str) and not str(raw_chat_id).lstrip("-").isdigit():
            await resolve_and_cache_peer(app, raw_chat_id)

        logger.info(f"DEBUG: Resolved Target ID: {chat_id} (Kind: {peer_kind})")

        # 3. Bot DM / Private User DM handling (e.g. https://t.me/justsagaraf2bot/222151)
        is_dm_source = peer_kind in ("bot", "user") or (isinstance(chat_id, int) and chat_id > 0)
        if is_dm_source:
            if not uclient:
                return None, "⚠️ **Bot/Private DM:** Please connect your Telegram Session in Settings so I can read messages from your private/bot chat."
            if msg_id:
                try:
                    msg = await uclient.get_messages(chat_id, msg_id)
                    if msg and not getattr(msg, "empty", True):
                        logger.info(f"DEBUG: Bot/User DM message {msg_id} verified via User Session!")
                        return True, "🔒 **Bot/Private DM (User Session Routed)**"
                except Exception as dm_e:
                    logger.warning(f"DEBUG: DM get_messages error: {dm_e}")

            if is_watcher or is_range:
                try:
                    await uclient.get_chat(chat_id)
                    logger.info("DEBUG: Bot/User DM chat verified for Watcher/Range!")
                    return True, "🔒 **Bot/Private DM (User Session Routed)**"
                except Exception as e:
                    return None, f"❌ **Cannot access Bot/User DM:** {e}"

            return None, "Message is missing, deleted, or inaccessible in this Bot/User DM."

        # 4. Channel / Supergroup / Group Fetch Helper
        async def smart_fetch(c, target_id):
            if not msg_id:
                return None, target_id, None
            try:
                await c.get_chat(target_id)
            except Exception:
                pass
            try:
                m = await c.get_messages(target_id, msg_id)
                if m and not getattr(m, "empty", True):
                    return m, target_id, None
            except Exception as e:
                err = e

            if isinstance(target_id, int) and target_id > 0:
                alt_id = int(f"-100{target_id}")
                try:
                    await c.get_chat(alt_id)
                except Exception:
                    pass
                try:
                    m = await c.get_messages(alt_id, msg_id)
                    if m and not getattr(m, "empty", True):
                        return m, alt_id, None
                except Exception as e:
                    err = e

            return None, target_id, locals().get("err", None)

        msg, chat_id, fetch_err = await smart_fetch(primary_client, chat_id)

        # Fallback to User Session if Main Bot failed
        if not msg and primary_client != uclient and uclient:
            chat_id, _ = await resolve_and_cache_peer(uclient, raw_chat_id)
            msg, chat_id, fetch_err = await smart_fetch(uclient, chat_id)

        # Fallback to Main Bot if User Session returned empty on a public chat
        if not msg and primary_client != app:
            msg, chat_id, _ = await smart_fetch(app, chat_id)

        if msg and not getattr(msg, "empty", True):
            is_content_protected = (
                getattr(msg, "has_protected_content", False)
                or getattr(msg.chat, "has_protected_content", False)
            )
            logger.info(f"DEBUG: Message {msg.id} found! Protected: {is_content_protected}")
            status_text = "🔒 **Restricted Content**" if is_content_protected else "🔓 **Unrestricted Content**"
            logger.info("========== DEBUG: VALIDATION SUCCESS ==========")
            return is_content_protected, status_text

        # 5. If the sample msg_id was deleted, still allow Watchers & Batch Ranges if the Chat itself is accessible
        if is_watcher or is_range:
            chat_obj = None
            for c in ([uclient, app] if uclient else [app]):
                try:
                    chat_obj = await c.get_chat(chat_id)
                    if chat_obj:
                        break
                except Exception:
                    continue

            if chat_obj:
                is_content_protected = getattr(chat_obj, "has_protected_content", False)
                logger.info(f"DEBUG: Sample msg_id {msg_id} was deleted, but Chat {chat_id} is valid! Protected: {is_content_protected}")
                status_text = "🔒 **Restricted Content**" if is_content_protected else "🔓 **Unrestricted Content**"
                return is_content_protected, status_text

        if fetch_err:
            raise fetch_err

        logger.error("DEBUG: get_messages returned completely empty!")
        return None, "Message is missing, deleted, or inaccessible."

    except Exception as e:
        logger.error(f"========== DEBUG: VALIDATION CRASH ==========\n{traceback.format_exc()}")
        err_str = str(e).lower()
        if "channel_invalid" in err_str or "channel_private" in err_str or "user_not_participant" in err_str:
            return None, "⚠️ **Private Chat:** I cannot access this. Please run `/login` so I can use your account to read it."
        elif "username_not_found" in err_str or "peer_id_invalid" in err_str:
            return None, "❌ **Access Blocked:** Telegram cannot find this chat. It may be geo-blocked, deleted, or you are not a member."

        clean_err = str(e).replace("KeyError:", "").replace('"', '').strip()
        return None, clean_err

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

async def resolve_task_clients(user_id, source_link, dest_chat_id, needs_reupload=False):
    """
    Accurately identifies In (fetcher) and Out (forwarder/uploader) without 
    triggering failing API attempts or breaking delays.
    """
    user_client = await ensure_user_client(user_id)
    worker_bots = USER_TASK_BOTS.get(user_id, [])
    parsed = _parse_source_link(source_link)

    raw_src = parsed.get("chat_id")
    src_id, peer_kind = await resolve_and_cache_peer(user_client or app, raw_src)

    is_private_src = (
        parsed.get("kind") in ["private_c", "private"]
        or peer_kind in ["bot", "user"]
        or (isinstance(src_id, int) and src_id > 0)
    )

    if is_private_src and peer_kind in ["bot", "user"]:
        needs_reupload = True

    # 1. Resolve Fetcher (In)
    fetcher = user_client if user_client else app

    # 2. Resolve Forwarder/Uploader (Out)
    if needs_reupload:
        uploader = user_client or app
        for wb in worker_bots:
            try:
                if not getattr(wb, "is_connected", False): await wb.connect()
                mb = await wb.get_chat_member(dest_chat_id, "me")
                if mb.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
                    uploader = wb
                    break
            except Exception: pass
        return fetcher, uploader

    # 3. Direct Fast Forwarding (Unrestricted & No Metadata Cleaning):
    forwarder = None
    if not is_private_src and worker_bots:
        for wb in worker_bots:
            try:
                if not getattr(wb, "is_connected", False): await wb.connect()
                dest_mb = await wb.get_chat_member(dest_chat_id, "me")
                if dest_mb.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
                    await wb.get_chat(raw_src)
                    forwarder = wb
                    break
            except Exception: pass

    if not forwarder:
        forwarder = user_client if user_client else app

    return forwarder, forwarder
        
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
