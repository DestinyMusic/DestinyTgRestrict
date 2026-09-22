def _u16(b, o): return int.from_bytes(b[o:o + 2], "little")
def _u32(b, o): return int.from_bytes(b[o:o + 4], "little")
def _u64(b, o): return int.from_bytes(b[o:o + 8], "little")

def _zip64_sizes(extra, uncomp, comp, need_offset=False, offset=0):
    i = 0
    while i + 4 <= len(extra):
        hid, hsz = _u16(extra, i), _u16(extra, i + 2)
        body = extra[i + 4:i + 4 + hsz]
        if hid == 0x0001:
            vals = [_u64(body, j) for j in range(0, (len(body) // 8) * 8, 8)]
            k = 0
            if uncomp == 0xFFFFFFFF and k < len(vals): uncomp = vals[k]; k += 1
            if comp == 0xFFFFFFFF and k < len(vals): comp = vals[k]; k += 1
            if need_offset and offset == 0xFFFFFFFF and k < len(vals): offset = vals[k]; k += 1
            break
        i += 4 + hsz
    return uncomp, comp, offset

def parse_local_header(buf):
    if len(buf) < 30 or buf[0:4] != b"PK\x03\x04": return None
    flag, method = _u16(buf, 6), _u16(buf, 8)
    comp, uncomp = _u32(buf, 18), _u32(buf, 22)
    name_len, extra_len = _u16(buf, 26), _u16(buf, 28)
    name = buf[30:30 + name_len].decode("utf-8", "ignore")
    extra = buf[30 + name_len:30 + name_len + extra_len]
    if uncomp == 0xFFFFFFFF or comp == 0xFFFFFFFF: uncomp, comp, _ = _zip64_sizes(extra, uncomp, comp)
    return {"method": method, "name": name, "data_offset": 30 + name_len + extra_len, "size": uncomp, "comp_size": comp, "has_descriptor": bool(flag & 0x08)}

def _parse_central_directory_full(tail, tail_base, zip_size):
    eocd = tail.rfind(b"PK\x05\x06")
    if eocd < 0: return []
    cd_offset = _u32(tail, eocd + 16)
    cd_records = _u16(tail, eocd + 10)
    z64loc = tail.rfind(b"PK\x06\x07")
    if cd_offset == 0xFFFFFFFF and z64loc >= 0:
        rel = _u64(tail, z64loc + 8) - tail_base
        if 0 <= rel < len(tail) and tail[rel:rel + 4] == b"PK\x06\x06": 
            cd_offset = _u64(tail, rel + 48)
            cd_records = _u64(tail, rel + 32)
    rel_cd = cd_offset - tail_base
    if rel_cd < 0 or rel_cd >= len(tail): return []
    
    entries = []
    o = rel_cd
    for _ in range(cd_records):
        if o + 46 > len(tail) or tail[o:o+4] != b"PK\x01\x02": break
        method, comp, uncomp = _u16(tail, o + 10), _u32(tail, o + 20), _u32(tail, o + 24)
        name_len, extra_len, comment_len = _u16(tail, o + 28), _u16(tail, o + 30), _u16(tail, o + 32)
        local_offset = _u32(tail, o + 42)
        name = tail[o + 46:o + 46 + name_len].decode("utf-8", "ignore")
        extra = tail[o + 46 + name_len:o + 46 + name_len + extra_len]
        if uncomp == 0xFFFFFFFF or comp == 0xFFFFFFFF or local_offset == 0xFFFFFFFF: 
            uncomp, comp, local_offset = _zip64_sizes(extra, uncomp, comp, need_offset=True, offset=local_offset)
        
        entries.append({"method": method, "name": name, "size": uncomp, "comp_size": comp, "local_offset": local_offset})
        o += 46 + name_len + extra_len + comment_len
    return entries

async def get_zip_playlist(read_fn, zip_size):
    try:
        tail_len = min(262144, zip_size)
        tail = await read_fn(zip_size - tail_len, tail_len)
        entries = _parse_central_directory_full(tail, zip_size - tail_len, zip_size)
        valid_exts = (".flac", ".mp3", ".m4a", ".ogg", ".wav", ".aac", ".wma", ".opus", ".dsf", ".ape", ".mka", ".alac", ".mp4", ".mkv", ".webm")
        playlist = []
        for idx, e in enumerate(entries):
            if e["name"].lower().endswith(valid_exts) and e["method"] == 0:
                e["original_index"] = idx
                e["display_name"] = e["name"].split("/")[-1].split("\\")[-1]
                playlist.append(e)
        return playlist
    except Exception: return []

async def resolve_specific_zip_entry(read_fn, entry):
    try:
        lh_buf = await read_fn(entry["local_offset"], min(4096, entry["size"] + 4096))
        lh = parse_local_header(lh_buf)
        if not lh: return None
        data_offset = entry["local_offset"] + lh["data_offset"]
        return {"method": 0, "name": entry["name"], "data_offset": data_offset, "size": entry["size"], "comp_size": entry["comp_size"]}
    except Exception: return None

CLIENT_MSG_CACHE = {}

async def get_client_msg(client, chat_id, msg_id):
    """Caches Telegram messages per-client. Auto-wipes dead sessions mid-fetch."""
    key = (id(client), chat_id, msg_id)
    if key not in CLIENT_MSG_CACHE:
        try:
            msg = await client.get_messages(chat_id, msg_id)
            if getattr(msg, "empty", True) or not (msg.document or msg.video or msg.audio):
                raise ValueError(f"Empty Message for client {getattr(client, 'name', 'Unknown')}")
            CLIENT_MSG_CACHE[key] = msg
        except (AuthKeyUnregistered, UserDeactivated, UserDeactivatedBan) as e:
            if getattr(client, "name", "").startswith("User_"):
                try:
                    uid = int(client.name.split("_")[1])
                    import asyncio
                    asyncio.create_task(auto_wipe_dead_session(client, uid))
                except Exception: pass
            raise e
    return CLIENT_MSG_CACHE[key]

async def fetch_single_chunk(client, chat_id, msg_id, offset, limit):
    """Fetches a chunk continuously. Translates raw bytes into Pyrogram Chunk Indexes."""
    import math
    import asyncio
    CHUNK_SIZE = 1048576
    
    # 🟢 CRITICAL FIX: Pyrogram offset expects CHUNK INDEX, not raw bytes!
    chunk_index = offset // CHUNK_SIZE
    skip_bytes = offset % CHUNK_SIZE
    
    target_bytes = limit
    # Calculate how many 1MB chunks we need to fetch to satisfy the request
    total_bytes_to_fetch = skip_bytes + target_bytes
    chunk_limit = math.ceil(total_bytes_to_fetch / CHUNK_SIZE)
    
    for attempt in range(6): 
        if not getattr(client, "is_connected", False):
            try: await client.connect()
            except Exception: pass

        current_skip = skip_bytes
        try:
            msg = await get_client_msg(client, chat_id, msg_id)
            data = bytearray()
            
            async def fetch_continuous():
                nonlocal current_skip
                # 🟢 Pass the correct Chunk Index (e.g. 1) and Chunk Limit (e.g. 4)
                async for chunk in client.stream_media(msg, offset=chunk_index, limit=chunk_limit):
                    if current_skip > 0:
                        if len(chunk) <= current_skip:
                            current_skip -= len(chunk)
                            continue
                        else:
                            chunk = chunk[current_skip:]
                            current_skip = 0
                            
                    data.extend(chunk)
                    if len(data) >= target_bytes:
                        break
                        
            # Allow enough time for large blocks (e.g. 3MB chunk = 15 seconds max)
            dynamic_timeout = max(15.0, (target_bytes / 1024 / 1024) * 5.0)
            await asyncio.wait_for(fetch_continuous(), timeout=dynamic_timeout)
                    
            if not data: 
                raise ValueError("EOF Reached or Empty Chunk")
            return bytes(data[:target_bytes])
            
        except FloodWait as e:
            await asyncio.sleep(e.value + 1)
        except Exception as e:
            if attempt == 5: raise e
            await asyncio.sleep(1.5 + attempt) 
            
    raise TimeoutError("Exceeded max retries for chunk")

async def parallel_stream_generator(fallback_client, chat_id, msg_parts, start_byte, total_length, chunk_size=3 * 1024 * 1024, concurrency=None):
    """Fast Telegram range generator with cached client selection and continuous work units."""
    if total_length <= 0:
        return

    working_pool = []
    user_id = 0
    if fallback_client in USER_CLIENTS.values():
        for uid, candidate in USER_CLIENTS.items():
            if candidate is fallback_client:
                user_id = uid; break

    user_worker_bots = list(USER_WORKER_BOTS.get(user_id, []))
    for c in user_worker_bots:
        try:
            if getattr(c, "is_connected", False): working_pool.append(c)
        except Exception: pass
            
    if fallback_client:
        try:
            if getattr(fallback_client, "is_connected", False): working_pool.append(fallback_client)
        except Exception: pass

    if not working_pool:
        working_pool = [app]
    
    # 🟢 Determine safe concurrency dynamically based on hardware!
    safe_concurrency = len(working_pool)
    if concurrency is not None:
        safe_concurrency = min(concurrency, safe_concurrency)
    # Bound it by our RAM limit to prevent Out-Of-Memory kills
    safe_concurrency = min(safe_concurrency, DYNAMIC_CONCURRENCY)
    safe_concurrency = max(1, safe_concurrency)

    # 🟢 FIX: Use dynamic chunk size based on server RAM!
    actual_chunk_size = DYNAMIC_CHUNK_SIZE

    range_start = int(start_byte)
    range_end = range_start + int(total_length)
    units = []
    
    for part in msg_parts:
        p_start = int(part["start"])
        p_end = int(part["end"])
        if p_end <= range_start or p_start >= range_end:
            continue
        cursor = max(range_start, p_start)
        limit_end = min(range_end, p_end)
        while cursor < limit_end:
            take = min(int(actual_chunk_size), limit_end - cursor)
            units.append((part, cursor - p_start, take))
            cursor += take

    if not units:
        return

    if safe_concurrency == 1:
        client = working_pool[0]
        for part, internal_offset, internal_limit in units:
            try:
                yield await fetch_single_chunk(client, chat_id, part["msg_id"], internal_offset, internal_limit)
            except Exception:
                raise
        return

    # 🟢 Multi-Bot Parallel Path with Ghost Task Kill Switch
    cursor_idx = 0
    import asyncio
    tasks = []
    
    try:
        while cursor_idx < len(units):
            batch = units[cursor_idx:cursor_idx + safe_concurrency]

            async def _fetch_with_failover(unit_idx, unit):
                part, internal_offset, internal_limit = unit
                preferred = working_pool[unit_idx % len(working_pool)]
                candidates = [preferred] + [c for c in working_pool if c is not preferred]
                last_exc = None
                for client in candidates:
                    try:
                        return await fetch_single_chunk(client, chat_id, part["msg_id"], internal_offset, internal_limit)
                    except Exception as exc:
                        last_exc = exc
                raise last_exc or RuntimeError("Telegram chunk fetch failed across all bots")

            # 🟢 create_task() starts them all simultaneously and yields data instantly
            tasks = [asyncio.create_task(_fetch_with_failover(i, unit)) for i, unit in enumerate(batch)]
            
            for task in tasks:
                result = await task
                if result:
                    yield result
                    
            cursor_idx += len(batch)
            tasks.clear()
            
    finally:
        # 🟢 THE KILL SWITCH: If you skip or pause, instantly kill all active worker bots!
        for task in tasks:
            if not task.done():
                task.cancel()
                
USER_STREAM_BOTS = defaultdict(list)
USER_TASK_BOTS = defaultdict(list)

