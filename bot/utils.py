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

def _parse_source_link(link: str):
    """Universal parser: handles t.me, telegram.me, tg://, /c/, /b/, /s/, batch ranges, and topics."""
    if not link:
        return None
    raw = str(link).strip()
    msg_id_end = None

    # 1. Extract Batch Ranges (e.g. 100-120 or 100 - 120)
    range_match = re.search(r"\s*(?:-|to)\s*(\d+)$", raw, re.IGNORECASE)
    if range_match:
        msg_id_end = int(range_match.group(1))
        raw = raw[:range_match.start()].strip()

    # 2. Native tg:// links
    if raw.startswith("tg://openmessage") or raw.startswith("tg://resolve"):
        from urllib.parse import urlparse, parse_qs
        qs = parse_qs(urlparse(raw).query)
        chat_target = qs.get("user_id", qs.get("domain", [None]))[0]
        msg_id = qs.get("message_id", qs.get("post", [None]))[0]
        if chat_target and str(chat_target).lstrip("-").isdigit():
            chat_target = int(chat_target)
        return {
            "kind": "private" if isinstance(chat_target, int) else "public",
            "chat_id": chat_target,
            "join_target": chat_target,
            "topic_id": None,
            "msg_id": int(msg_id) if msg_id and str(msg_id).isdigit() else None,
            "msg_id_end": msg_id_end
        }

    # 3. Standard HTTP Telegram links
    link_clean = raw.split("?")[0].strip("/")
    has_c_prefix = "/c/" in link_clean.lower()

    # Strip domain prefixes cleanly
    cleaned = re.sub(r"https?://(?:www\.)?(?:telegram\.me|t\.me)/(?:s/|b/)?(?:c/)?", "", link_clean)
    parts = cleaned.split("/")
    if not parts or not parts[0]:
        return None

    if parts[0] in ["joinchat", "+"]:
        return {
            "kind": "invite",
            "join_target": raw,
            "chat_id": None,
            "topic_id": None,
            "msg_id": None,
            "msg_id_end": msg_id_end
        }

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

async def _safe_store_peer(client, peer_id, access_hash, peer_type, username=None, phone=None):
    """Safely writes peer to storage across varying Pyrogram/fork storage signatures."""
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
    Resolves usernames or IDs and caches their access_hash to prevent PEER_ID_INVALID.
    Returns (numeric_id, peer_kind).
    """
    if not client or target_ref is None:
        return target_ref, "unknown"

    if isinstance(target_ref, str) and not target_ref.lstrip("-").isdigit():
        clean_user = target_ref.replace("@", "").strip()

        # 1. Native resolve (hits local DB cache if already encountered)
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

        # 2. Raw MTProto API ResolveUsername fallback
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
        except Exception as e:
            logger.debug(f"Raw ResolveUsername failed for {clean_user}: {e}")

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
    
import traceback
from pyrogram.raw.functions.contacts import ResolveUsername

async def check_link_restriction(user_id, link, is_watcher=False):
    """Accurately checks link restrictions with boolean safety and fallback handling."""
    logger.info("========== DEBUG: LINK VALIDATION START ==========")
    logger.info(f"Target Link: {link} (is_watcher={is_watcher})")

    parsed = _parse_source_link(link)
    if not parsed:
        return None, "⚠️ **Could not analyze link format.**"

    raw_chat_id = parsed.get("chat_id")
    msg_id = parsed.get("msg_id")
    is_range = bool(parsed.get("msg_id_end"))

    if not raw_chat_id or (not msg_id and not is_watcher):
        return None, "Invalid Telegram link."

    uclient = await ensure_user_client(user_id)
    primary_client = uclient if uclient else app

    try:
        chat_id, peer_kind = await resolve_and_cache_peer(primary_client, raw_chat_id)
        if primary_client != app and isinstance(raw_chat_id, str) and not str(raw_chat_id).lstrip("-").isdigit():
            await resolve_and_cache_peer(app, raw_chat_id)

        is_dm_source = peer_kind in ("bot", "user") or (isinstance(chat_id, int) and chat_id > 0)
        
        # 1. Handling Bot DMs / User DMs
        if is_dm_source:
            if not uclient:
                return None, "⚠️ **Bot/Private DM:** Please connect your Telegram Session in Settings so I can read messages from your private/bot chat."

            if is_watcher or is_range:
                chat_obj = await uclient.get_chat(chat_id)
                is_prot = bool(getattr(chat_obj, "has_protected_content", False))
                return is_prot, "🔒 **Restricted Content**" if is_prot else "🔓 **Unrestricted Content**"

            if msg_id:
                try:
                    msg = await uclient.get_messages(chat_id, msg_id)
                    if msg and not getattr(msg, "empty", True):
                        is_prot = bool(getattr(msg, "has_protected_content", False)) or bool(getattr(getattr(msg, "chat", None), "has_protected_content", False))
                        return is_prot, "🔒 **Restricted Content**" if is_prot else "🔓 **Unrestricted Content**"
                except Exception:
                    pass

            return None, "Message is missing, deleted, or inaccessible in this Bot/User DM."

        # 2. Handling Channels / Groups
        async def _fetch(c, cid):
            if not msg_id:
                return None, cid, None
            try:
                await c.get_chat(cid)
            except Exception:
                pass
            try:
                m = await c.get_messages(cid, msg_id)
                if m and not getattr(m, "empty", True):
                    return m, cid, None
            except Exception as e:
                err = e

            if isinstance(cid, int) and cid > 0:
                alt = int(f"-100{cid}")
                try:
                    m = await c.get_messages(alt, msg_id)
                    if m and not getattr(m, "empty", True):
                        return m, alt, None
                except Exception:
                    pass
            return None, cid, locals().get("err", None)

        msg, chat_id, err = await _fetch(primary_client, chat_id)
        if not msg and primary_client != uclient and uclient:
            chat_id, _ = await resolve_and_cache_peer(uclient, raw_chat_id)
            msg, chat_id, err = await _fetch(uclient, chat_id)
        if not msg and primary_client != app:
            msg, chat_id, _ = await _fetch(app, chat_id)

        # 🟢 CRITICAL FIX: Explicit boolean casting prevents 'None' from triggering false error returns
        if msg and not getattr(msg, "empty", True):
            is_prot = bool(getattr(msg, "has_protected_content", False)) or bool(getattr(getattr(msg, "chat", None), "has_protected_content", False))
            return is_prot, "🔒 **Restricted Content**" if is_prot else "🔓 **Unrestricted Content**"

        # Deleted sample message fallback for Watchers & Batch Ranges
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
                is_prot = bool(getattr(chat_obj, "has_protected_content", False))
                return is_prot, "🔒 **Restricted Content**" if is_prot else "🔓 **Unrestricted Content**"

        if err:
            raise err
        return None, "Message is missing, deleted, or inaccessible."

    except Exception as e:
        err_str = str(e).lower()
        if "channel_invalid" in err_str or "channel_private" in err_str or "user_not_participant" in err_str:
            return None, "⚠️ **Private Chat:** I cannot access this. Please run `/login` so I can use your account to read it."
        elif "username_not_found" in err_str or "peer_id_invalid" in err_str:
            return None, "❌ **Access Blocked:** Telegram cannot find this chat. It may be geo-blocked, deleted, or you are not a member."
        return None, str(e).replace("KeyError:", "").replace('"', '').strip()

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
    user_client = USER_CLIENTS.get(user_id)
    worker_bots = USER_TASK_BOTS.get(user_id, [])
    parsed = _parse_source_link(source_link)
    
    is_private_src = parsed.get("kind") in ["private_c", "private"] or (isinstance(parsed.get("chat_id"), int) and parsed.get("chat_id") > 0)
    
    # 1. Resolve Fetcher (In)
    fetcher = user_client if (is_private_src and user_client) else app
    
    # 2. Resolve Forwarder/Uploader (Out)
    # If content needs physical re-upload (restricted / custom thumb / cleanup keywords):
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
    # The client MUST have access to BOTH source and destination!
    forwarder = None
    
    # Check if a Worker Bot can access BOTH Source AND Destination
    if not is_private_src and worker_bots:
        for wb in worker_bots:
            try:
                if not getattr(wb, "is_connected", False): await wb.connect()
                dest_mb = await wb.get_chat_member(dest_chat_id, "me")
                if dest_mb.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
                    # Test source access
                    await wb.get_chat(parsed.get("chat_id") or parsed.get("join_target"))
                    forwarder = wb
                    break
            except Exception: pass
            
    # If source is private OR worker bots cannot access source: MUST use User Session!
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
