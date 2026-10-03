import asyncio
import hashlib
import json
import os
import threading
import uuid
from urllib.parse import urlparse

from pyrogram import Client, filters
from pyrogram.errors import SessionPasswordNeeded
from pyrogram.handlers import MessageHandler
from task_filters import (
    clean_keyword_tags,
    is_protected,
    deliver_task_message,
    iter_message_ids,
    matches_message_filters,
    message_category,
    split_filter_values,
)

_pending_client = None
_pending_phone = None
_pending_code_hash = None
_active_client = None
_storage_directory = None
_watch_loop = None
_watch_thread = None
_watch_client = None
_watchers = {}
_download_cancellations = {}
_download_lock = threading.Lock()
_worker_loop = None
_worker_thread = None
_stream_workers = []
_task_workers = []
_worker_positions = {"stream": 0, "task": 0}
_worker_lock = threading.Lock()
_worker_config_lock = threading.Lock()
_stream_loop = None
_stream_thread = None
_stream_client = None
_stream_session = None
_active_media_streams = {}


def set_storage_directory(path):
    global _storage_directory
    _storage_directory = path
    os.makedirs(path, exist_ok=True)


def runtime_status():
    import pyrogram

    return {
        "runtime": "embedded",
        "engine": "destiny-device",
        "telegram_client_version": pyrogram.__version__,
    }


def _ensure_worker_loop():
    global _worker_loop, _worker_thread
    if _worker_loop is not None and _worker_thread is not None and _worker_thread.is_alive():
        return
    _worker_loop = asyncio.new_event_loop()

    def run_loop():
        asyncio.set_event_loop(_worker_loop)
        _worker_loop.run_forever()

    _worker_thread = threading.Thread(target=run_loop, name="destiny-worker-pools", daemon=True)
    _worker_thread.start()


def configure_worker_pools(api_id, api_hash, stream_tokens, task_tokens):
    global _stream_workers, _task_workers
    if _storage_directory is None:
        raise RuntimeError("Local storage is not initialized")
    streams = [token.strip() for token in str(stream_tokens or "").splitlines()
               if ":" in token]
    tasks = [token.strip() for token in str(task_tokens or "").splitlines()
             if ":" in token]

    async def replace_pool(existing, tokens, prefix):
        for client in existing:
            try:
                await client.stop()
            except Exception:
                pass
        clients = []
        errors = []
        for index, token in enumerate(tokens, start=1):
            client = Client(prefix + str(index), api_id=int(api_id), api_hash=api_hash,
                            bot_token=token, no_updates=True, workers=4,
                            workdir=_storage_directory, loop=_worker_loop)
            try:
                await client.start()
                clients.append(client)
            except Exception as error:
                errors.append(str(error))
                try:
                    await client.stop()
                except Exception:
                    pass
        return clients, errors

    async def configure():
        new_streams, stream_errors = await replace_pool(
            _stream_workers, streams, "destiny-stream-worker-")
        new_tasks, task_errors = await replace_pool(
            _task_workers, tasks, "destiny-task-worker-")
        return new_streams, new_tasks, stream_errors + task_errors

    with _worker_config_lock:
        _ensure_worker_loop()
        future = asyncio.run_coroutine_threadsafe(configure(), _worker_loop)
        _stream_workers, _task_workers, errors = future.result(timeout=180)
    return json.dumps({"stream_workers": len(_stream_workers),
                       "task_workers": len(_task_workers), "errors": errors})


def get_worker_status():
    return json.dumps({"stream_workers": len(_stream_workers),
                       "task_workers": len(_task_workers)})


def _next_worker(pool_name):
    clients = _stream_workers if pool_name == "stream" else _task_workers
    connected = [client for client in clients if getattr(client, "is_connected", False)]
    if not connected:
        return None
    with _worker_lock:
        position = _worker_positions[pool_name] % len(connected)
        _worker_positions[pool_name] += 1
    return connected[position]


async def _invoke_worker(client, method_name, *args, **kwargs):
    operation = getattr(client, method_name)(*args, **kwargs)
    if _worker_loop is None:
        return await operation
    future = asyncio.run_coroutine_threadsafe(operation, _worker_loop)
    return await asyncio.wrap_future(future)


def _ensure_stream_loop():
    global _stream_loop, _stream_thread
    if _stream_loop is not None and _stream_thread is not None and _stream_thread.is_alive():
        return
    _stream_loop = asyncio.new_event_loop()

    def run_loop():
        asyncio.set_event_loop(_stream_loop)
        _stream_loop.run_forever()

    _stream_thread = threading.Thread(target=run_loop, name="destiny-media-stream", daemon=True)
    _stream_thread.start()


def open_telegram_media(api_id, api_hash, session_string, link):
    global _stream_client, _stream_session
    if _storage_directory is None:
        raise RuntimeError("Local storage is not initialized")
    chat_id, message_id = parse_message_link(link)
    _ensure_stream_loop()

    async def open_media():
        global _stream_client, _stream_session
        if _stream_client is None or _stream_session != session_string:
            if _stream_client is not None:
                try:
                    await _stream_client.stop()
                except Exception:
                    pass
            _stream_client = Client(
                "destiny-device-stream", api_id=int(api_id), api_hash=api_hash,
                session_string=session_string, no_updates=True, workers=2,
                workdir=_storage_directory, loop=_stream_loop)
            await _stream_client.start()
            _stream_session = session_string

        message = None
        selected_client = None
        for worker in list(_stream_workers):
            if not getattr(worker, "is_connected", False):
                continue
            try:
                message = await _invoke_worker(worker, "get_messages", chat_id, message_id)
                if message and not message.empty:
                    selected_client = worker
                    break
            except Exception:
                continue
        if message is None or message.empty:
            message = await _stream_client.get_messages(chat_id, message_id)
            selected_client = _stream_client
        if message is None or message.empty:
            raise ValueError("Telegram media message was not found or is inaccessible")
        if is_protected(message):
            raise ValueError("This Telegram message is protected")
        media = message.document or message.video or message.audio
        if media is None:
            raise ValueError("This Telegram message has no streamable media")
        size = int(getattr(media, "file_size", 0) or 0)
        if size <= 0:
            raise ValueError("Telegram did not provide the media size")
        stream_id = uuid.uuid4().hex
        file_name = (getattr(media, "file_name", None)
                     or "telegram-{}".format(message_id))
        _active_media_streams[stream_id] = (selected_client, message, size)
        return json.dumps({
            "stream_id": stream_id,
            "file_name": file_name,
            "mime_type": getattr(media, "mime_type", None) or "application/octet-stream",
            "file_size": size,
        })

    return asyncio.run_coroutine_threadsafe(open_media(), _stream_loop).result(timeout=120)


def read_telegram_media_range(stream_id, offset, length):
    stream = _active_media_streams.get(str(stream_id))
    if stream is None:
        raise ValueError("Telegram stream is closed")
    client, message, size = stream
    start = max(0, int(offset))
    count = min(max(0, int(length)), size - start)
    if count <= 0:
        return b""
    chunk_size = 1024 * 1024
    chunk_index = start // chunk_size
    skip_bytes = start % chunk_size
    chunk_limit = (skip_bytes + count + chunk_size - 1) // chunk_size

    async def read_range():
        data = bytearray()
        skip = skip_bytes
        async for chunk in client.stream_media(message, offset=chunk_index, limit=chunk_limit):
            if skip:
                if len(chunk) <= skip:
                    skip -= len(chunk)
                    continue
                chunk = chunk[skip:]
                skip = 0
            data.extend(chunk)
            if len(data) >= count:
                break
        return bytes(data[:count])

    loop = _worker_loop if client in _stream_workers else _stream_loop
    return asyncio.run_coroutine_threadsafe(read_range(), loop).result(timeout=180)


def close_telegram_media(stream_id):
    _active_media_streams.pop(str(stream_id), None)
    return "CLOSED"


def get_chats(api_id, api_hash, session_string):
    client = Client(
        "destiny-device-chat-picker",
        api_id=int(api_id),
        api_hash=api_hash,
        session_string=session_string,
        in_memory=True,
        no_updates=True,
        workers=1,
        workdir=_storage_directory,
    )

    async def load_chats():
        await client.start()
        try:
            chats = []
            async for dialog in client.get_dialogs(limit=500):
                chat = dialog.chat
                title = (getattr(chat, "title", None)
                         or getattr(chat, "first_name", None)
                         or getattr(chat, "username", None)
                         or str(chat.id))
                chats.append({
                    "id": str(chat.id),
                    "title": title,
                    "username": getattr(chat, "username", None) or "",
                    "type": str(getattr(chat, "type", "unknown")),
                    "is_forum": bool(getattr(chat, "is_forum", False)),
                })
            return json.dumps(chats)
        finally:
            await client.stop()

    return client.loop.run_until_complete(load_chats())


def get_forum_topics(api_id, api_hash, session_string, chat_reference):
    chat_reference = str(chat_reference or "").strip()
    if chat_reference.startswith("@"):
        chat_id = chat_reference[1:]
    else:
        chat_id = _parse_source_chat(chat_reference)
    client = Client(
        "destiny-device-topic-picker",
        api_id=int(api_id),
        api_hash=api_hash,
        session_string=session_string,
        in_memory=True,
        no_updates=True,
        workers=1,
        workdir=_storage_directory,
    )

    async def load_topics():
        await client.start()
        try:
            topics = []
            async for topic in client.get_forum_topics(chat_id, limit=250):
                topics.append({"id": str(topic.id), "title": topic.title})
            return json.dumps(topics)
        finally:
            await client.stop()

    return client.loop.run_until_complete(load_topics())


def send_login_code(api_id, api_hash, phone):
    global _pending_client, _pending_phone, _pending_code_hash
    if _storage_directory is None:
        raise RuntimeError("Local storage is not initialized")
    client = Client(
        "destiny-device-login",
        api_id=int(api_id),
        api_hash=api_hash,
        in_memory=True,
        no_updates=True,
        workers=1,
        workdir=_storage_directory,
    )

    async def request_code():
        await client.connect()
        return await client.send_phone_number_code(phone)

    try:
        sent_code = client.loop.run_until_complete(request_code())
    except Exception:
        client.loop.close()
        raise
    _pending_client = client
    _pending_phone = phone
    _pending_code_hash = sent_code.phone_code_hash
    return "CODE_SENT"


def verify_login_code(phone, code):
    if _pending_client is None or phone != _pending_phone:
        raise RuntimeError("Request a new Telegram login code first")

    async def verify():
        return await _pending_client.sign_in(phone, _pending_code_hash, code)

    try:
        _pending_client.loop.run_until_complete(verify())
    except SessionPasswordNeeded:
        return "PASSWORD_REQUIRED"
    return _finish_login()


def verify_login_password(password):
    if _pending_client is None:
        raise RuntimeError("Request a new Telegram login code first")

    async def verify():
        return await _pending_client.check_password(password)

    _pending_client.loop.run_until_complete(verify())
    return _finish_login()


def _finish_login():
    global _pending_client, _pending_phone, _pending_code_hash, _active_client
    client = _pending_client

    async def finish():
        await client.invoke(__import__("pyrogram").raw.functions.updates.GetState())
        client.me = await client.get_me()
        await client.initialize()
        return await client.export_session_string()

    session = client.loop.run_until_complete(finish())
    _active_client = client
    _pending_client = None
    _pending_phone = None
    _pending_code_hash = None
    return "AUTH_OK:" + session


def parse_message_link(link):
    parsed = urlparse(link if "://" in link else "https://" + link)
    if parsed.netloc.lower() not in {"t.me", "www.t.me", "telegram.me", "www.telegram.me"}:
        raise ValueError("Enter a Telegram message link")
    parts = [part for part in parsed.path.split("/") if part]
    if parts and parts[0] == "s":
        parts.pop(0)
    if len(parts) < 2:
        raise ValueError("The link must include a message ID")
    message_id = int(parts[-1])
    if parts[0] == "c":
        if len(parts) < 3:
            raise ValueError("The private channel link is incomplete")
        chat_id = int("-100" + parts[1])
    else:
        chat_id = parts[0]
    return chat_id, message_id


async def _retry_task_operation(operation, attempts=3):
    for attempt in range(attempts):
        try:
            return await operation()
        except Exception as error:
            if attempt + 1 == attempts:
                raise
            wait_seconds = max(2 ** attempt, int(getattr(error, "value", 0) or 0))
            await asyncio.sleep(min(wait_seconds, 60))


async def _download_and_forward_message(client, message, category, destination,
                                        destination_thread_id, cleanup_keywords,
                                        download_directory, persist_local, uploader=None):
    os.makedirs(download_directory, exist_ok=True)
    local_path = await _retry_task_operation(lambda: client.download_media(
        message, file_name=download_directory + os.sep))
    if not local_path:
        raise RuntimeError("Telegram did not provide a downloadable file")

    completed = False
    media = getattr(message, category, None)
    mime_type = getattr(media, "mime_type", None) or {
        "video": "video/mp4",
        "audio": "audio/mpeg",
        "voice": "audio/ogg",
        "photo": "image/jpeg",
        "animation": "video/mp4",
        "sticker": "image/webp",
    }.get(category, "application/octet-stream")
    caption = _clean_watch_caption(message.caption, cleanup_keywords)
    caption_entities = (message.caption_entities
                        if caption == (message.caption or "") else None)
    thread_arguments = {"message_thread_id": destination_thread_id} \
        if destination_thread_id else {}

    async def deliver(method_name, *args, **kwargs):
        if uploader is not None and getattr(uploader, "is_connected", False):
            try:
                return await _retry_task_operation(lambda:
                    _invoke_worker(uploader, method_name, *args, **kwargs))
            except Exception:
                pass
        return await _retry_task_operation(lambda:
            getattr(client, method_name)(*args, **kwargs))

    try:
        if category == "video":
            await deliver("send_video",
                destination, local_path, caption=caption,
                caption_entities=caption_entities,
                duration=getattr(media, "duration", 0),
                width=getattr(media, "width", 0), height=getattr(media, "height", 0),
                **thread_arguments)
        elif category == "audio":
            await deliver("send_audio",
                destination, local_path, caption=caption,
                caption_entities=caption_entities,
                duration=getattr(media, "duration", 0),
                performer=getattr(media, "performer", None),
                title=getattr(media, "title", None), **thread_arguments)
        elif category == "voice":
            await deliver("send_voice",
                destination, local_path, caption=caption,
                caption_entities=caption_entities,
                duration=getattr(media, "duration", 0), **thread_arguments)
        elif category == "photo":
            await deliver("send_photo",
                destination, local_path, caption=caption,
                caption_entities=caption_entities, **thread_arguments)
        elif category == "animation":
            await deliver("send_animation",
                destination, local_path, caption=caption,
                caption_entities=caption_entities, **thread_arguments)
        elif category == "sticker":
            await deliver("send_sticker", destination, local_path, **thread_arguments)
        elif category == "document":
            await deliver("send_document",
                destination, local_path, caption=caption,
                caption_entities=caption_entities, **thread_arguments)
        else:
            raise ValueError("Unsupported media category: " + str(category))
        completed = True
        return local_path, mime_type
    finally:
        if (not persist_local or not completed) and os.path.isfile(local_path):
            try:
                os.remove(local_path)
            except OSError:
                pass


def download_media_for_editing(api_id, api_hash, session_string, link):
    if _storage_directory is None:
        raise RuntimeError("Local storage is not initialized")
    chat_id, message_id = parse_message_link(link)
    client = Client(
        "destiny-device-editor-task",
        api_id=int(api_id),
        api_hash=api_hash,
        session_string=session_string,
        no_updates=True,
        workers=1,
        workdir=_storage_directory,
    )

    async def stage_media():
        await client.start()
        try:
            message = None
            source_client = client
            for worker in list(_stream_workers):
                if not getattr(worker, "is_connected", False):
                    continue
                try:
                    candidate = await _invoke_worker(
                        worker, "get_messages", chat_id, message_id)
                    if candidate is not None and not candidate.empty:
                        message = candidate
                        source_client = worker
                        break
                except Exception:
                    continue
            if message is None:
                message = await client.get_messages(chat_id, message_id)
            if message is None or message.empty:
                raise ValueError("Telegram media message was not found or is inaccessible")
            if is_protected(message):
                raise ValueError("This Telegram message is protected")
            category = message_category(message)
            media = getattr(message, category, None) if category else None
            if media is None:
                raise ValueError("The Telegram message does not contain editable media")
            import_directory = os.path.join(_storage_directory, "editor_imports")
            os.makedirs(import_directory, exist_ok=True)
            try:
                if source_client is client:
                    local_path = await client.download_media(
                        message, file_name=import_directory + os.sep)
                else:
                    local_path = await _invoke_worker(
                        source_client, "download_media", message,
                        file_name=import_directory + os.sep)
            except Exception:
                if source_client is client:
                    raise
                message = await client.get_messages(chat_id, message_id)
                if message is None or message.empty or is_protected(message):
                    raise
                local_path = await client.download_media(
                    message, file_name=import_directory + os.sep)
            if not local_path:
                raise RuntimeError("Telegram did not provide a downloadable file")
            mime_type = getattr(media, "mime_type", None) or {
                "video": "video/mp4",
                "audio": "audio/mpeg",
                "voice": "audio/ogg",
                "photo": "image/jpeg",
                "animation": "video/mp4",
                "sticker": "image/webp",
            }.get(category, "application/octet-stream")
            return json.dumps({
                "path": local_path,
                "file_name": os.path.basename(local_path),
                "mime_type": mime_type,
            })
        finally:
            await client.stop()

    return client.loop.run_until_complete(stage_media())


def download_message(api_id, api_hash, session_string, link, destination="me"):
    if _storage_directory is None:
        raise RuntimeError("Local storage is not initialized")
    chat_id, message_id = parse_message_link(link)
    client = Client(
        "destiny-device-task",
        api_id=int(api_id),
        api_hash=api_hash,
        session_string=session_string,
        no_updates=True,
        workers=1,
        workdir=_storage_directory,
    )

    async def process_message():
        await client.start()
        try:
            message = await client.get_messages(chat_id, message_id)
            if message is None or message.empty:
                raise ValueError("Telegram message was not found or is inaccessible")
            if is_protected(message):
                raise ValueError("This message is protected and cannot be downloaded by this app")
            if not message.media:
                if not message.text:
                    raise ValueError("This message has no downloadable content")
                await client.send_message(destination, message.text, entities=message.entities)
                return "SUCCESS_TEXT:Message copied to " + str(destination)
            else:
                download_directory = os.path.join(_storage_directory, "downloads")
                os.makedirs(download_directory, exist_ok=True)
                local_path = await client.download_media(
                    message, file_name=download_directory + os.sep)
                if not local_path:
                    raise RuntimeError("Telegram did not provide a downloadable file")
                if message.video:
                    mime_type = "video/" + (message.video.mime_type or "mp4").split("/")[-1]
                    await client.send_video(destination, local_path, caption=message.caption,
                                            caption_entities=message.caption_entities)
                elif message.audio:
                    mime_type = message.audio.mime_type or "audio/mpeg"
                    await client.send_audio(destination, local_path, caption=message.caption,
                                            caption_entities=message.caption_entities)
                elif message.photo:
                    mime_type = "image/jpeg"
                    await client.send_photo(destination, local_path, caption=message.caption,
                                            caption_entities=message.caption_entities)
                else:
                    mime_type = message.document.mime_type if message.document else "application/octet-stream"
                    await client.send_document(destination, local_path, caption=message.caption,
                                               caption_entities=message.caption_entities)
                filename = os.path.basename(local_path)
                return "SUCCESS_FILE|" + filename + "|" + mime_type + "|" + local_path
        finally:
            await client.stop()

    return client.loop.run_until_complete(process_message())


def download_messages(api_id, api_hash, session_string, link, start_id="", end_id="",
                      destination="me", media_types="video,audio,photo,document,animation,voice,sticker,text",
                      include_keywords="", exclude_keywords="", delay_seconds="3",
                      source_thread_id="0", destination_thread_id="0",
                      cleanup_keywords="", task_id="", resume_from_id="",
                      transfer_mode="AUTO"):
    if _storage_directory is None:
        raise RuntimeError("Local storage is not initialized")
    try:
        chat_id, linked_message_id = parse_message_link(link)
    except ValueError:
        chat_id = _parse_source_chat(link)
        linked_message_id = 0
    first_id = int(start_id) if str(start_id).strip() else linked_message_id
    last_id = int(end_id) if str(end_id).strip() else first_id
    checkpoint = int(resume_from_id or 0)
    if checkpoint >= first_id:
        first_id = checkpoint + 1
    if first_id > last_id:
        return "TASK_SUMMARY|downloaded=0,skipped=0,failed=0,cancelled=0"
    message_ids = iter_message_ids(first_id, last_id)
    delay = float(delay_seconds or 3)
    if delay < 3 or delay > 3600:
        raise ValueError("Per-message delay must be between 3 and 3600 seconds")
    source_thread_id = int(source_thread_id or 0)
    destination_thread_id = int(destination_thread_id or 0)

    selected_types = split_filter_values(media_types)
    include = split_filter_values(include_keywords)
    exclude = split_filter_values(exclude_keywords)
    cleanup = [value.strip() for value in (cleanup_keywords or "").split(",") if value.strip()]
    transfer_mode = str(transfer_mode or "AUTO").strip().upper()
    if transfer_mode not in {"FORWARD", "DOWNLOAD", "AUTO"}:
        raise ValueError("Transfer mode must be FORWARD, DOWNLOAD, or AUTO")
    destination = destination or "me"
    task_key = str(task_id or "")
    cancellation = threading.Event()
    if task_key:
        with _download_lock:
            _download_cancellations[task_key] = cancellation
    progress_directory = os.path.join(_storage_directory, "tasks")
    os.makedirs(progress_directory, exist_ok=True)
    progress_path = os.path.join(progress_directory, task_key + ".txt") if task_key else None
    checkpoint_path = os.path.join(progress_directory, task_key + ".checkpoint") if task_key else None
    events_path = os.path.join(progress_directory, task_key + ".jsonl") if task_key else None
    if events_path and checkpoint <= 0:
        with open(events_path, "w", encoding="utf-8"):
            pass

    def write_event(event):
        if not events_path:
            return
        with open(events_path, "a", encoding="ascii") as event_file:
            event_file.write(json.dumps(event, ensure_ascii=True) + "\n")

    def write_progress(state, current, downloaded, skipped, failed):
        if not progress_path:
            return
        temporary_path = progress_path + ".tmp"
        with open(temporary_path, "w", encoding="utf-8") as progress_file:
            progress_file.write("{}|{}|{}|{}|{}|{}".format(
                state, current, last_id - first_id + 1, downloaded, skipped, failed))
        os.replace(temporary_path, progress_path)

    def write_checkpoint(message_id):
        if not checkpoint_path:
            return
        temporary_path = checkpoint_path + ".tmp"
        with open(temporary_path, "w", encoding="ascii") as checkpoint_file:
            checkpoint_file.write(str(message_id))
        os.replace(temporary_path, checkpoint_path)

    client = Client(
        "destiny-device-batch-task",
        api_id=int(api_id),
        api_hash=api_hash,
        session_string=session_string,
        no_updates=True,
        workers=1,
        workdir=_storage_directory,
    )

    async def process_batch():
        downloaded = 0
        skipped = 0
        failed = 0
        cancelled = False
        processed = 0
        client_started = False
        task_state = "COMPLETE"
        processed_album_ids = set()
        download_directory = os.path.join(_storage_directory, "downloads")
        os.makedirs(download_directory, exist_ok=True)
        write_progress("RUNNING", 0, downloaded, skipped, failed)
        try:
            await client.start()
            client_started = True
            for current_id in message_ids:
                processed += 1
                if cancellation.is_set():
                    cancelled = True
                    processed -= 1
                    break
                if current_id in processed_album_ids:
                    skipped += 1
                    write_checkpoint(current_id)
                    write_progress("RUNNING", current_id - first_id + 1,
                                   downloaded, skipped, failed)
                    continue
                try:
                    message = await _retry_task_operation(
                        lambda: client.get_messages(chat_id, current_id))
                    if message is None or message.empty:
                        skipped += 1
                    elif not matches_message_filters(message, selected_types, include, exclude):
                        skipped += 1
                    else:
                        thread_id = getattr(message, "message_thread_id", None)
                        if thread_id is None:
                            thread_id = getattr(message, "reply_to_top_message_id", None)
                        if source_thread_id and int(thread_id or 0) != source_thread_id:
                            skipped += 1
                            write_checkpoint(current_id)
                            write_progress("RUNNING", current_id - first_id + 1,
                                           downloaded, skipped, failed)
                            continue
                        thread_argument = {"message_thread_id": destination_thread_id} \
                            if destination_thread_id else {}
                        uploader = _next_worker("task")
                        if category := message_category(message):
                            if category == "text":
                                text = _clean_watch_caption(message.text, cleanup)
                                entities = message.entities if text == (message.text or "") else None
                                await _retry_task_operation(lambda: client.send_message(
                                    destination, text, entities=entities,
                                    **thread_argument))
                                downloaded += 1
                                write_checkpoint(current_id)
                                write_progress("RUNNING", current_id - first_id + 1,
                                               downloaded, skipped, failed)
                                continue
                            media_group_id = getattr(message, "media_group_id", None)

                            async def copy_media():
                                if uploader is not None:
                                    try:
                                        if media_group_id is not None:
                                            return await _retry_task_operation(lambda:
                                                _invoke_worker(
                                                    uploader, "copy_media_group",
                                                    chat_id=destination, from_chat_id=chat_id,
                                                    message_id=current_id, **thread_argument))
                                        return await _retry_task_operation(lambda:
                                            _invoke_worker(
                                                uploader, "copy_message", chat_id=destination,
                                                from_chat_id=chat_id, message_id=current_id,
                                                **thread_argument))
                                    except Exception:
                                        pass
                                if media_group_id is not None:
                                    try:
                                        group_messages = await client.get_media_group(
                                            chat_id, current_id)
                                    except Exception:
                                        group_messages = [message]
                                    result = await _retry_task_operation(lambda:
                                        client.copy_media_group(
                                            chat_id=destination, from_chat_id=chat_id,
                                            message_id=current_id, **thread_argument))
                                    if result:
                                        processed_album_ids.update(
                                            int(member.id) for member in group_messages)
                                    return result
                                return await _retry_task_operation(lambda:
                                    client.copy_message(
                                        chat_id=destination, from_chat_id=chat_id,
                                        message_id=current_id, **thread_argument))

                            async def forward_media():
                                message_ids = [current_id]
                                if media_group_id is not None:
                                    try:
                                        group_messages = await client.get_media_group(
                                            chat_id, current_id)
                                        message_ids = [int(member.id)
                                                       for member in group_messages]
                                    except Exception:
                                        pass
                                if uploader is not None:
                                    try:
                                        forwarded = await _retry_task_operation(lambda:
                                            _invoke_worker(
                                                uploader, "forward_messages", destination,
                                                chat_id, message_ids, **thread_argument))
                                        if forwarded:
                                            processed_album_ids.update(message_ids)
                                            return forwarded
                                    except Exception:
                                        pass
                                forwarded = await _retry_task_operation(lambda:
                                    client.forward_messages(
                                        destination, chat_id, message_ids,
                                        **thread_argument))
                                if forwarded:
                                    processed_album_ids.update(message_ids)
                                return forwarded

                            async def download_and_forward():
                                local_path, mime_type = await _download_and_forward_message(
                                    client, message, category, destination,
                                    destination_thread_id, cleanup, download_directory, True,
                                    uploader=uploader)
                                write_event({
                                    "type": "file",
                                    "name": os.path.basename(local_path),
                                    "mime_type": mime_type,
                                    "path": local_path,
                                })
                                return True

                            await deliver_task_message(
                                transfer_mode, message, forward_media, download_and_forward,
                                force_fallback=bool(cleanup) and transfer_mode == "AUTO",
                                copy_operation=copy_media)
                            downloaded += 1
                        else:
                            skipped += 1
                except Exception as error:
                    failed += 1
                write_checkpoint(current_id)
                write_progress("RUNNING", current_id - first_id + 1,
                               downloaded, skipped, failed)
                if delay and current_id < last_id:
                    if await asyncio.to_thread(cancellation.wait, delay):
                        cancelled = True
                        break
        except Exception as error:
            failed += 1
            task_state = "FAILED"
        finally:
            try:
                if client_started:
                    await client.stop()
            except Exception as error:
                failed += 1
                task_state = "FAILED"
            finally:
                if cancelled:
                    task_state = "CANCELLED"
                elif failed and downloaded:
                    task_state = "PARTIAL"
                elif failed:
                    task_state = "FAILED"
                write_progress(task_state, processed, downloaded, skipped, failed)
                if task_key:
                    with _download_lock:
                        _download_cancellations.pop(task_key, None)
        return "TASK_SUMMARY|downloaded={},skipped={},failed={},cancelled={}".format(
            downloaded, skipped, failed, int(cancelled))

    return client.loop.run_until_complete(process_batch())


def cancel_download_task(task_id):
    with _download_lock:
        cancellation = _download_cancellations.get(str(task_id))
    if cancellation is None:
        return "NOT_RUNNING"
    cancellation.set()
    return "CANCEL_REQUESTED"


def _parse_source_chat(link):
    link = str(link or "").strip()
    if link.lstrip("-").isdigit():
        return int(link)
    parsed = urlparse(link if "://" in link else "https://" + link)
    if parsed.netloc.lower() not in {"t.me", "www.t.me", "telegram.me", "www.telegram.me"}:
        raise ValueError("Enter a Telegram source link")
    parts = [part for part in parsed.path.split("/") if part]
    if parts and parts[0] == "s":
        parts.pop(0)
    if not parts or parts[0].startswith("+"):
        raise ValueError("Use a public channel or an accessible private chat link")
    if parts[0] == "c":
        if len(parts) < 2:
            raise ValueError("The private channel link is incomplete")
        return int("-100" + parts[1])
    if parts[0].lstrip("-").isdigit():
        return int(parts[0])
    return parts[0]


def _watch_checkpoint_path(source_chat, destination, source_thread_id, destination_thread_id):
    checkpoint_directory = os.path.join(_storage_directory, "watchers")
    os.makedirs(checkpoint_directory, exist_ok=True)
    identity = "|".join((str(source_chat), str(destination), str(source_thread_id),
                         str(destination_thread_id)))
    digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()
    return os.path.join(checkpoint_directory, digest + ".json")


def _clean_watch_caption(caption, cleanup_keywords):
    return clean_keyword_tags(caption, cleanup_keywords)


def start_watcher(api_id, api_hash, session_string, source_link, destination="me",
                  media_types="video,audio,photo,document,animation,voice,sticker,text",
                  include_keywords="", exclude_keywords="", delay_seconds="0",
                  source_thread_id="0", destination_thread_id="0",
                  cleanup_keywords="", checkpoint_message_id="0",
                  transfer_mode="AUTO"):
    global _watch_loop, _watch_thread, _watch_client
    source_chat = _parse_source_chat(source_link)
    destination = destination or "me"
    source_thread_id = int(source_thread_id or 0)
    destination_thread_id = int(destination_thread_id or 0)
    transfer_mode = str(transfer_mode or "AUTO").strip().upper()
    if transfer_mode not in {"FORWARD", "DOWNLOAD", "AUTO"}:
        raise ValueError("Transfer mode must be FORWARD, DOWNLOAD, or AUTO")
    watcher_key = (str(source_chat), destination, source_thread_id, destination_thread_id)
    if watcher_key in _watchers:
        return "WATCHING|{}".format(_watchers[watcher_key]["last_message_id"])
    if _watch_loop is None or _watch_thread is None or not _watch_thread.is_alive():
        _watch_loop = asyncio.new_event_loop()

        def run_loop():
            asyncio.set_event_loop(_watch_loop)
            _watch_loop.run_forever()

        _watch_thread = threading.Thread(target=run_loop, name="destiny-watcher-loop", daemon=True)
        _watch_thread.start()
        _watch_client = Client(
            "destiny-device-watchers",
            api_id=int(api_id),
            api_hash=api_hash,
            session_string=session_string,
            no_updates=False,
            workers=4,
            workdir=_storage_directory,
            loop=_watch_loop,
        )

        async def connect():
            await _watch_client.start()

        asyncio.run_coroutine_threadsafe(connect(), _watch_loop).result(timeout=90)

    selected_types = split_filter_values(media_types)
    include = split_filter_values(include_keywords)
    exclude = split_filter_values(exclude_keywords)
    cleanup = [value.strip() for value in (cleanup_keywords or "").split(",") if value.strip()]
    delay = max(3.0, min(float(delay_seconds or 3), 3600.0))
    checkpoint_path = _watch_checkpoint_path(source_chat, destination,
                                             source_thread_id, destination_thread_id)
    checkpoint = int(checkpoint_message_id or 0)
    restored_stats = {}
    try:
        with open(checkpoint_path, "r", encoding="utf-8") as checkpoint_file:
            saved_state = json.load(checkpoint_file)
            checkpoint = max(checkpoint, int(saved_state.get("last_message_id", 0)))
            restored_stats = saved_state.get("stats", {})
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        pass

    async def initialize_watcher():
        queue = asyncio.Queue()
        state = {"source_link": source_link, "destination": destination,
                 "source_thread_id": source_thread_id,
                 "destination_thread_id": destination_thread_id,
                 "last_message_id": checkpoint, "pending": [], "ready": False,
                 "queue": queue, "worker": None, "stats": {
                     "detected": int(restored_stats.get("detected", 0)),
                     "success": int(restored_stats.get("success", 0)),
                     "skipped": int(restored_stats.get("skipped", 0)),
                     "failed": int(restored_stats.get("failed", 0)),
                 }}

        def save_checkpoint():
            temporary_path = checkpoint_path + ".tmp"
            with open(temporary_path, "w", encoding="utf-8") as checkpoint_file:
                json.dump({"last_message_id": state["last_message_id"],
                           "stats": state["stats"]}, checkpoint_file)
            os.replace(temporary_path, checkpoint_path)

        async def process_message(message):
            message_id = int(message.id)
            if message_id <= state["last_message_id"]:
                return
            topic_id = getattr(message, "message_thread_id", None)
            if topic_id is None:
                topic_id = getattr(message, "reply_to_top_message_id", None)
            state["stats"]["detected"] = state["stats"].get("detected", 0) + 1
            should_skip = (not matches_message_filters(message, selected_types, include, exclude)
                           or (source_thread_id and int(topic_id or 0) != source_thread_id))
            if should_skip:
                state["stats"]["skipped"] += 1
                state["last_message_id"] = message_id
                save_checkpoint()
                return

            if delay:
                await asyncio.sleep(delay)
            caption = _clean_watch_caption(message.caption, cleanup)
            if message.text:
                caption = _clean_watch_caption(message.text, cleanup)
                send_text = getattr(_watch_client, "send_message")
                thread_arguments = {"message_thread_id": destination_thread_id} \
                    if destination_thread_id else {}
                try:
                    await _retry_task_operation(lambda: send_text(
                        destination, caption, entities=message.entities, **thread_arguments))
                    state["stats"]["success"] += 1
                except Exception:
                    state["stats"]["failed"] += 1
                state["last_message_id"] = message_id
                save_checkpoint()
                return
            media_category = message_category(message)
            uploader = _next_worker("task")

            async def copy_media():
                thread_arguments = {"message_thread_id": destination_thread_id} \
                    if destination_thread_id else {}
                if uploader is not None:
                    try:
                        if getattr(message, "media_group_id", None) is not None:
                            return await _retry_task_operation(lambda:
                                _invoke_worker(
                                    uploader, "copy_media_group", chat_id=destination,
                                    from_chat_id=message.chat.id, message_id=message_id,
                                    **thread_arguments))
                        return await _retry_task_operation(lambda:
                            _invoke_worker(
                                uploader, "copy_message", chat_id=destination,
                                from_chat_id=message.chat.id, message_id=message_id,
                                **thread_arguments))
                    except Exception:
                        pass
                if getattr(message, "media_group_id", None) is not None:
                    try:
                        group_messages = await _watch_client.get_media_group(
                            message.chat.id, message_id)
                    except Exception:
                        group_messages = [message]
                    result = await _retry_task_operation(lambda:
                        _watch_client.copy_media_group(
                            chat_id=destination, from_chat_id=message.chat.id,
                            message_id=message_id, **thread_arguments))
                    if result:
                        state["last_message_id"] = max(
                            [state["last_message_id"]]
                            + [int(member.id) for member in group_messages])
                    return result
                return await _retry_task_operation(lambda:
                    _watch_client.copy_message(
                        chat_id=destination, from_chat_id=message.chat.id,
                        message_id=message_id, **thread_arguments))

            async def forward_media():
                if uploader is not None:
                    try:
                        forwarded = await _retry_task_operation(lambda:
                            _invoke_worker(
                                uploader, "forward_messages", destination,
                                message.chat.id, message_id, **thread_arguments))
                        if forwarded:
                            return forwarded
                    except Exception:
                        pass
                return await _retry_task_operation(lambda:
                    _watch_client.forward_messages(
                        destination, message.chat.id, message_id, **thread_arguments))

            async def download_and_forward():
                await _download_and_forward_message(
                    _watch_client, message, media_category, destination,
                    destination_thread_id, cleanup,
                    os.path.join(_storage_directory, "watcher_transfers"), False,
                    uploader=uploader)
                return True

            try:
                await deliver_task_message(
                    transfer_mode, message, forward_media, download_and_forward,
                    force_fallback=bool(cleanup) and transfer_mode == "AUTO",
                    copy_operation=copy_media)
                state["stats"]["success"] += 1
            except Exception:
                state["stats"]["failed"] += 1
            state["last_message_id"] = max(state["last_message_id"], message_id)
            save_checkpoint()

        async def forward_new_message(client, message):
            if state["ready"]:
                await queue.put(message)
            else:
                state["pending"].append(message)

        handler = MessageHandler(forward_new_message, filters.chat(source_chat))
        group = 100 + len(_watchers)
        _watch_client.add_handler(handler, group=group)
        state["handler"] = handler
        state["group"] = group
        _watchers[watcher_key] = state

        if state["last_message_id"] <= 0:
            async for latest in _watch_client.get_chat_history(source_chat, limit=1):
                state["last_message_id"] = int(latest.id)
                break
            save_checkpoint()
        else:
            missed = []
            async for old_message in _watch_client.get_chat_history(source_chat, limit=0):
                if int(old_message.id) <= state["last_message_id"]:
                    break
                missed.append(old_message)
                if len(missed) >= 5000:
                    break
            for old_message in reversed(missed):
                await process_message(old_message)

        while state["pending"]:
            pending = state["pending"]
            state["pending"] = []
            unique_pending = {int(message.id): message for message in pending}
            for message in sorted(unique_pending.values(), key=lambda item: int(item.id)):
                await process_message(message)
        state["ready"] = True

        async def worker():
            while True:
                message = await queue.get()
                try:
                    await process_message(message)
                finally:
                    queue.task_done()

        state["worker"] = asyncio.create_task(worker())
        return state["last_message_id"]

    checkpoint = asyncio.run_coroutine_threadsafe(
        initialize_watcher(), _watch_loop).result(timeout=180)
    return "WATCHING|" + str(checkpoint)


def stop_watchers():
    global _watch_loop, _watch_thread, _watch_client, _watchers
    if _watch_loop is None or _watch_client is None:
        return "STOPPED"
    loop = _watch_loop
    client = _watch_client

    async def stop_client():
        for state in list(_watchers.values()):
            client.remove_handler(state["handler"], state["group"])
            if state["worker"] is not None:
                state["worker"].cancel()
        workers = [state["worker"] for state in _watchers.values() if state["worker"] is not None]
        if workers:
            await asyncio.gather(*workers, return_exceptions=True)
        await client.stop()

    asyncio.run_coroutine_threadsafe(stop_client(), loop).result(timeout=30)
    loop.call_soon_threadsafe(loop.stop)
    if _watch_thread is not None:
        _watch_thread.join(timeout=5)
    _watch_loop = None
    _watch_thread = None
    _watch_client = None
    _watchers = {}
    return "STOPPED"


def remove_watcher(source_link, destination="me", source_thread_id="0",
                   destination_thread_id="0"):
    global _watchers
    source_chat = _parse_source_chat(source_link)
    watcher_key = (str(source_chat), destination or "me", int(source_thread_id or 0),
                   int(destination_thread_id or 0))
    watcher = _watchers.pop(watcher_key, None)
    if watcher is None or _watch_loop is None or _watch_client is None:
        return "NOT_RUNNING"
    async def remove_handler():
        _watch_client.remove_handler(watcher["handler"], watcher["group"])
        worker = watcher.get("worker")
        if worker is not None:
            worker.cancel()
            await asyncio.gather(worker, return_exceptions=True)

    asyncio.run_coroutine_threadsafe(remove_handler(), _watch_loop).result(timeout=15)
    if not _watchers:
        stop_watchers()
    return "STOPPED"


def get_watcher_status():
    return json.dumps([
        {
            "source": state["source_link"],
            "destination": state["destination"],
            "source_thread_id": state["source_thread_id"],
            "destination_thread_id": state["destination_thread_id"],
            "last_message_id": state["last_message_id"],
            "stats": state["stats"],
        }
        for state in _watchers.values()
    ])