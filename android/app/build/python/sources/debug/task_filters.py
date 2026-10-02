import re


def split_filter_values(value):
    return {part.strip().casefold() for part in (value or "").split(",") if part.strip()}


def is_protected(message):
    chat = getattr(message, "chat", None)
    return bool(getattr(message, "has_protected_content", False)
                or getattr(chat, "has_protected_content", False))


def message_category(message):
    if message.text:
        return "text"
    if message.video:
        return "video"
    if message.audio:
        return "audio"
    if message.voice:
        return "voice"
    if message.photo:
        return "photo"
    if message.animation:
        return "animation"
    if message.document:
        return "document"
    if message.sticker:
        return "sticker"
    return ""


def matches_message_filters(message, media_types, include_keywords, exclude_keywords):
    category = message_category(message)
    if not category or (media_types and category not in media_types):
        return False
    media = getattr(message, category, None)
    if category == "audio" and media is None:
        media = getattr(message, "voice", None)
    filename = getattr(media, "file_name", "") if media else ""
    searchable = " ".join((message.caption or "", message.text or "", filename or "")).casefold()
    if include_keywords and not any(word in searchable for word in include_keywords):
        return False
    return not any(word in searchable for word in exclude_keywords)


def clean_keyword_tags(text, keywords):
    cleaned = text or ""
    for keyword in keywords:
        if keyword:
            cleaned = re.sub(re.escape(keyword), "", cleaned, flags=re.IGNORECASE)
    return cleaned.strip()


def iter_message_ids(first_id, last_id):
    if first_id <= 0 or last_id < first_id:
        raise ValueError("Enter a valid inclusive message ID range")
    return range(first_id, last_id + 1)
