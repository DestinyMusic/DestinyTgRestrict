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
        valid_exts = (".flac", ".mp3", ".m4a", ".ogg", ".wav", ".aac", ".wma", ".opus", ".dsf", ".ape", ".mka", ".alac", ".mp4", ".mkv", ".webm", ".m4v", ".mov", ".ts", ".avi")
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
