# ==============================================================================
# --- FULL-STACK STREMIO WEB ENGINE & AUTHENTICATION BRIDGE ---
# ==============================================================================
try:
    from aiohttp import web
except ImportError:
    web = None

import hashlib
import hmac
import json
import secrets
import re
from urllib.parse import urlencode

WEB_AUTH_COOKIE = "web_auth"
WEB_SESSION_TTL = 12 * 60 * 60
STREAM_LINK_TTL = 12 * 60 * 60
PASSWORD_RESET_REQUESTS = {}
STREAM_AUTH_PATHS = {
    "/api/stream": {"link", "quality", "audio_idx", "audio_codec", "start", "transcode", "force_x264", "hevc", "ac3", "opus", "flac", "vp9", "av1", "zip_idx", "external"},
    "/api/tg_stream": {"link", "chat_id", "msg_id", "range", "zip_idx"},
    "/api/direct_stream": {"url", "zip_idx"},
}
PUBLIC_AUTH_PATHS = {
    "/api/auth/login",
    "/api/auth/forgot",
    "/api/auth/reset",
}
API_SUCCESS_LOG_PATHS = {
    "/api/auth/login", "/api/auth/reset", "/api/auth/logout", "/api/auth/password",
    "/api/auth/stream-link", "/api/task/add", "/api/task/cancel",
    "/api/watcher/add", "/api/watcher/cancel", "/api/edit_media",
    "/api/mediainfo", "/api/spectrogram", "/api/media_probe",
    "/api/playlist", "/api/subtitles", "/api/tg/send_code",
    "/api/tg/verify", "/api/tg/verify_2fa", "/api/tg/logout",
    "/api/settings/tokens", "/api/stream/kill", "/api/editor_cancel",
    "/api/admin/users/add", "/api/admin/users/remove",
    "/api/cookies/upload", "/api/cookies/delete", "/api/topics", "/api/chats",
}


def _diagnostic_safe_reason(value):
    text = str(value or "")
    text = re.sub(r"https?://[^\s\]\[<>'\"]+", "[url-redacted]", text)
    text = re.sub(
        r"(?i)\b(token|password|api[_-]?hash|authorization|cookie)(\s*[:=]\s*)[^\s,;]+",
        r"\1\2[redacted]",
        text,
    )
    return text[:400]


def _log_api_result(request, result, http_status, elapsed_ms, reason=None):
    user_id = request.get("authenticated_user_id", "-")
    message = (
        "API_RESULT request_id=%s method=%s path=%s user_id=%s http_status=%s "
        "result=%s duration_ms=%.1f reason=%r"
    )
    args = (
        request.get("diagnostic_request_id", "-"),
        request.method,
        request.path,
        user_id,
        http_status,
        result,
        elapsed_ms,
        _diagnostic_safe_reason(reason),
    )
    if result == "FAILED":
        logger.warning(message, *args)
    else:
        logger.info(message, *args)


@web.middleware
async def _api_diagnostics_middleware(request, handler):
    if not request.path.startswith("/api/"):
        return await handler(request)

    request["diagnostic_request_id"] = uuid.uuid4().hex[:12]
    started = time.monotonic()
    try:
        response = await handler(request)
    except web.HTTPException as exc:
        status = exc.status
        # 🟢 FIX: Add 401 to the ignore list
        if status >= 400 and status not in {401, 416, 499}:
            _log_api_result(request, "FAILED", status, (time.monotonic() - started) * 1000, exc.reason)
        raise
    except Exception as exc:
        _log_api_result(
            request,
            "FAILED",
            500,
            (time.monotonic() - started) * 1000,
            f"{type(exc).__name__}: {exc}",
        )
        raise

    result = "SUCCESS"
    reason = None
    # 🟢 FIX: Add 401 to the ignore list here as well
    if response.status >= 400 and response.status not in {401, 416, 499}:
        result = "FAILED"
        reason = f"HTTP {response.status}"
        # 🟢 CRITICAL FIX: Safe check for StreamResponses to stop the server crashing
        if hasattr(response, "body") and response.content_type.startswith("text/") and response.body:
            reason = response.body[:2048].decode("utf-8", errors="replace")
    elif hasattr(response, "body") and response.content_type == "application/json" and response.body:
        try:
            payload = json.loads(response.body)
            if isinstance(payload, dict) and payload.get("status") == "error":
                result = "FAILED"
                reason = payload.get("message") or "API returned status=error"
        except (TypeError, ValueError):
            pass

    # 🟢 FIX: Hard-block 401 HTTP codes from triggering the logger under any circumstance
    if (result == "FAILED" or request.path in API_SUCCESS_LOG_PATHS) and response.status != 401:
        _log_api_result(request, result, response.status, (time.monotonic() - started) * 1000, reason)
    return response

def _hash_web_password(password):
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1)
    return f"scrypt${salt.hex()}${digest.hex()}"


def _verify_web_password(password, stored_password):
    if not isinstance(password, str) or not isinstance(stored_password, str):
        return False
    if stored_password.startswith("scrypt$"):
        try:
            _, salt_hex, digest_hex = stored_password.split("$", 2)
            salt = bytes.fromhex(salt_hex)
            expected = bytes.fromhex(digest_hex)
            actual = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1)
            return hmac.compare_digest(actual, expected)
        except (ValueError, TypeError):
            return False
    return hmac.compare_digest(password, stored_password)


def _stream_signature(path, params, expires):
    canonical_query = urlencode(sorted(params.items()))
    message = f"{path}\n{canonical_query}\n{expires}".encode("utf-8")
    return hmac.new(API_HASH.encode("utf-8"), message, hashlib.sha256).hexdigest()


def _build_signed_stream_url(path, params, user_id, session_id):
    if path not in STREAM_AUTH_PATHS or not isinstance(params, dict):
        raise ValueError("Unsupported stream route")
    if not isinstance(session_id, str) or not session_id:
        raise ValueError("Missing web session")
    clean_params = {}
    for key, value in params.items():
        if key not in STREAM_AUTH_PATHS[path] or not isinstance(value, (str, int, float, bool)):
            raise ValueError("Invalid stream parameter")
        clean_params[key] = str(value)
    clean_params["user_id"] = str(int(user_id))
    clean_params["session_id"] = session_id
    expires = str(int(time.time()) + STREAM_LINK_TTL)
    signature = _stream_signature(path, clean_params, expires)
    query = urlencode(sorted(clean_params.items()))
    return f"{path}?{query}&expires={expires}&sig={signature}"


def _normalize_keyword_list(value):
    values = value.split(",") if isinstance(value, str) else value if isinstance(value, list) else []
    return list(dict.fromkeys(str(item).strip() for item in values if str(item).strip()))[:20]


def _normalize_task_thumb_data(value):
    if not value:
        return None
    if value == "REMOVE":
        return "REMOVE"
    if not isinstance(value, str) or len(value) > 30_000_000: # 🟢 INCREASED LIMIT
        raise ValueError("Thumbnail image is too large.")
    import base64
    import io
    from PIL import Image

    encoded = value.split(",", 1)[-1]
    try:
        raw = base64.b64decode(encoded, validate=True)
        if not raw:
            raise ValueError("Invalid thumbnail image.")
        with Image.open(io.BytesIO(raw)) as source:
            image = source.convert("RGB")
            for dimensions in ((320, 320), (256, 256), (160, 160)):
                image.thumbnail(dimensions)
                for quality in (80, 65, 50):
                    output = io.BytesIO()
                    image.save(output, format="JPEG", quality=quality, optimize=True)
                    if output.tell() <= 200_000:
                        return "data:image/jpeg;base64," + base64.b64encode(output.getvalue()).decode("ascii")
        raise ValueError("Could not compress thumbnail below 200 KB.")
    except (OSError, base64.binascii.Error) as exc:
        raise ValueError("Invalid thumbnail image.") from exc


def _get_signed_stream_user(request):
    try:
        expires = int(request.query.get("expires", "0"))
        user_id = int(request.query.get("user_id", "0"))
        session_id = request.query.get("session_id", "")
    except (TypeError, ValueError):
        return None
    now = int(time.time())
    if expires <= now or expires > now + STREAM_LINK_TTL:
        return None
    params = {key: value for key, value in request.query.items() if key not in {"expires", "sig"}}
    expected = _stream_signature(request.path, params, str(expires))
    if not hmac.compare_digest(expected, request.query.get("sig", "")):
        return None
    if not re.fullmatch(r"[a-f0-9]{64}", session_id):
        return None
    return user_id, session_id


@web.middleware
async def _web_auth_middleware(request, handler):
    if not request.path.startswith("/api/") or request.path in PUBLIC_AUTH_PATHS:
        return await handler(request)

    # 🟢 FIX: Allow internal server loopback requests (FFprobe / FFmpeg) to bypass authentication
    if request.remote in {"127.0.0.1", "::1"} or request.headers.get("X-Internal-Loopback") == "true":
        # We must still inject a dummy user_id so the downstream handlers don't crash
        request["authenticated_user_id"] = int(request.query.get("user_id", 0))
        request["web_auth_token"] = "loopback"
        request["web_session_id"] = "loopback"
        return await handler(request)

    payload = {}
    if request.content_type == "application/json" and request.can_read_body:
        try:
            payload = await request.json()
        except (ValueError, TypeError):
            payload = {}
    if not isinstance(payload, dict):
        payload = {}

    token = request.cookies.get(WEB_AUTH_COOKIE, "")
    if token:
        user_doc = await db.col.find_one({"$or": [{"web_tokens": token}, {"web_token": token}]})
        if not user_doc:
            return web.json_response({"status": "error", "message": "Invalid or expired session."}, status=401)
        token_expiries = user_doc.get("web_token_expiries", {})
        token_expiry = token_expiries.get(token) if isinstance(token_expiries, dict) else None
        if not isinstance(token_expiry, (int, float)) or token_expiry <= time.time():
            return web.json_response({"status": "error", "message": "Invalid or expired session."}, status=401)
        user_id = int(user_doc["id"])
        session_id = hashlib.sha256(token.encode("utf-8")).hexdigest()
    elif request.path in STREAM_AUTH_PATHS:
        signed_identity = _get_signed_stream_user(request)
        if signed_identity is None:
            return web.json_response({"status": "error", "message": "Invalid or expired stream link."}, status=401)
        user_id, session_id = signed_identity
        user_doc = await db.col.find_one({"id": user_id})
        if not user_doc:
            return web.json_response({"status": "error", "message": "Invalid or expired stream link."}, status=401)
        token_expiries = user_doc.get("web_token_expiries", {})
        active_session = any(
            hmac.compare_digest(hashlib.sha256(active_token.encode("utf-8")).hexdigest(), session_id)
            and isinstance(expiry, (int, float))
            and expiry > time.time()
            for active_token, expiry in token_expiries.items()
        ) if isinstance(token_expiries, dict) else False
        if not active_session:
            return web.json_response({"status": "error", "message": "Invalid or expired stream link."}, status=401)
    else:
        return web.json_response({"status": "error", "message": "Authentication required."}, status=401)

    if not await db.is_user_approved(user_id):
        return web.json_response({"status": "error", "message": "Account access is not approved."}, status=403)

    requested_user_id = payload.get("user_id", request.query.get("user_id"))
    if requested_user_id is not None:
        try:
            if int(requested_user_id) != user_id:
                return web.json_response({"status": "error", "message": "Cannot access another user's account."}, status=403)
        except (TypeError, ValueError):
            return web.json_response({"status": "error", "message": "Invalid user ID."}, status=400)

    if request.path.startswith("/api/admin/") or request.path == "/api/logs/download":
        if not await db.is_user_admin(user_id):
            return web.json_response({"status": "error", "message": "Administrator access required."}, status=403)

    request["authenticated_user_id"] = user_id
    request["web_auth_token"] = token
    request["web_session_id"] = session_id
    return await handler(request)


HTML_DASHBOARD = (BASE_DIR / "web" / "templates" / "dashboard.html").read_text(encoding="utf-8")
async def _dashboard_ui_handler(request):
    return web.Response(text=HTML_DASHBOARD, content_type='text/html', status=200)

async def _api_login_handler(request):
    try:
        data = await request.json()
        user_id = int(data.get("user_id"))
        password = data.get("password")
        if not isinstance(password, str) or not password:
            return web.json_response({"status": "error", "message": "Enter your password."}, status=400)
        
        if not await db.is_user_approved(user_id):
            return web.json_response({"status": "error", "message": "⛔ Unauthorized: You are not allowed to access this dashboard."})
            
        user = await db.col.find_one({"id": user_id})
        if not user:
            return web.json_response({"status": "error", "message": "Account not found! Please go to Telegram and send /start to the bot first."})

        stored_pwd = user.get("web_password")
        if not stored_pwd:
            return web.json_response({
                "status": "error",
                "message": "Set your dashboard password using Forgot Password so a setup token can be sent to your Telegram account.",
            }, status=400)
        if _verify_web_password(password, stored_pwd):
            web_token = secrets.token_hex(16)
            
            now = time.time()
            existing_tokens = user.get("web_tokens")
            if not isinstance(existing_tokens, list): 
                existing_tokens = [user.get("web_token")] if user.get("web_token") else []
            existing_expiries = user.get("web_token_expiries")
            if not isinstance(existing_expiries, dict):
                existing_expiries = {}
            existing_tokens = [
                token for token in existing_tokens
                if isinstance(token, str) and existing_expiries.get(token, 0) > now
            ]
            existing_tokens.append(web_token)
            if len(existing_tokens) > 5:
                existing_tokens = existing_tokens[-5:]
            token_expiries = {
                token: existing_expiries[token]
                for token in existing_tokens
                if token in existing_expiries
            }
            token_expiries[web_token] = now + WEB_SESSION_TTL
                
            update_data = {
                "web_tokens": existing_tokens, 
                "web_token": web_token,
                "web_token_expiries": token_expiries,
            }
            
            if not stored_pwd.startswith("scrypt$"):
                update_data["web_password"] = _hash_web_password(password)
                
            await db.col.update_one({"id": user_id}, {"$set": update_data})
            response = web.json_response({"status": "success"})
            forwarded_proto = request.headers.get("X-Forwarded-Proto", "").split(",", 1)[0].strip().lower()
            response.set_cookie(
                WEB_AUTH_COOKIE,
                web_token,
                httponly=True,
                secure=request.secure or forwarded_proto == "https",
                samesite="Strict",
                max_age=WEB_SESSION_TTL,
                path="/api",
            )
            return response
        else:
            return web.json_response({"status": "error", "message": "Incorrect password!"})
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)}, status=400)

async def _api_forgot_password_handler(request):
    try:
        data = await request.json()
        user_id = int(data.get("user_id"))
        now = time.monotonic()
        eligible = now - PASSWORD_RESET_REQUESTS.get(user_id, 0) >= 60
        PASSWORD_RESET_REQUESTS[user_id] = now

        user = await db.col.find_one({"id": user_id})
        if eligible and user and await db.is_user_approved(user_id):
            reset_token = secrets.token_urlsafe(32)
            await db.col.update_one(
                {"id": user_id},
                {"$set": {
                    "web_password_reset_hash": hashlib.sha256(reset_token.encode("utf-8")).hexdigest(),
                    "web_password_reset_expires": time.time() + 600,
                }},
            )
            try:
                await app.send_message(
                    chat_id=user_id,
                    text=f"Web dashboard password reset token (valid for 10 minutes): {reset_token}",
                )
            except Exception:
                await db.col.update_one(
                    {"id": user_id},
                    {"$unset": {"web_password_reset_hash": "", "web_password_reset_expires": ""}},
                )

        return web.json_response({
            "status": "success",
            "message": "If the account is eligible, password reset instructions will arrive in Telegram.",
        })
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)}, status=400)


async def _api_reset_password_handler(request):
    try:
        data = await request.json()
        user_id = int(data.get("user_id"))
        reset_token = data.get("reset_token", "")
        password = data.get("password", "")
        if not isinstance(password, str) or len(password) < 12:
            return web.json_response({"status": "error", "message": "Use a password with at least 12 characters."}, status=400)
        if not isinstance(reset_token, str) or not reset_token:
            return web.json_response({"status": "error", "message": "Invalid or expired reset token."}, status=400)

        user = await db.col.find_one({"id": user_id})
        reset_hash = hashlib.sha256(reset_token.encode("utf-8")).hexdigest()
        if (
            not user
            or not await db.is_user_approved(user_id)
            or user.get("web_password_reset_expires", 0) < time.time()
            or not hmac.compare_digest(user.get("web_password_reset_hash", ""), reset_hash)
        ):
            return web.json_response({"status": "error", "message": "Invalid or expired reset token."}, status=400)

        await db.col.update_one(
            {"id": user_id, "web_password_reset_hash": reset_hash},
            {
                "$set": {"web_password": _hash_web_password(password), "web_tokens": []},
                "$unset": {
                    "web_token": "",
                    "web_token_expiries": "",
                    "web_password_reset_hash": "",
                    "web_password_reset_expires": "",
                },
            },
        )
        return web.json_response({"status": "success", "message": "Password reset. Please log in with your new password."})
    except Exception:
        return web.json_response({"status": "error", "message": "Unable to reset password."}, status=400)


async def _api_logout_handler(request):
    user_id = request["authenticated_user_id"]
    token = request["web_auth_token"]
    await db.col.update_one({"id": user_id}, {"$pull": {"web_tokens": token}})
    await db.col.update_one({"id": user_id, "web_token": token}, {"$unset": {"web_token": ""}})
    await db.col.update_one({"id": user_id}, {"$unset": {f"web_token_expiries.{token}": ""}})
    response = web.json_response({"status": "success"})
    response.del_cookie(WEB_AUTH_COOKIE, path="/api")
    return response


async def _api_stream_link_handler(request):
    try:
        data = await request.json()
        path = data.get("path")
        params = data.get("params")
        user_id = request["authenticated_user_id"]
        if path not in STREAM_AUTH_PATHS or not isinstance(params, dict):
            return web.json_response({"status": "error", "message": "Unsupported stream request."}, status=400)
        signed_url = _build_signed_stream_url(path, params, user_id, request["web_session_id"])
        return web.json_response({"status": "success", "url": signed_url, "expires_in": STREAM_LINK_TTL})
    except (TypeError, ValueError):
        return web.json_response({"status": "error", "message": "Invalid stream request."}, status=400)
    except Exception:
        return web.json_response({"status": "error", "message": "Unable to create stream link."}, status=500)


async def _api_password_handler(request):
    try:
        data = await request.json()
        password = data.get("password")
        if not isinstance(password, str) or len(password) < 12:
            return web.json_response({"status": "error", "message": "Use a password with at least 12 characters."}, status=400)
        user_id = request["authenticated_user_id"]
        token = request["web_auth_token"]
        await db.col.update_one(
            {"id": user_id},
            {"$set": {
                "web_password": _hash_web_password(password),
                "web_tokens": [token],
                "web_token": token,
                "web_token_expiries": {token: time.time() + WEB_SESSION_TTL},
            }},
        )
        return web.json_response({"status": "success"})
    except Exception:
        return web.json_response({"status": "error"}, status=400)

async def _api_stats_handler(request):
    user_id = request["authenticated_user_id"]

    uptime_seconds = int(time.time() - BOT_START_TIME)
    days, rem = divmod(uptime_seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)
    uptime_str = f"{days}d, {hours:02d}h: {minutes:02d}m" if days > 0 else f"{hours:02d}h: {minutes:02d}m"
    
    # User-specific tasks
    user_tasks = ACTIVE_PROCESSES.get(user_id, {})
    task_details = []
    for t_id, info in user_tasks.items():
        tot = info.get("total", 0)
        curr = info.get("current", 0)
        
        prog_down = PROGRESS.get(f"{t_id}:down")
        prog_up = PROGRESS.get(f"{t_id}:up")
        
        phase = "Processing"
        speed = 0
        eta = 0
        file_current = 0
        file_total = 0
        percent = 0.0

        if prog_up and prog_up["current"] > 0:
            if prog_up["total"] > 0 and prog_up["current"] >= prog_up["total"]:
                phase = "Finalizing on Telegram..."
                speed = 0
                eta = 0
                file_current = prog_up["total"]
                file_total = prog_up["total"]
                percent = 100.0
            else:
                phase = "Uploading"
                speed = prog_up["speed"]
                eta = prog_up["eta"]
                file_current = prog_up["current"]
                file_total = prog_up["total"]
                percent = prog_up.get("percent", 0.0)
        elif prog_down and prog_down["current"] > 0:
            if prog_down["total"] > 0 and prog_down["current"] >= prog_down["total"]:
                phase = "Finalizing Download..."
                speed = 0
                eta = 0
                file_current = prog_down["total"]
                file_total = prog_down["total"]
                percent = 100.0
            else:
                phase = "Downloading"
                speed = prog_down["speed"]
                eta = prog_down["eta"]
                file_current = prog_down["current"]
                file_total = prog_down["total"]
                percent = prog_down.get("percent", 0.0)
        else:
            if tot > 0:
                percent = (curr / tot * 100)

        src_name = info.get("source_title")
        if not src_name or src_name == "Unknown Source":
            src_name = info.get("item", "Task")
            
        task_details.append({
            "id": t_id,
            "name": src_name,
            "dest": info.get("dest_title_name", "DM"),
            "batch_current": curr,
            "batch_total": tot,
            "phase": phase,
            "speed": speed,
            "eta": eta,
            "file_current": file_current,
            "file_total": file_total,
            "percent": percent,
            "success": info.get("success", 0),
            "skipped": info.get("skipped", 0),
            "failed": info.get("failed", 0),
            "current_file": info.get("current_file", ""),
            "fetcher": info.get("fetcher", "🤖 Unknown"),
            "uploader": info.get("uploader", "🤖 Unknown")
        })

    # User-specific watchers
    watcher_cursor = db.db.watchers.find({"user_id": user_id})
    watcher_details = []
    async for w in watcher_cursor:
        stats = w.get("stats", {})
        watcher_details.append({
            "id": str(w["_id"]),
            "source": w.get("source_title", "Source"),
            "dest": w.get("dest_title", "Destination"),
            "detected": stats.get("detected", 0),
            "success": stats.get("success", 0),
            "skipped": stats.get("skipped", 0),
            "failed": stats.get("failed", 0),
            "fetcher": w.get("fetcher", "⏳ Waiting..."),
            "uploader": w.get("uploader", "⏳ Waiting...")
        })

    total_watchers = await db.db.watchers.count_documents({"user_id": user_id})
    
    # Check if user session exists in DB
    user_doc = await db.col.find_one({"id": user_id})
    tg_session_active = bool(user_doc and user_doc.get("session"))
    user_name = user_doc.get("name", "User") if user_doc else "User"
    is_admin = await db.is_user_admin(user_id)

    return web.json_response({
        "uptime": uptime_str,
        "user_name": user_name,
        "is_admin": is_admin,
        "ram": psutil.virtual_memory().percent,
        "cpu": psutil.cpu_percent(),
        "active_tasks": len(user_tasks),
        "active_watchers": total_watchers,
        "tg_session_active": tg_session_active,
        "tasks": task_details,
        "watchers": watcher_details
    })

async def _api_add_task(request):
    try:
        data = await request.json()
        user_id = request["authenticated_user_id"]
        link = data.get("link")
        dest_str = data.get("dest", "")
        delay = max(3, min(int(data.get("delay", 3)), 3600))
        allowed_types = data.get("filters", ["Video", "Document"])
        if not isinstance(allowed_types, list):
            allowed_types = ["Video", "Document"]
        allowed_types = [t for t in allowed_types if t in ALL_MSG_TYPES]
        include_keywords = _normalize_keyword_list(data.get("include_keywords"))
        exclude_keywords = _normalize_keyword_list(data.get("exclude_keywords"))
        cleanup_keywords = _normalize_keyword_list(data.get("cleanup_keywords")) # 🟢 NEW
        try:
            thumb_b64 = _normalize_task_thumb_data(data.get("thumb_b64"))
        except ValueError as exc:
            return web.json_response({"status": "error", "message": str(exc)}, status=400)

        if not link: return web.json_response({"status": "error", "message": "No link provided"})

        dest_chat_id = user_id
        dest_thread_id = None
        dest_title = "Saved Messages"
        
        if dest_str:
            dest_chat_id, dest_thread_id = _parse_chat_target(dest_str)
            uclient = USER_CLIENTS.get(user_id, app)
            try:
                d_chat = await uclient.get_chat(dest_chat_id)
                dest_title = d_chat.title or d_chat.first_name or str(dest_chat_id)
                if dest_thread_id: 
                    dest_title += await get_topic_title(uclient, dest_chat_id, dest_thread_id)
            except:
                dest_title = str(dest_chat_id)

        # 🟢 NEW: Check Worker Bots access and warn via PM if missing!
        worker_bots = USER_TASK_BOTS.get(user_id, [])
        is_dm = str(dest_chat_id).lstrip("-").isdigit() and not str(dest_chat_id).startswith("-100") and int(dest_chat_id) > 0
        if worker_bots and not is_dm:
            has_worker_access = False
            for wb in worker_bots:
                try:
                    if not getattr(wb, "is_connected", False): await wb.connect()
                    wb_member = await wb.get_chat_member(dest_chat_id, "me")
                    if wb_member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
                        has_worker_access = True
                        break
                except Exception: pass
            if not has_worker_access:
                try: await app.send_message(user_id, f"⚠️ **Worker Bot Warning:** You just started a Batch Task to `{dest_title}` via the Web UI, but your Worker Bots are not Admins there!\n\nI will fallback to your User Session. Add your worker bots as Admins for maximum speed.")
                except Exception: pass

        if not await check_disk_space():
            return web.json_response({"status": "error", "message": "Server disk is almost full (<500MB). Please wait."})

        if user_id not in ADMINS and batch_temp.ACTIVE_TASKS[user_id] >= MAX_CONCURRENT_TASKS_PER_USER:
            return web.json_response({"status": "error", "message": f"Task limit reached ({MAX_CONCURRENT_TASKS_PER_USER} max). Wait for existing tasks to finish."})

        is_restricted, _ = await check_link_restriction(user_id, link)
        if is_restricted is None: is_restricted = False

        task_uuid = uuid.uuid4().hex
        batch_temp.ACTIVE_TASKS[user_id] += 1
        batch_temp.IS_BATCH[user_id] = False

        # 🟢 Pre-resolve In & Out clients
        needs_reupload = bool(is_restricted or thumb_b64 or cleanup_keywords)
        client_in, client_out = await resolve_task_clients(user_id, link, dest_chat_id, needs_reupload=needs_reupload)

        def _get_lbl(c):
            if not c: return "Unknown"
            nm = getattr(c, "name", "Unknown")
            if "User_" in nm: return "👤 User Session"
            if "task_bot_" in nm: return f"🤖 {nm}"
            if nm == "RestrictedBot": return "🤖 Main Bot"
            return f"🤖 {nm}"

        if user_id not in ACTIVE_PROCESSES: ACTIVE_PROCESSES[user_id] = {}
        ACTIVE_PROCESSES[user_id][task_uuid] = {
            "user": f"WebUI({user_id})",
            "dest_title_name": dest_title,
            "item": link,
            "started": time.time(),
            "total": 0,
            "current": 0,
            "include_keywords": include_keywords,
            "exclude_keywords": exclude_keywords,
            "thumb_b64": thumb_b64,
            "fetcher": _get_lbl(client_in),   # 🟢 Displays In client immediately
            "uploader": _get_lbl(client_out), # 🟢 Displays Out client immediately
        }

        task_coro = asyncio.create_task(
            process_links_logic(
                client=app,
                message=None,
                text=link,
                dest_chat_id=dest_chat_id,
                dest_thread_id=dest_thread_id,
                dest_title=dest_title,
                delay=delay,
                acc_user_id=user_id,
                task_uuid=task_uuid,
                is_restricted=is_restricted,
                allowed_types=allowed_types,
                include_keywords=include_keywords,
                exclude_keywords=exclude_keywords,
                cleanup_keywords=cleanup_keywords, # 🟢 ADDED THIS
                thumb_b64=thumb_b64,
            )
        )
        ACTIVE_TASK_OBJECTS[task_uuid] = task_coro # 🟢 Save task handle for hard cancel
        return web.json_response({"status": "success"})
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)}, status=500)

async def _api_cancel_task(request):
    try:
        data = await request.json()
        task_id = data.get("task_id")
        user_id = request["authenticated_user_id"]
        if task_id and task_id in ACTIVE_PROCESSES.get(user_id, {}):
            CANCEL_FLAGS[task_id] = True
            task_obj = ACTIVE_TASK_OBJECTS.pop(task_id, None)
            if task_obj and not task_obj.done():
                task_obj.cancel() # 🟢 Kill socket/task immediately
            cleanup_task_memory(user_id, task_id) # 🟢 Instant memory cleanup
            try: await db.remove_active_task(task_id)
            except: pass
            return web.json_response({"status": "success"})
    except: pass
    return web.json_response({"status": "error"}, status=400)

async def _api_add_watcher(request):
    try:
        data = await request.json()
        user_id = request["authenticated_user_id"]
        link = data.get("link")
        dest_str = data.get("dest", "")
        delay = max(3, min(int(data.get("delay", 3)), 3600))
        allowed_types = data.get("filters", ["Video", "Document"])
        if not isinstance(allowed_types, list):
            allowed_types = ["Video", "Document"]
        allowed_types = [t for t in allowed_types if t in ALL_MSG_TYPES]
        include_keywords = _normalize_keyword_list(data.get("include_keywords"))
        exclude_keywords = _normalize_keyword_list(data.get("exclude_keywords"))
        cleanup_keywords = _normalize_keyword_list(data.get("cleanup_keywords")) # 🟢 NEW
        try:
            thumb_b64 = _normalize_task_thumb_data(data.get("thumb_b64"))
        except ValueError as exc:
            return web.json_response({"status": "error", "message": str(exc)}, status=400)

        dest_chat_id = user_id
        dest_thread_id = None
        if dest_str:
            dest_chat_id, dest_thread_id = _parse_chat_target(dest_str)

        is_restricted, _ = await check_link_restriction(user_id, link)
        if is_restricted is None: is_restricted = False

        parsed = _parse_source_link(link)
        source_thread = parsed.get("topic_id")
        
        user_client = USER_CLIENTS.get(user_id, app)
        try:
            if parsed["kind"] == "public":
                try: await user_client.resolve_peer(parsed["join_target"])
                except Exception: pass
                chat = await user_client.get_chat(parsed["join_target"])
            else:
                try: await user_client.resolve_peer(parsed["chat_id"])
                except Exception: pass
                chat = await user_client.get_chat(parsed["chat_id"])
            source_id = chat.id
            # 🟢 FIX: Extract first_name so Bot DMs dynamically show the actual Bot name instead of raw IDs
            source_title = chat.title or getattr(chat, "first_name", None) or str(source_id)
            if parsed.get("topic_id"): 
                source_title += await get_topic_title(user_client, source_id, parsed["topic_id"])
        except Exception:
            source_id = parsed.get("chat_id")
            source_title = "Watched Source"
            
        dest_title = "Saved Messages" if dest_chat_id == user_id else str(dest_chat_id)
        if dest_chat_id != user_id:
            try:
                try: await user_client.resolve_peer(dest_chat_id)
                except Exception: pass
                d_chat = await user_client.get_chat(dest_chat_id)
                dest_title = d_chat.title or d_chat.first_name or str(dest_chat_id)
                if dest_thread_id: 
                    dest_title += await get_topic_title(user_client, dest_chat_id, dest_thread_id)
            except: pass

        # 🟢 NEW: Check Worker Bots access and warn via PM if missing!
        worker_bots = USER_TASK_BOTS.get(user_id, [])
        is_dm = str(dest_chat_id).lstrip("-").isdigit() and not str(dest_chat_id).startswith("-100") and int(dest_chat_id) > 0
        if worker_bots and not is_dm:
            has_worker_access = False
            for wb in worker_bots:
                try:
                    if not getattr(wb, "is_connected", False): await wb.connect()
                    wb_member = await wb.get_chat_member(dest_chat_id, "me")
                    if wb_member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
                        has_worker_access = True
                        break
                except Exception: pass
            if not has_worker_access:
                try: await app.send_message(user_id, f"⚠️ **Worker Bot Warning:** You just started a Live Watcher to `{dest_title}` via the Web UI, but your Worker Bots are not Admins there!\n\nI will fallback to your User Session. Add your worker bots as Admins for maximum forwarding speed.")
                except Exception: pass

        if user_id not in USER_CLIENTS:
            user_session = await db.get_session(user_id)
            if user_session:
                u_api = await db.get_api_id(user_id) or API_ID
                u_hash = await db.get_api_hash(user_id) or API_HASH
                # 🟢 FIX: Increased workers to 100
                new_client = Client(f"User_{user_id}", session_string=user_session, api_id=u_api, api_hash=u_hash, workers=100, ipv6=False)
                new_client.add_handler(MessageHandler(user_watcher_handler, is_watched_chat))
                await new_client.start()
                USER_CLIENTS[user_id] = new_client

        last_msg_id = 0
        try:
            async for m in USER_CLIENTS.get(user_id, app).get_chat_history(source_id, limit=1):
                last_msg_id = m.id
        except: pass

        await db.add_watcher(
            user_id=user_id,
            source_id=source_id,
            dest_id=dest_chat_id,
            source_thread=source_thread,
            dest_thread=dest_thread_id,
            delay=delay,
            is_restricted=is_restricted,
            source_title=source_title,
            dest_title=dest_title,
            allowed_types=allowed_types,
            include_keywords=include_keywords,
            exclude_keywords=exclude_keywords,
            cleanup_keywords=cleanup_keywords, # 🟢 ADDED THIS
            thumb_b64=thumb_b64,
            last_msg_id=last_msg_id
        )
        GLOBAL_WATCHER_SOURCES.add(source_id) # 🟢 UPDATE CACHE
        return web.json_response({"status": "success"})
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)}, status=500)

async def _api_cancel_watcher(request):
    try:
        data = await request.json()
        watcher_id = data.get("watcher_id")
        user_id = request["authenticated_user_id"]
        if watcher_id:
            await db.db.watchers.delete_one({"_id": ObjectId(watcher_id), "user_id": user_id})
            return web.json_response({"status": "success"})
    except: pass
    return web.json_response({"status": "error"}, status=400)

def _read_logs_sync():
    """Reads logs safely in a background thread so the server doesn't freeze."""
    if not os.path.exists("bot.log"): return "Log file not created yet."
    with open("bot.log", "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    return "".join(lines[-150:])

async def _api_logs_handler(request):
    uid = request["authenticated_user_id"]
        
    if not await db.is_user_admin(uid):
        return web.json_response({"logs": "⚠️ ACCESS DENIED: You must be a Bot Admin to view server logs."})
        
    try:
        logs = await asyncio.to_thread(_read_logs_sync)
        return web.json_response({"logs": logs})
    except Exception as e:
        return web.json_response({"logs": f"Error reading logs: {e}"})

async def _api_download_log_handler(request):
    uid = request["authenticated_user_id"]
    if not await db.is_user_admin(uid):
        return web.Response(text="ACCESS DENIED: Admins Only", status=403)
        
    try:
        if os.path.exists("bot.log"):
            return web.FileResponse("bot.log", headers={"Content-Disposition": "attachment; filename=bot.log"})
        return web.Response(text="Log file not found.", status=404)
    except Exception:
        return web.Response(text="Error downloading logs.", status=500)

import base64
import uuid
from urllib.parse import quote
from pyrogram import raw

TG_QR_LOGIN_SESSIONS = {}
WEB_AUTH_CACHE = {}

# ==============================================================================
# --- FIXED: TELEGRAM QR CODE LOGIN ENGINE (NO SELF-INVALIDATION & DC MIGRATION) ---
# ==============================================================================
from pyrogram.handlers import RawUpdateHandler

async def _api_tg_qr_start(request):
    try:
        user_id = request["authenticated_user_id"]
        qr_key = uuid.uuid4().hex
        
        temp_client = Client(f"qr_{qr_key[:8]}", api_id=API_ID, api_hash=API_HASH, in_memory=True, ipv6=False)
        await temp_client.connect()
        
        # 🟢 Event flag: set ONLY when Telegram pushes that the phone scanned the code
        scanned_event = asyncio.Event()

        async def _on_raw_update(client, update, users, chats):
            if isinstance(update, raw.types.UpdateLoginToken):
                scanned_event.set()

        temp_client.add_handler(RawUpdateHandler(_on_raw_update))
        await temp_client.dispatcher.start()
        
        res = await temp_client.invoke(raw.functions.auth.ExportLoginToken(api_id=API_ID, api_hash=API_HASH, except_ids=[]))
        
        if isinstance(res, raw.types.auth.LoginToken):
            b64_tok = base64.urlsafe_b64encode(res.token).decode("utf-8").rstrip("=")
            tg_qr_url = f"tg://login?token={b64_tok}"
            
            TG_QR_LOGIN_SESSIONS[qr_key] = {
                "user_id": user_id, 
                "client": temp_client, 
                "expires": res.expires, 
                "scanned_event": scanned_event
            }
            
            return web.json_response({
                "status": "success", 
                "qr_key": qr_key, 
                "qr_url": tg_qr_url,
                "expires_in": max(15, int(res.expires - time.time()))
            })
        else:
            await temp_client.disconnect()
            return web.json_response({"status": "error", "message": "Failed to generate QR token"}, status=500)
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)}, status=500)

async def _api_tg_qr_check(request):
    qr_key = request.query.get("qr_key", "").strip()
    session_data = TG_QR_LOGIN_SESSIONS.get(qr_key)
    if not session_data:
        return web.json_response({"status": "expired", "message": "Session expired"})
        
    temp_client = session_data["client"]
    user_id = session_data["user_id"]
    try:
        res = await temp_client.invoke(raw.functions.auth.ExportLoginToken(api_id=API_ID, api_hash=API_HASH, except_ids=[]))
        
        # 🟢 Case 1: Account is on DC 2 without 2FA
        if isinstance(res, raw.types.auth.LoginTokenSuccess):
            session_str = await temp_client.export_session_string()
            await db.set_session(user_id, session_str)
            await db.set_api_id(user_id, API_ID)
            await db.set_api_hash(user_id, API_HASH)
            await temp_client.disconnect()
            TG_QR_LOGIN_SESSIONS.pop(qr_key, None)
            return web.json_response({"status": "authorized", "message": "Telegram session connected successfully!"})
            
        # 🟢 Case 2: Account is on DC 5 (India) / DC 4 / DC 1 -> Auto-Migrate!
        elif isinstance(res, raw.types.auth.LoginTokenMigrateTo):
            target_dc = res.dc_id
            transfer_token = res.token
            await temp_client.disconnect()
            
            # Create client directly targeted at your datacenter
            migrated_client = Client(f"qr_dc{target_dc}_{qr_key[:8]}", api_id=API_ID, api_hash=API_HASH, in_memory=True, ipv6=False)
            if callable(getattr(migrated_client.storage, "dc_id", None)):
                await migrated_client.storage.dc_id(target_dc)
            else:
                migrated_client.storage.dc_id = target_dc
                
            await migrated_client.connect()
            session_data["client"] = migrated_client  # Update reference for 2FA password verification
            
            try:
                import_res = await migrated_client.invoke(raw.functions.auth.ImportLoginToken(token=transfer_token))
                if isinstance(import_res, raw.types.auth.LoginTokenSuccess):
                    session_str = await migrated_client.export_session_string()
                    await db.set_session(user_id, session_str)
                    await db.set_api_id(user_id, API_ID)
                    await db.set_api_hash(user_id, API_HASH)
                    await migrated_client.disconnect()
                    TG_QR_LOGIN_SESSIONS.pop(qr_key, None)
                    return web.json_response({"status": "authorized", "message": "Telegram session connected successfully!"})
            except Exception as import_err:
                if "session_password_needed" in str(import_err).lower():
                    return web.json_response({"status": "2fa_required", "message": "Two-Step Verification password required."})
                raise import_err

        return web.json_response({"status": "pending"})
    except Exception as e:
        if "session_password_needed" in str(e).lower():
            return web.json_response({"status": "2fa_required", "message": "Two-Step Verification password required."})
        return web.json_response({"status": "pending"})

async def _api_tg_qr_verify_2fa(request):
    """Verifies the Telegram Cloud Password for a QR login session."""
    data = await request.json()
    qr_key = data.get("qr_key", "").strip()
    pwd = data.get("password", "")
    
    session_data = TG_QR_LOGIN_SESSIONS.get(qr_key)
    if not session_data:
        return web.json_response({"status": "error", "message": "QR login session expired. Please generate a new QR code."})
        
    temp_client = session_data["client"]
    user_id = session_data["user_id"]
    
    try:
        await temp_client.check_password(pwd)
        
        session_str = await temp_client.export_session_string()
        await temp_client.disconnect()
        TG_QR_LOGIN_SESSIONS.pop(qr_key, None)
        
        await db.set_session(user_id, session_str)
        await db.set_api_id(user_id, API_ID)
        await db.set_api_hash(user_id, API_HASH)
        return web.json_response({"status": "success", "message": "Logged in successfully!"})
    except (PasswordHashInvalid, SessionPasswordNeeded):
        return web.json_response({"status": "error", "message": "Incorrect 2FA password! Please try again."})
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)})

async def _api_tg_send_code(request):
    data = await request.json()
    uid = int(data.get("user_id"))
    phone = data.get("phone")
    
    client = Client(f"web_auth_{uid}_{uuid.uuid4().hex}", in_memory=True, api_id=API_ID, api_hash=API_HASH)
    await client.connect()
    try:
        code = await client.send_code(phone)
        WEB_AUTH_CACHE[uid] = {"client": client, "phone": phone, "hash": code.phone_code_hash}
        return web.json_response({"status": "success"})
    except Exception as e:
        await client.disconnect()
        return web.json_response({"status": "error", "message": str(e)})

async def _api_tg_verify_code(request):
    data = await request.json()
    uid = int(data.get("user_id"))
    code = data.get("code")
    
    cache = WEB_AUTH_CACHE.get(uid)
    if not cache: return web.json_response({"status": "error", "message": "Session expired. Try again."})
    
    client = cache["client"]
    try:
        await client.sign_in(cache["phone"], cache["hash"], code)
        
        # 🟢 ENFORCE ID MATCH: Prevent cross-account chat leaks!
        me = await client.get_me()
        if me.id != uid:
            await client.disconnect()
            del WEB_AUTH_CACHE[uid]
            return web.json_response({"status": "error", "message": f"⚠️ ID Mismatch! You logged into the Web UI as {uid}, but this phone number belongs to {me.id}. Please use your own Telegram account."})
            
        session_str = await client.export_session_string()
        await client.disconnect()
        del WEB_AUTH_CACHE[uid]
        
        await db.set_session(uid, session_str)
        await db.set_api_id(uid, API_ID)
        await db.set_api_hash(uid, API_HASH)
        return web.json_response({"status": "success"})
        
    except SessionPasswordNeeded:
        return web.json_response({"status": "2fa_required"})
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)})

async def _api_tg_verify_2fa(request):
    data = await request.json()
    uid = int(data.get("user_id"))
    pwd = data.get("password")
    
    cache = WEB_AUTH_CACHE.get(uid)
    if not cache: return web.json_response({"status": "error", "message": "Session expired."})
    
    client = cache["client"]
    try:
        await client.check_password(pwd)
        
        # 🟢 ENFORCE ID MATCH: Prevent cross-account chat leaks!
        me = await client.get_me()
        if me.id != uid:
            await client.disconnect()
            del WEB_AUTH_CACHE[uid]
            return web.json_response({"status": "error", "message": f"⚠️ ID Mismatch! You logged into the Web UI as {uid}, but this phone number belongs to {me.id}. Please use your own Telegram account."})
            
        session_str = await client.export_session_string()
        await client.disconnect()
        del WEB_AUTH_CACHE[uid]
        
        await db.set_session(uid, session_str)
        await db.set_api_id(uid, API_ID)
        await db.set_api_hash(uid, API_HASH)
        return web.json_response({"status": "success"})
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)})

async def _api_tg_logout(request):
    data = await request.json()
    uid = int(data.get("user_id", 0))
    
    uclient = USER_CLIENTS.pop(uid, None)
    if uclient:
        try: await uclient.log_out()
        except: pass
        try: await uclient.stop()
        except: pass
        
    await db.set_session(uid, None)
    await db.set_api_id(uid, None)
    await db.set_api_hash(uid, None)
    
    user_tasks = list(ACTIVE_PROCESSES.get(uid, {}).keys())
    for tid in user_tasks: CANCEL_FLAGS[tid] = True
    batch_temp.IS_BATCH[uid] = True
    try: await db.db.active_tasks.delete_many({"user_id": uid})
    except: pass
    
    return web.json_response({"status": "success"})

async def _api_chats_handler(request):
    uid = request["authenticated_user_id"]
        
    session_str = await db.get_session(uid)
    
    if not session_str:
        return web.json_response({"status": "error", "message": "Not connected to Telegram. Please login."})

    uclient = USER_CLIENTS.get(uid)
    
    # 🟢 DYNAMIC WAKE-UP: Keep the main user session alive so we don't lose Access Hashes!
    if not uclient or not uclient.is_connected:
        try:
            api_id = await db.get_api_id(uid) or API_ID
            api_hash = await db.get_api_hash(uid) or API_HASH
            uclient = Client(f"User_{uid}", session_string=session_str, api_id=api_id, api_hash=api_hash, workers=100, ipv6=False)
            uclient.add_handler(MessageHandler(user_watcher_handler, is_watched_chat))
            await uclient.start()
            USER_CLIENTS[uid] = uclient
        except Exception as e:
            return web.json_response({"status": "error", "message": f"Session invalid: {e}"})

    dialog_collection = []

    try:
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
                        category_label = "Unknown"
                        is_forum = False
                        
                        if chat_id > 0:
                            u = resolved_users.get(chat_id)
                            if u:
                                title = getattr(u, "first_name", None)
                                if not title:
                                    title = "Unknown User"
                                if getattr(u, "last_name", None):
                                    title += f" {u.last_name}"
                                category_label = "🤖 Bot" if getattr(u, "bot", False) else "👤 User"
                        else:
                            c = resolved_chats.get(abs(chat_id)) or resolved_chats.get(getattr(peer, "channel_id", 0)) or resolved_chats.get(getattr(peer, "chat_id", 0))
                            if c:
                                title = getattr(c, "title", None)
                                if not title:
                                    title = "Unknown Group"
                                category_label = "📢 Channel" if getattr(c, "broadcast", False) else "👥 Group"
                                is_forum = getattr(c, "forum", False)

                        dialog_collection.append({
                            "id": str(chat_id), 
                            "name": f"[{category_label}] {title}", 
                            "is_forum": is_forum
                        })

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
                    
                    # 🟢 FIX: Pace the pagination requests to prevent FloodWaits
                    await asyncio.sleep(1.5)

                except FloodWait as e:
                    await asyncio.sleep(e.value + 1)
                except Exception as e:
                    logger.warning(f"Raw dialog pagination error: {e}")
                    break

        async def populate_web_dialogs():
            await execute_raw_pagination(0) # Standard Chats
            await execute_raw_pagination(1) # Archived Chats

        try:
            await asyncio.wait_for(populate_web_dialogs(), timeout=300.0)
        except asyncio.TimeoutError:
            logger.warning("Web dialog fetch reached the 300s timeout ceiling. Returning the partial payload.")
            
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)})

    # Deduplicate arrays safely before returning to web UI
    sanitized_collection = {c['id']: c for c in dialog_collection}.values()
    return web.json_response({"status": "success", "chats": list(sanitized_collection)})

async def _api_speedtest_handler(request):
    uid = request["authenticated_user_id"]
    
    session_str = await db.get_session(uid)
    if not session_str and uid not in ADMINS:
        return web.json_response({"status": "error", "message": "Unauthorized"})

    def run_speedtest_sync():
        try:
            st = speedtest.Speedtest(secure=True)
            st.get_best_server()
            st.download()
            st.upload()
            try:
                st.results.share()
            except Exception:
                pass
            return st.results.dict(), None
        except Exception as e:
            return None, str(e)

    result, error = await asyncio.to_thread(run_speedtest_sync)
    if error or not result:
        return web.json_response({"status": "error", "message": error or "Speedtest failed"})

    dl_mbps = result['download'] / 1_000_000
    ul_mbps = result['upload'] / 1_000_000
    
    return web.json_response({
        "status": "success",
        "download": f"{dl_mbps:.2f} Mbps",
        "upload": f"{ul_mbps:.2f} Mbps",
        "ping": f"{result['ping']} ms",
        "server": f"{result['server']['name']} ({result['server']['country']})",
        "sponsor": result['server']['sponsor'],
        "share_image": result.get("share", "")
    })

def _get_sos_sync():
    """Fetches system OS and IO stats safely in a background thread."""
    try:
        with open("/etc/os-release") as f:
            os_info = dict(line.strip().split("=", 1) for line in f if "=" in line)
        os_name = os_info.get("PRETTY_NAME", f'"{platform.system()} {platform.release()}"').strip('"')
    except Exception:
        os_name = f"{platform.system()} {platform.release()}"
    return os_name, psutil.virtual_memory(), psutil.disk_usage('/'), psutil.net_io_counters()

async def _api_sos_handler(request):
    uid = request["authenticated_user_id"]
    if not await db.is_user_admin(uid):
        return web.json_response({"status": "error", "message": "Unauthorized"})

    os_name, mem, disk, net = await asyncio.to_thread(_get_sos_sync)
    bytes_recv_total = net.bytes_recv
    bytes_sent_total = net.bytes_sent
    bytes_combined = bytes_recv_total + bytes_sent_total

    worker_bots_count = len(USER_TASK_BOTS.get(uid, [])) + len(USER_STREAM_BOTS.get(uid, []))

    return web.json_response({
        "status": "success",
        "cpu_cores": psutil.cpu_count(logical=True),
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "ram_used_gb": round((mem.total - mem.available) / (1024**3), 2),
        "ram_total_gb": round(mem.total / (1024**3), 2),
        "ram_percent": mem.percent,
        "disk_used_gb": round(disk.used / (1024**3), 2),
        "disk_total_gb": round(disk.total / (1024**3), 2),
        "disk_percent": disk.percent,
        "disk_free_gb": round(disk.free / (1024**3), 2),
        "bandwidth": {
            "total_bytes": bytes_combined,
            "recv_bytes": bytes_recv_total,
            "sent_bytes": bytes_sent_total,
            "active_streams": len(GLOBAL_NETWORK_STATS.get("active", {}))
        },
        "workers_online": worker_bots_count
    })

PWA_MANIFEST = {
    "name": "Destiny TG Forwarder",
    "short_name": "TG Portal",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#000000",
    "theme_color": "#000000",
    "orientation": "portrait-primary",
    "icons": [
        {
            "src": "https://cdn-icons-png.flaticon.com/512/2111/2111646.png",
            "sizes": "192x192",
            "type": "image/png"
        },
        {
            "src": "https://cdn-icons-png.flaticon.com/512/2111/2111646.png",
            "sizes": "512x512",
            "type": "image/png"
        }
    ]
}

async def _manifest_handler(request):
    return web.json_response(PWA_MANIFEST)

async def _sw_handler(request):
    sw_code = "self.addEventListener('fetch', function(e) {});"
    return web.Response(text=sw_code, content_type='application/javascript')

async def _api_topics_handler(request):
    uid = int(request.query.get("user_id", 0))
    chat_id = request.query.get("chat_id", "")
    try: chat_id = int(chat_id)
    except: pass
    
    session_str = await db.get_session(uid)
    if not session_str:
        return web.json_response({"status": "error", "message": "Not connected to Telegram."})

    uclient = USER_CLIENTS.get(uid)

    # 🟢 DYNAMIC WAKE-UP
    if not uclient or not uclient.is_connected:
        try:
            api_id = await db.get_api_id(uid) or API_ID
            api_hash = await db.get_api_hash(uid) or API_HASH
            uclient = Client(f"User_{uid}", session_string=session_str, api_id=api_id, api_hash=api_hash, workers=100, ipv6=False)
            uclient.add_handler(MessageHandler(user_watcher_handler, is_watched_chat))
            await uclient.start()
            USER_CLIENTS[uid] = uclient
        except Exception as e:
            return web.json_response({"status": "error", "message": f"Session invalid: {e}"})
    
    topics = []
    try:
        async def fetch_tg_topics():
            try:
                count = 0
                # 🟢 SPEED FIX: Lowered limit to 250 and batched the sleeps!
                async for topic in uclient.get_forum_topics(chat_id, limit=250):
                    topics.append({"id": topic.id, "title": topic.title})
                    count += 1
                    # 🟢 CRITICAL: Yield only every 25 topics to eliminate artificial lag!
                    if count % 25 == 0:
                        await asyncio.sleep(0.01)
            except Exception as e:
                # Graceful handling of Pyrogram pagination bug
                if "'NoneType'" not in str(e):
                    logger.warning(f"Topic pagination interrupted: {e}")
            
        try:
            await asyncio.wait_for(fetch_tg_topics(), timeout=25.0)
        except asyncio.TimeoutError:
            logger.warning(f"Topics endpoint timed out. Returning {len(topics)} topics found so far.")
        except Exception as e:
            logger.warning(f"Topics endpoint exception: {repr(e)}")
                
    except Exception as e:
        logger.warning(f"Topics endpoint error: {repr(e)}")

    return web.json_response({"status": "success", "topics": topics})

# 🟢 NEW: Deep Chat Details & MetaData Fetcher
import traceback

async def _api_chat_details_handler(request):
    uid = request["authenticated_user_id"]
    raw_chat_string = request.query.get("chat_id", "").strip()
    
    if not raw_chat_string:
        return web.json_response({"status": "error", "message": "Missing required chat_id parameter."})
        
    try: 
        chat_id = int(raw_chat_string)
    except ValueError: 
        chat_id = raw_chat_string if raw_chat_string.startswith("@") else f"@{raw_chat_string}"

    session_str = await db.get_session(uid)
    if not session_str:
        return web.json_response({"status": "error", "message": "Not logged in."})

    uclient = USER_CLIENTS.get(uid)
    
    # Wake up routine to prevent locks
    if not uclient or not uclient.is_connected:
        try:
            api_id = await db.get_api_id(uid) or API_ID
            api_hash = await db.get_api_hash(uid) or API_HASH
            uclient = Client(f"User_{uid}", session_string=session_str, api_id=api_id, api_hash=api_hash, workers=100, ipv6=False)
            uclient.add_handler(MessageHandler(user_watcher_handler, is_watched_chat))
            await uclient.start()
            USER_CLIENTS[uid] = uclient
        except Exception as e:
            logger.error(f"[CHAT DETAILS] Client connection failed: {e}")
            return web.json_response({"status": "error", "message": f"Session invalid: {e}"})

    try:
        # 🟢 FIX 1: Safely resolve ALL chat types (Users, Bots, Channels, Groups)
        try:
            chat = await asyncio.wait_for(uclient.get_chat(chat_id), timeout=12.0)
        except PeerIdInvalid:
            try:
                resolved_peer = await asyncio.wait_for(uclient.resolve_peer(chat_id), timeout=8.0)
                chat = await asyncio.wait_for(uclient.get_chat(resolved_peer), timeout=12.0)
            except Exception as inner_e:
                raise Exception(f"Fatal resolution failure. ({inner_e})")
        
        is_forum = getattr(chat, "is_forum", False)
        is_supergroup = getattr(chat, "type", None) == enums.ChatType.SUPERGROUP
        topics = []
        
        # 🟢 SPEED FIX 1: Wrap message count in its own async function
        async def fetch_msg_count():
            try:
                return await asyncio.wait_for(uclient.get_chat_history_count(chat_id), timeout=3.0)
            except Exception:
                return "Unknown"
                
        # 🟢 SPEED FIX 2: Optimize the Topic Fetcher
        async def fetch_forum_topology():
            if not (is_forum and is_supergroup):
                return
            try:
                count = 0
                # Lowered limit to 250 for instant UI preview
                async for t in uclient.get_forum_topics(chat_id, limit=250):
                    top_msg_data = getattr(t, "top_message", "?")
                    topics.append({
                        "id": t.id,
                        "title": t.title,
                        "top_msg": str(getattr(top_msg_data, "id", top_msg_data))
                    })
                    count += 1
                    # 🟢 CRITICAL: Yield every 25 topics so the 250-item loop doesn't freeze the server
                    if count % 25 == 0:
                        await asyncio.sleep(0.01) 
            except Exception as inner_e:
                if "'NoneType'" not in str(inner_e):
                    logger.warning(f"[CHAT DETAILS] Topic pagination interrupted: {inner_e}")

        # 🟢 SPEED FIX 3: Run both network requests at the EXACT SAME TIME!
        total_msgs_result, _ = await asyncio.gather(
            fetch_msg_count(),
            asyncio.wait_for(fetch_forum_topology(), timeout=5.0) if (is_forum and is_supergroup) else asyncio.sleep(0)
        )
        
        total_msgs = total_msgs_result

        return web.json_response({
            "status": "success",
            "id": str(chat.id),
            "title": chat.title or getattr(chat, "first_name", "Unknown"),
            "type": str(getattr(chat, "type", "Unknown")).replace("ChatType.", "").upper(),
            "members": getattr(chat, "members_count", 0),
            "total_messages": total_msgs,
            "description": getattr(chat, "description", getattr(chat, "bio", "")),
            "is_forum": is_forum,
            "topics": topics
        })
    except Exception as e:
        import traceback
        err_trace = traceback.format_exc()
        logger.error(f"[CHAT DETAILS ERROR] Traceback:\n{err_trace}")
        return web.json_response({"status": "error", "message": f"API Error: {str(e)}"})

async def _api_mediainfo_web_handler(request):
    data = await request.json()
    uid = int(data.get("user_id", 0))
    url = data.get("link", "")
    if not url: return web.json_response({"status": "error", "message": "No link provided"})
    
    file_path = Path(os.getcwd()) / f"web_mi_{uid}_{int(time.time())}.dat"
    file_name_display = "Unknown_File"
    file_size_display = 0
    
    try:
        # 🟢 FIX: Prioritize Telegram links FIRST so they don't get trapped by the HTTP downloader
        if "t.me" in url or "telegram.me" in url:
            parsed = _parse_source_link(url)
            chat_id = parsed.get("chat_id")
            msg_id = parsed.get("msg_id")
            
            # 🟢 DYNAMIC WAKE-UP: Automatically reconnect session if it fell asleep
            uclient = USER_CLIENTS.get(uid)
            if not uclient or not uclient.is_connected:
                session_str = await db.get_session(uid)
                if not session_str:
                    return web.json_response({"status": "error", "message": "Telegram session not active. Connect in Settings."})
                try:
                    api_id = await db.get_api_id(uid) or API_ID
                    api_hash = await db.get_api_hash(uid) or API_HASH
                    uclient = Client(f"User_{uid}", session_string=session_str, api_id=api_id, api_hash=api_hash, workers=100, ipv6=False)
                    uclient.add_handler(MessageHandler(user_watcher_handler, is_watched_chat))
                    await uclient.start()
                    USER_CLIENTS[uid] = uclient
                except Exception as e:
                    return web.json_response({"status": "error", "message": f"Session invalid: {e}"})
                
            try:
                msg = await uclient.get_messages(chat_id, msg_id)
            except Exception as e:
                return web.json_response({"status": "error", "message": f"Failed to fetch message: {e}"})
                
            if not msg or msg.empty: return web.json_response({"status": "error", "message": "Message not found or inaccessible"})
            
            media_obj = msg.document or msg.video or msg.audio or msg.photo
            if not media_obj: return web.json_response({"status": "error", "message": "No media found in the provided link"})
            
            file_name_display = getattr(media_obj, 'file_name', 'Telegram_Media')
            file_size_display = getattr(media_obj, 'file_size', 0)
            
            await partial_download_tg(uclient, msg, file_path, limit_mb=15)

        elif url.startswith("http"):
            file_size_display, detected_name = await partial_download_http(url, file_path, limit_mb=15)
            file_name_display = detected_name
        else:
            return web.json_response({"status": "error", "message": "Invalid link format"})
            
        real_ext = Path(file_name_display).suffix
        if real_ext:
            new_path = file_path.with_suffix(real_ext)
            file_path.rename(new_path)
            file_path = new_path
            
        cmd = ["mediainfo", str(file_path)]
        process = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        stdout, _ = await process.communicate()
        raw_output = stdout.decode('utf-8', errors='ignore').strip()
        
        if not raw_output:
            return web.json_response({"status": "error", "message": "Could not read media metadata. File might be empty or invalid."})
            
        raw_output = raw_output.replace(str(file_path), file_name_display).replace(str(file_path.absolute()), file_name_display)
        html_formatted = f"<div style='color:var(--accent); font-weight:bold; font-size:15px;'>📌 {html.escape(file_name_display)}</div><br>" + parseinfo(raw_output, file_size_display)
        
        return web.json_response({"status": "success", "html": html_formatted})
        
    except Exception as e:
        # 🟢 FIX: Force empty string errors to print their raw representation so the popup is never blank
        err_msg = str(e) if str(e).strip() else repr(e)
        return web.json_response({"status": "error", "message": f"Processing error: {err_msg}"})
    finally:
        if 'file_path' in locals() and file_path.exists():
            try: os.remove(file_path)
            except: pass

async def _api_spectrogram_web_handler(request):
    data = await request.json()
    uid = int(data.get("user_id", 0))
    url = data.get("link", "")
    if not url: return web.json_response({"status": "error", "message": "No link provided"})
    
    temp_dir = Path(f"./temp_sox_web_{uid}_{int(time.time())}")
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    original_file = temp_dir / "audio_input.dat"
    wav_file = temp_dir / "converted.wav"
    output_img = temp_dir / "spectrogram.png"
    
    try:
        # 1. DOWNLOAD FULL FILE
        if "t.me" in url or "telegram.me" in url:
            parsed = _parse_source_link(url)
            chat_id = parsed.get("chat_id")
            msg_id = parsed.get("msg_id")
            
            uclient = USER_CLIENTS.get(uid)
            if not uclient or not uclient.is_connected:
                return web.json_response({"status": "error", "message": "Telegram session not active. Connect in Settings."})
                
            msg = await uclient.get_messages(chat_id, msg_id)
            if msg.empty: return web.json_response({"status": "error", "message": "Message not found or inaccessible"})
            await uclient.download_media(msg, file_name=str(original_file))
        elif url.startswith("http"):
            await full_download_http(url, original_file)
        else:
            return web.json_response({"status": "error", "message": "Invalid link format"})

        # 2. FFMPEG
        ffmpeg_cmd = ["ffmpeg", "-i", str(original_file), "-vn", "-ac", "2", "-c:a", "pcm_f32le", str(wav_file), "-y"]
        process = await asyncio.create_subprocess_exec(*ffmpeg_cmd, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.PIPE)
        await process.wait()
        
        if not wav_file.exists(): return web.json_response({"status": "error", "message": "Audio Extraction Failed."})

        # 3. DSP & SOX
        stats = await asyncio.to_thread(generate_audio_stats_dsp, str(wav_file), str(original_file), "Web Audio")
        if not stats: return web.json_response({"status": "error", "message": "DSP Processing Failed."})

        sox_cmd = ["sox", str(wav_file), "-n", "spectrogram", "-o", str(output_img), "-x", "1000", "-Y", "800", "-c", "Audio", "-t", " "]
        process_sox = await asyncio.create_subprocess_exec(*sox_cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        await process_sox.communicate()

        if not output_img.exists(): return web.json_response({"status": "error", "message": "SoX Generation Failed."})

        # 4. CONVERT TO BASE64 & HTML
        with open(output_img, "rb") as img_f:
            img_b64 = base64.b64encode(img_f.read()).decode('utf-8')

        m = stats['mastering']
        mastering_html = ""
        if m:
            mastering_html = (
                f"<br><span style='color:var(--accent);'><b>— MASTERING ANALYSIS —</b></span><br>"
                f"🎚 <b>Dynamic Range:</b> DR {m['dr']}<br>"
                f"🔊 <b>Loudness:</b> {m['lufs']:.1f} LUFS<br>"
                f"📈 <b>Peak / RMS:</b> {m['peak']:.2f} dBFS / {m['rms']:.2f} dB<br>"
                f"🏷 <b>Score:</b> {m['grade']}"
            )

        html_stats = (
            f"<span style='color:#10b981;'><b>{stats['auth_badge']}</b></span><br>"
            f"<i>{stats['auth_desc']}</i><br><br>"
            f"📀 <b>Format:</b> {stats['format']} • {stats['channel_str']} • {stats['bit_depth']}-bit • {stats['sample_rate']/1000} kHz<br>"
            f"📈 <b>Cutoff:</b> {stats['cutoff']} kHz<br>"
            f"🧱 <b>Cliff Drop:</b> {stats['cliff_drop']:.1f} dB"
            f"{mastering_html}"
        )

        return web.json_response({"status": "success", "image": img_b64, "html": html_stats})

    except Exception as e:
        return web.json_response({"status": "error", "message": f"Processing error: {e}"})
    finally:
        import shutil
        try: shutil.rmtree(str(temp_dir), ignore_errors=True)
        except: pass

# ==============================================================================
from collections import defaultdict

USER_STREAM_BOTS = defaultdict(list)
USER_TASK_BOTS = defaultdict(list)

async def init_worker_bots(user_id=None):
    """Initializes isolated bot clients for streaming vs tasks."""
    user_ids_to_init = [user_id] if user_id else []
    if not user_id:
        # 🟢 FIX: Check all 3 arrays so it boots up perfectly on startup
        cursor = db.col.find({"$or": [
            {"stream_tokens": {"$exists": True, "$ne": []}}, 
            {"task_tokens": {"$exists": True, "$ne": []}},
            {"bot_tokens": {"$exists": True, "$ne": []}}
        ]})
        async for u in cursor:
            user_ids_to_init.append(u["id"])
            
    for uid in user_ids_to_init:
        # Stop existing Stream Bots
        for c in USER_STREAM_BOTS.get(uid, []):
            try: await c.stop()
            except Exception: pass
        USER_STREAM_BOTS[uid].clear()
        
        # Stop existing Task Bots
        for c in USER_TASK_BOTS.get(uid, []):
            try: await c.stop()
            except Exception: pass
        USER_TASK_BOTS[uid].clear()
        
        user_doc = await db.col.find_one({"id": uid})
        if not user_doc: continue
        
        # 🟢 Migrate old tokens to stream array if necessary
        stream_tokens = user_doc.get("stream_tokens", [])
        if not stream_tokens and user_doc.get("bot_tokens"):
            stream_tokens = user_doc.get("bot_tokens")
            
        task_tokens = user_doc.get("task_tokens", [])
        
        # 1. Initialize Stream Bots
        for idx, token in enumerate(stream_tokens, start=1):
            try:
                # 🟢 FIX: Increased workers to 100 to stop queue drops
                bot_client = Client(f"stream_bot_{uid}_{idx}", api_id=API_ID, api_hash=API_HASH, bot_token=token.strip(), workers=100, no_updates=True, ipv6=False)
                await bot_client.start()
                USER_STREAM_BOTS[uid].append(bot_client)
                logger.info(f"🚀 Stream Bot {idx} active for user {uid}")
            except Exception as e:
                logger.warning(f"Failed to load stream token {idx} for {uid}: {e}")

        # 2. Initialize Task Bots
        for idx, token in enumerate(task_tokens, start=1):
            try:
                # 🟢 FIX: Increased workers to 100 to stop queue drops
                bot_client = Client(f"task_bot_{uid}_{idx}", api_id=API_ID, api_hash=API_HASH, bot_token=token.strip(), workers=100, no_updates=True, ipv6=False)
                await bot_client.start()
                USER_TASK_BOTS[uid].append(bot_client)
                logger.info(f"🚀 Task Bot {idx} active for user {uid}")
            except Exception as e:
                logger.warning(f"Failed to load task token {idx} for {uid}: {e}")

async def _api_get_worker_tokens(request):
    uid = request["authenticated_user_id"]
    doc = await db.col.find_one({"id": uid})
        
    # 🟢 FIX: Auto-load your old "bot_tokens" into the streaming box if you haven't saved new ones yet!
    stream_tokens = doc.get("stream_tokens", [])
    if not stream_tokens and doc.get("bot_tokens"):
        stream_tokens = doc.get("bot_tokens")
        
    return web.json_response({
        "status": "success", 
        "stream_tokens": stream_tokens,
        "task_tokens": doc.get("task_tokens", []) if doc else []
    })

async def _api_save_worker_tokens(request):
    data = await request.json()
    uid = request["authenticated_user_id"]
    
    stream_tokens = [t.strip() for t in data.get("stream_tokens", []) if ":" in t]
    task_tokens = [t.strip() for t in data.get("task_tokens", []) if ":" in t]
    
    # Save directly to the User's Database Object
    await db.col.update_one(
        {"id": uid}, 
        {"$set": {"stream_tokens": stream_tokens, "task_tokens": task_tokens}}, 
        upsert=True
    )
    asyncio.create_task(init_worker_bots(uid))
    
    # Clear access cache so the new bots are used immediately
    TG_ACCESS_CACHE.clear()
    
    return web.json_response({"status": "success", "message": f"Saved {len(stream_tokens)} Stream Bots and {len(task_tokens)} Task Bots. Pools reloading."})

async def _api_network_stats(request):
    uid = request["authenticated_user_id"]
        
    # 🟢 PRIVACY FIX: Filter streams so normal users only see their own!
    is_admin = await db.is_user_admin(uid)
    active_list = list(GLOBAL_NETWORK_STATS["active"].values())
    recent_list = GLOBAL_NETWORK_STATS["recent"]

    if not is_admin:
        active_list = [s for s in active_list if str(s.get("user_id", "")) == str(uid)]
        recent_list = [s for s in recent_list if str(s.get("user_id", "")) == str(uid)]
        
    return web.json_response({
        "status": "success",
        "active": active_list,
        "recent": recent_list,
        "worker_bots_count": len(USER_STREAM_BOTS.get(uid, [])) + len(USER_TASK_BOTS.get(uid, []))
    })

# --- NEW: STEALTH IMAGE PROXY TO BYPASS HUGGINGFACE & TMDB ---
async def _api_bg_proxy(request):
    url = request.query.get("url", "")
    if not url: return web.Response(status=400)
    import aiohttp
    try:
        # 🟢 FIX: Mimic Google Chrome perfectly to bypass TMDB's 403 Anti-Bot Protection
        stealth_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.themoviedb.org/",
            "Sec-Fetch-Dest": "image",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "cross-site"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=stealth_headers) as resp:
                body = await resp.read()
                return web.Response(body=body, headers={"Content-Type": "image/jpeg", "Cache-Control": "public, max-age=8640000"})
    except Exception:
        return web.Response(status=500)

async def _api_playlist_handler(request):
    """Extracts playlist array from ZIPs and Split ZIPs for continuous album playback."""
    try: user_id = int(request.query.get("user_id", 0))
    except: user_id = 0
    link = request.query.get("link", "").strip()
    if not link: return web.json_response({"status": "error"})
    
    is_tg = _is_tg_link(link)
    playlist = []
    try:
        if is_tg:
            parsed = _parse_source_link(link)
            chat_id = parsed.get("chat_id")
            msg_id = parsed.get("msg_id")
            pool, _ = await _get_working_tg_pool(user_id, chat_id, msg_id)
            primary_client = pool[0]
            
            msg = await get_client_msg(primary_client, chat_id, msg_id)
            media = msg.document or msg.video or msg.audio
            filename = str(getattr(media, "file_name", "")).lower()
            
            # 🟢 FIX: Support all major archive extensions for the playlist extractor (.zip.001, .7z.001, etc)
            is_zip = bool(re.search(r'\.(zip|7z|rar|tar|gz)(\.\d{3})?$', filename))
            if not is_zip: return web.json_response({"status": "success", "playlist": []})
            
            parts_map = []
            global_offset = 0
            match = re.search(r'\.(\d{2,3})$', filename)
            if match and int(match.group(1)) == 1:
                current_id = msg_id
                while True:
                    try:
                        m = await get_client_msg(primary_client, chat_id, current_id)
                        doc = m.document or m.video or m.audio
                        if not doc: break
                        psz = int(doc.file_size or 0)
                        parts_map.append({"msg_id": m.id, "start": global_offset, "end": global_offset + psz, "size": psz})
                        global_offset += psz
                        current_id += 1
                        next_m = await get_client_msg(primary_client, chat_id, current_id)
                        next_doc = next_m.document or next_m.video or next_m.audio
                        if not next_doc or not re.search(r'\.\d{2,3}$', next_doc.file_name or ""): break
                    except Exception: break
            else:
                part_size = int(getattr(media, "file_size", 0) or 0)
                parts_map.append({"msg_id": msg_id, "start": 0, "end": part_size, "size": part_size})
                global_offset = part_size
                
            async def zip_read_tg(off, length):
                buf = bytearray()
                async for chunk in parallel_stream_generator(primary_client, chat_id, parts_map, off, length):
                    buf.extend(chunk)
                    if len(buf) >= length: break
                return bytes(buf[:length])
                
            playlist = await get_zip_playlist(zip_read_tg, global_offset)
        else:
            actual_url = await resolve_direct_link(link)
            filename = _guess_filename_from_url(actual_url, original_url=link).lower()
            
            is_zip = bool(re.search(r'\.(zip|7z|rar|tar|gz)(\.\d{3})?$', filename))
            if not is_zip: return web.json_response({"status": "success", "playlist": []})
            
            session = await _get_direct_http_session()
            
            zip_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0"}
            from streaming.direct_stream import DIRECT_HEADER_CACHE
            cached_h = DIRECT_HEADER_CACHE.get(actual_url) or DIRECT_HEADER_CACHE.get(link) or {}
            for h_key in ["Cookie", "Referer", "Authorization", "User-Agent"]:
                if h_key in cached_h: 
                    zip_headers[h_key] = cached_h[h_key]

            raw_size = int(cached_h.get("meta_content_length", 0))
            if raw_size <= 0:
                try:
                    # 🟢 FAST NATIVE STRING (No _safe_yarl corruption)
                    async with session.head(actual_url, headers=zip_headers, allow_redirects=True) as h_resp:
                        raw_size = int(h_resp.headers.get("Content-Length", 0))
                except Exception: pass
                
            if raw_size <= 0:
                try:
                    get_h = zip_headers.copy()
                    get_h["Range"] = "bytes=0-0"
                    async with session.get(actual_url, headers=get_h, allow_redirects=True) as g_resp:
                        cr = g_resp.headers.get("Content-Range", "")
                        if cr and "/" in cr:
                            raw_size = int(cr.split("/")[-1])
                        else:
                            raw_size = int(g_resp.headers.get("Content-Length", 0))
                except Exception: pass

            if raw_size <= 0:
                return web.json_response({"status": "error", "message": "Failed to determine ZIP size. Host may be blocking requests."})

            async def zip_read_http(off, length):
                z_req_headers = zip_headers.copy()
                z_req_headers["Range"] = f"bytes={off}-{off+length-1}"
                async with session.get(actual_url, headers=z_req_headers) as r:
                    return await r.read()
                    
            playlist = await get_zip_playlist(zip_read_http, raw_size)

        return web.json_response({"status": "success", "playlist": playlist})
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)})

# ==============================================================================
# --- NEW: WORLD EXPLORER PROXY ENDPOINTS ---
# ==============================================================================
async def _api_proxy_country(request):
    iso = request.query.get("iso", "").strip()
    name = request.query.get("name", "").strip()
    import aiohttp
    import json
    from urllib.parse import quote

    async def fetch_api(url):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        try:
            # 🟢 FIX: Increased timeout to 10s and disabled strict SSL to prevent Koyeb blocks
            timeout = aiohttp.ClientTimeout(total=10)
            connector = aiohttp.TCPConnector(ssl=False)
            async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
                async with session.get(url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if isinstance(data, list) and len(data) > 0: return data
                        if isinstance(data, dict): return [data] # Always format as list
        except Exception as e:
            print(f"[Globe API] Backend failed: {e}")
        return None

    try:
        data = None
        # Attempt 1: Try ISO Code
        if iso and iso != "-99":
            data = await fetch_api(f"https://restcountries.com/v3.1/alpha/{iso}")
        
        # Attempt 2: Fallback to Exact Name Search
        if not data and name:
            data = await fetch_api(f"https://restcountries.com/v3.1/name/{quote(name)}?fullText=true")
            
        # Attempt 3: Fallback to Partial Name Search
        if not data and name:
            data = await fetch_api(f"https://restcountries.com/v3.1/name/{quote(name)}")

        # Attempt 4: Fallback to V2 API if V3 is rate-limited
        if not data and iso and iso != "-99":
            data = await fetch_api(f"https://restcountries.com/v2/alpha/{iso}")

        if data:
            return web.json_response(data)
        else:
            # 🟢 FIX: Return real Earth icon if API fails
            mock_data = {
                "name": {"common": name or "Unknown Country"},
                "capital": ["Unavailable"],
                "region": "Unavailable",
                "population": "Unavailable",
                "timezones": ["UTC"],
                "flags": {"png": "https://cdn-icons-png.flaticon.com/512/44/44386.png"} 
            }
            return web.json_response([mock_data])
            
    except Exception as e:
        mock_data = {
            "name": {"common": name or "Unknown Country"},
            "capital": ["Unavailable"],
            "region": "Unavailable",
            "population": "Unavailable",
            "timezones": ["UTC"],
            "flags": {"png": "https://cdn-icons-png.flaticon.com/512/44/44386.png"}
        }
        return web.json_response([mock_data])

async def _api_proxy_wiki(request):
    q = request.query.get("q", "").strip()
    import aiohttp
    from urllib.parse import quote
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        async with aiohttp.ClientSession() as session:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(q)}"
            async with session.get(url, headers=headers) as resp:
                text = await resp.text()
                return web.Response(status=resp.status, text=text, content_type="application/json")
    except Exception as e:
        return web.Response(status=500, text=str(e))

# ==============================================================================
# --- MEDIA EDITOR PROGRESS TRACKER ---
# ==============================================================================
EDITOR_UI_STATE = {}
EDITOR_ACTIVE_TASKS = {}  # 🟢 Track active Python tasks for cancellation

async def _api_editor_cancel(request):
    try:
        data = await request.json()
        task_uuid = data.get("task_uuid")
        uid = request["authenticated_user_id"]

        if task_uuid == "all":
            for tid, tinfo in list(EDITOR_ACTIVE_TASKS.items()):
                if tinfo["user_id"] == uid:
                    tinfo["task"].cancel()
            return web.json_response({"status": "success", "message": "All tasks cancelled."})
            
        if task_uuid in EDITOR_ACTIVE_TASKS:
            tinfo = EDITOR_ACTIVE_TASKS[task_uuid]
            if tinfo["user_id"] == uid:
                tinfo["task"].cancel()
                return web.json_response({"status": "success"})
        return web.json_response({"status": "error", "message": "Task not found"})
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)})

async def _api_editor_progress(request):
    task_uuid = request.query.get("task_uuid")
    if not task_uuid or task_uuid not in EDITOR_UI_STATE:
        return web.json_response({"status": "error", "message": "Task not found"})
    
    state = EDITOR_UI_STATE[task_uuid]
    if state.get("user_id") != request["authenticated_user_id"]:
        return web.json_response({"status": "error", "message": "Task not found"}, status=404)
    resp = {
        "status": "success", "phase": state["phase"], "done": state["done"], 
        "result": "FAILED" if state.get("error") else "SUCCESS" if state.get("done") else "RUNNING",
        "error": state["error"], "fetcher": state.get("fetcher", "🤖 Unknown"), 
        "uploader": state.get("uploader", "🤖 Unknown")
    }
    
    # 🟢 Bridge download AND split uploads ("Uploading Part 1/3") into the Web UI
    typ = "down" if "Downloading" in state["phase"] else ("up" if "Uploading" in state["phase"] else None)
    if typ:
        prog = PROGRESS.get(f"{task_uuid}:{typ}")
        if prog:
            resp["percent"] = prog.get("percent", 0)
            resp["speed"] = prog.get("speed", 0)
            resp["current"] = prog.get("current", 0)
            resp["total"] = prog.get("total", 0)
            resp["eta"] = prog.get("eta", 0)
                
    return web.json_response(resp)

# 🟢 NEW ENDPOINT: Restores tasks when you refresh your browser
async def _api_editor_active_tasks(request):
    uid = request["authenticated_user_id"]
    active = {}
    for t_uuid, t_info in list(EDITOR_ACTIVE_TASKS.items()):
        if t_info.get("user_id") == uid:
            state = EDITOR_UI_STATE.get(t_uuid, {})
            active[t_uuid] = {
                "file_name": state.get("file_name", "Media Task"),
                "fetcher": state.get("fetcher", "🌐 Direct Link"),
                "uploader": state.get("uploader", "🤖 Pending")
            }
    return web.json_response({"status": "success", "tasks": active})
    uid = int(request.query.get("user_id", 0))
    active = {}
    for t_uuid, t_info in list(EDITOR_ACTIVE_TASKS.items()):
        if t_info.get("user_id") == uid:
            state = EDITOR_UI_STATE.get(t_uuid, {})
            active[t_uuid] = {
                "file_name": state.get("file_name", "Media Task"),
                "fetcher": state.get("fetcher", "🤖 Pending"),
                "uploader": state.get("uploader", "🤖 Pending")
            }
    return web.json_response({"status": "success", "tasks": active})          
    
async def _api_edit_media_handler(request):
    data = await request.json()
    uid = int(data.get("user_id", 0))
    link = data.get("link", "")
    is_archive = data.get("is_archive", False)
    config = data.get("config", [])
    new_name = build_media_filename(str(data.get("new_name", "output.mkv")))
    dest = data.get("dest", "tg")
    upload_mode = data.get("upload_mode", "document").lower()
    thumb_b64 = data.get("thumb", "")
    global_tags = data.get("global_tags", {})
    if not isinstance(global_tags, dict):
        global_tags = {}
    global_tags = {str(key): clean_media_text(value) for key, value in global_tags.items()}
    if isinstance(config, list):
        for track in config:
            if isinstance(track, dict) and "title" in track:
                track["title"] = clean_media_text(track["title"])
    
    if not link or (not is_archive and not config):
        return web.json_response({"status": "error", "message": "Missing link or config"})
        
    # 🟢 1. PRE-FLIGHT ACCESS CHECK & DESTINATION PARSING
    upload_chat_id = dest
    upload_thread_id = None
    
    if dest not in ["tg", "gofile"]:
        if "/" in str(dest):
            parts = str(dest).split("/", 1)
            upload_chat_id = parts[0]
            upload_thread_id = int(parts[1])
        try: upload_chat_id = int(upload_chat_id)
        except: pass
        
        uclient = USER_CLIENTS.get(uid)
        stream_bots = USER_STREAM_BOTS.get(uid, [])
        has_access = False
        
        # Priority 1: Test Stream Bots and Main Bot
        for b in stream_bots + [app]:
            try:
                if not getattr(b, "is_connected", False): await b.connect()
                await b.get_chat(upload_chat_id)
                has_access = True
                break
            except: pass
            
        # Priority 2: Fallback test User Session
        if not has_access and uclient and uclient.is_connected:
            try:
                await uclient.get_chat(upload_chat_id)
                has_access = True
            except: pass
            
        if not has_access:
            return web.json_response({"status": "error", "message": "Access Denied: Neither your Stream Bots, Main Bot, nor User Session have access to that Chat/Channel ID. Please add them to the chat as Admins first!"})

    import time
    import math
    from pathlib import Path
    import shutil
    import base64
    import os
    import zipfile
    import re  # 🟢 THE FIX: Moved to the top so HTTP links can use it!
    
    task_uuid = uuid.uuid4().hex[:8]
    temp_dir = Path(f"./temp_remux_{uid}_{task_uuid}")
    EDITOR_UI_STATE[task_uuid] = {
        "phase": "Starting...", "status_msg_id": None, "error": None, "done": False,
        "user_id": uid, "file_name": new_name, "fetcher": "🌐 Direct Link", "uploader": "🤖 Pending..."
    }
    
    def _lbl(c):
        if not c: return "Unknown"
        nm = getattr(c, "name", "Unknown")
        if "User_" in nm or "temp_acc_" in nm: return "👤 User Session"
        if "worker_bot_" in nm or "stream_bot_" in nm or "task_bot_" in nm: return f"🤖 Worker {nm.split('_')[-1]}"
        if nm == "RestrictedBot": return "🤖 Main Bot"
        return f"🤖 {nm}"

    async def safe_tg_edit(msg, text):
        try: await msg.edit_text(text)
        except Exception: pass

    async def background_editor():
        nonlocal new_name
        temp_dir.mkdir(parents=True, exist_ok=True)
        input_file = temp_dir / "input_media.dat"
        output_file = temp_dir / sanitize_filename(new_name)
        thumb_path = None

        # 🟢 MOVED TO TOP: RICH CAPTION & METADATA EXTRACTORS
        async def generate_rich_caption(file_path, file_name, pre_probed_info=None):
            try:
                import json, math, os, re
                
                # 1. Exact Size
                try: size_bytes = os.path.getsize(file_path)
                except Exception: size_bytes = 0
                k = 1024
                sizes = ['B', 'KB', 'MB', 'GB', 'TB']
                i = 0 if size_bytes == 0 else math.floor(math.log(size_bytes) / math.log(k))
                size_str = f"{(size_bytes / (k**i)):.1f} {sizes[i]}"
                
                caption = f"`{file_name}`\n\n🗂 {size_str}"
                
                # 2. Bypass FFprobe for chunks if we don't have pre-probed info
                info = pre_probed_info
                file_name_lower = str(file_name).lower()
                is_archive_or_split = file_name_lower.endswith(('.zip', '.rar', '.7z', '.tar', '.gz')) or re.search(r'\.\d{3}$', file_name_lower)
                
                if not info:
                    if is_archive_or_split:
                        return caption
                    cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", str(file_path)]
                    proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
                    stdout, _ = await proc.communicate()
                    info = json.loads(stdout)
                
                # 3. Dynamic Time Formatter (Days, Hours, Mins, Secs)
                dur_sec = float(info.get('format', {}).get('duration', 0))
                d = math.floor(dur_sec / 86400)
                h = math.floor((dur_sec % 86400) / 3600)
                m = math.floor((dur_sec % 3600) / 60)
                s = math.floor(dur_sec % 60)
                
                if d > 0: dur_str = f"{d}d {h}h {m}m {s}s"
                elif h > 0: dur_str = f"{h}h {m}m {s}s"
                elif m > 0: dur_str = f"{m}m {s}s"
                else: dur_str = f"{s}s"
                
                v_stream = next((st for st in info.get('streams', []) if st.get('codec_type') == 'video' and st.get('codec_name') not in ['mjpeg', 'png']), None)
                a_streams = [st for st in info.get('streams', []) if st.get('codec_type') == 'audio']
                s_streams = [st for st in info.get('streams', []) if st.get('codec_type') == 'subtitle']
                
                if v_stream:
                    w = v_stream.get('width', '?')
                    h = v_stream.get('height', '?')
                    
                    a_langs = []
                    for a in a_streams:
                        lng = a.get('tags', {}).get('language', a.get('tags', {}).get('LANGUAGE', 'Unknown')).title()
                        if lng not in a_langs: a_langs.append(lng)
                    
                    s_langs = []
                    for sub in s_streams:
                        lng = sub.get('tags', {}).get('language', sub.get('tags', {}).get('LANGUAGE', 'None')).title()
                        if lng not in s_langs: s_langs.append(lng)
                        
                    a_str = ", ".join(a_langs) if a_langs else "Unknown"
                    s_str = ", ".join(s_langs) if s_langs else "None"
                    
                    caption += f" 💎 {w}x{h}\n⏳ {dur_str} 💬 {s_str}\n🔊 {a_str}"
                elif a_streams:
                    # 🟢 Hide Audio Tags if zipped/split (per your request)
                    if is_archive_or_split:
                        return caption
                        
                    a = a_streams[0]
                    codec = str(a.get('codec_name', 'Unknown')).upper()
                    
                    if codec == 'EAC3': codec = 'E-AC-3 (Dolby Digital Plus / Atmos)'
                    elif codec == 'TRUEHD': codec = 'TrueHD (Dolby Atmos)'
                    elif 'DSD' in codec: codec = 'DSD (Direct Stream Digital)'
                    elif codec == 'DCA': codec = 'DTS Audio'
                    elif codec == 'ALAC': codec = 'Apple Lossless (ALAC)'
                    
                    sr = int(a.get('sample_rate', 0)) / 1000
                    bits = a.get('bits_per_raw_sample') or a.get('bits_per_sample') or '16'
                    
                    if 'DSD' in codec:
                        caption += f"\n🎧 {codec} • 1-Bit - {sr}kHz"
                    else:
                        caption += f"\n🎧 {codec} • {bits}Bit - {sr}kHz"
                    
                return caption
            except Exception:
                return f"`{file_name}`"

        async def get_audio_metadata(file_path):
            try:
                import json, math, os
                cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", str(file_path)]
                proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
                stdout, _ = await proc.communicate()
                info = json.loads(stdout)
                
                duration = math.ceil(float(info.get('format', {}).get('duration', 0)))
                
                all_tags = {}
                for s in info.get('streams', []):
                    if s.get('codec_type') == 'audio':
                        for k, v in s.get('tags', {}).items():
                            all_tags[k.lower()] = str(v).strip()
                            
                for k, v in info.get('format', {}).get('tags', {}).items():
                    all_tags[k.lower()] = str(v).strip()
                    
                title = all_tags.get('title') or all_tags.get('©nam') or file_path.name
                
                artist = None
                for k in ['artist', 'album_artist', 'albumartist', 'performer', 'author', 'composer', '©art', 'aart']:
                    if k in all_tags:
                        artist = all_tags[k]
                        break
                        
                if not artist:
                    for k, v in all_tags.items():
                        if 'artist' in k or 'author' in k:
                            artist = v
                            break
                            
                if not artist:
                    artist = "Unknown Artist"
                
                cover_path = str(file_path) + "_cover.jpg"
                c_cmd = ["ffmpeg", "-y", "-i", str(file_path), "-an", "-vcodec", "copy", cover_path]
                c_proc = await asyncio.create_subprocess_exec(*c_cmd, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL)
                await c_proc.communicate()
                
                if not os.path.exists(cover_path) or os.path.getsize(cover_path) == 0:
                    c_cmd = ["ffmpeg", "-y", "-i", str(file_path), "-an", "-vframes", "1", cover_path]
                    c_proc = await asyncio.create_subprocess_exec(*c_cmd, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL)
                    await c_proc.communicate()
                    
                if not os.path.exists(cover_path) or os.path.getsize(cover_path) == 0:
                    cover_path = None
                    
                return {"duration": duration, "performer": artist, "title": title, "thumb": cover_path}
            except Exception:
                return {}
        
        try:
            status_msg = await app.send_message(uid, f"⚙️ **Media Editor Task Started!**\n\n📄 **Target:** `{new_name}`\n⏳ **Phase:** Downloading sources...")
            EDITOR_UI_STATE[task_uuid]["status_msg_id"] = status_msg.id
            
            if thumb_b64:
                try:
                    thumb_data = base64.b64decode(thumb_b64.split(",")[1] if "," in thumb_b64 else thumb_b64)
                    thumb_path = temp_dir / "thumb.jpg"
                    with open(thumb_path, "wb") as f:
                        f.write(thumb_data)
                except Exception as e:
                    logger.warning(f"Thumb decode failed: {e}")

            # DOWNLOAD EXTERNAL TRACKS
            EDITOR_UI_STATE[task_uuid]["phase"] = "Downloading"
            for idx, track in enumerate(config):
                if track.get("type") in ["ext_audio", "ext_sub"]:
                    ext_path = temp_dir / f"ext_track_{idx}_{track['type']}.dat"
                    if track.get("b64"):
                        try:
                            b64_data = track["b64"].split(",")[1] if "," in track["b64"] else track["b64"]
                            with open(ext_path, "wb") as f:
                                f.write(base64.b64decode(b64_data))
                        except Exception: pass
                    elif track.get("url"):
                        ext_link = track["url"]
                        try:
                            if _is_tg_link(ext_link):
                                eparsed = _parse_source_link(ext_link)
                                wp, _ = await _get_working_tg_pool(uid, eparsed["chat_id"], eparsed["msg_id"])
                                eclient = wp[0] if wp else app
                                emsg = await get_client_msg(eclient, eparsed["chat_id"], eparsed["msg_id"])
                                await eclient.download_media(emsg, file_name=str(ext_path))
                            else:
                                await full_download_http(ext_link, str(ext_path), task_uuid=task_uuid)
                        except Exception: pass
                    if ext_path.exists():
                        track["local_path"] = str(ext_path)

            # 🟢 DOWNLOAD MAIN FILE (WITH SMART STITCHING ENGINE FOR .001 & BATCH RANGES)
            is_tg = _is_tg_link(link)
            if is_tg:
                parsed = _parse_source_link(link)
                chat_id = parsed["chat_id"]
                start_id = parsed["msg_id"]
                end_id = parsed.get("msg_id_end")
                
                working_pool, _ = await _get_working_tg_pool(uid, chat_id, start_id)
                client_to_use = working_pool[0] if working_pool else app
                EDITOR_UI_STATE[task_uuid]["fetcher"] = _lbl(client_to_use)
                
                messages_to_stitch = []
                total_bytes = 0
                
                EDITOR_UI_STATE[task_uuid]["phase"] = "Analyzing Split Parts..."
                
                # SCENARIO A: Explicit Range given (e.g. 517544 - 517547)
                if end_id and end_id > start_id:
                    for i in range(start_id, end_id + 1):
                        try:
                            m = await get_client_msg(client_to_use, chat_id, i)
                            doc = m.document or m.video or m.audio
                            if doc:
                                messages_to_stitch.append(m)
                                total_bytes += getattr(doc, "file_size", 0)
                        except Exception: pass
                        
                # SCENARIO B: Single link, but auto-discover if it's a .001 file!
                else:
                    m = await get_client_msg(client_to_use, chat_id, start_id)
                    doc = m.document or m.video or m.audio
                    if doc:
                        messages_to_stitch.append(m)
                        total_bytes += getattr(doc, "file_size", 0)
                        fname = str(getattr(doc, "file_name", "")).lower()
                        
                        if re.search(r'\.001$', fname):
                            curr_id = start_id + 1
                            while True:
                                try:
                                    next_m = await get_client_msg(client_to_use, chat_id, curr_id)
                                    next_doc = next_m.document or next_m.video or next_m.audio
                                    if not next_doc or not re.search(r'\.\d{3}$', str(getattr(next_doc, "file_name", "")).lower()):
                                        break
                                    messages_to_stitch.append(next_m)
                                    total_bytes += getattr(next_doc, "file_size", 0)
                                    curr_id += 1
                                except Exception: break

                if not messages_to_stitch:
                    raise Exception("No valid media found in the provided link or range.")

                num_parts = len(messages_to_stitch)
                EDITOR_UI_STATE[task_uuid]["phase"] = f"Downloading {num_parts} Part{'s' if num_parts > 1 else ''}"
                await safe_tg_edit(status_msg, f"📥 **Downloading & Stitching {num_parts} Part{'s' if num_parts > 1 else ''}...**\n\n📄 `{new_name}`")
                
                # STITCHING DOWNLOADER (Streams all parts directly into a single massive file)
                with open(input_file, "wb") as f_out:
                    downloaded = 0
                    for m_idx, msg in enumerate(messages_to_stitch):
                        async for chunk in client_to_use.stream_media(msg):
                            f_out.write(chunk)
                            downloaded += len(chunk)
                            
                            try:
                                if asyncio.iscoroutinefunction(progress):
                                    await progress(downloaded, total_bytes, "down", task_uuid)
                                else:
                                    progress(downloaded, total_bytes, "down", task_uuid)
                            except Exception as e:
                                if "CANCELLED" in str(e).upper():
                                    raise Exception("Download Cancelled by User")
            else:
                await full_download_http(link, str(input_file), task_uuid=task_uuid)
                
            # 🟢 DYNAMIC BRANCH: ARCHIVE EXTRACTION & TRACK-BY-TRACK UPLOADER
            if is_archive or str(input_file).lower().endswith(('.zip', '.tar', '.gz', '.7z', '.rar')) or re.search(r'\.(zip|7z|rar)\.\d{3}$', link.lower()):
                EDITOR_UI_STATE[task_uuid]["phase"] = "Extracting Archive"
                await safe_tg_edit(status_msg, "🗜 **Unpacking Archive Tracks...**")
                
                extract_dir = temp_dir / "extracted_media"
                extract_dir.mkdir(parents=True, exist_ok=True)
                
                async def unpack_archive():
                    # 🟢 FIX: Use robust 7-Zip engine to handle RAR, 7Z, and heavy Split-ZIPs seamlessly
                    cmd = ["7z", "x", str(input_file), f"-o{extract_dir}", "-y"]
                    proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
                    await proc.communicate()
                    
                    if proc.returncode != 0:
                        # Fallback to Python's native zip extractor
                        def fallback_unzip():
                            import zipfile
                            with zipfile.ZipFile(input_file, 'r') as zf:
                                zf.extractall(extract_dir)
                        await asyncio.to_thread(fallback_unzip)
                
                try:
                    await unpack_archive()
                except Exception as e:
                    raise Exception(f"Failed to extract archive. Corrupt or unsupported format: {e}")
                
                # 🟢 Gather media and document tracks
                audio_exts = ('.flac', '.mp3', '.m4a', '.wav', '.aac', '.opus', '.ogg', '.alac', '.mka', '.dsf', '.dff', '.ac3', '.eac3', '.dts')
                video_exts = ('.mp4', '.mkv', '.webm', '.avi', '.ts', '.mov', '.m4v')
                doc_exts = ('.txt', '.lrc', '.srt', '.vtt', '.nfo', '.jpg', '.jpeg', '.png', '.pdf')
                
                audio_files = []
                video_files = []
                doc_files = []
                
                for root, _, files in os.walk(extract_dir):
                    for f in sorted(files):
                        f_low = f.lower()
                        p = Path(root) / f
                        if f_low.endswith(audio_exts):
                            audio_files.append(p)
                        elif f_low.endswith(video_exts):
                            video_files.append(p)
                        elif f_low.endswith(doc_exts):
                            doc_files.append(p)
                            
                all_media = audio_files + video_files + doc_files
                if not all_media:
                    raise Exception("No supported audio, video, or document files found inside the archive.")
                    
                total_tracks = len(all_media)
                final_chat_id = uid if dest == "tg" else upload_chat_id
                
                uclient = USER_CLIENTS.get(uid)
                is_premium = False
                if uclient and uclient.is_connected:
                    try:
                        me = uclient.me or await uclient.get_me()
                        is_premium = getattr(me, "is_premium", False)
                    except: pass
                    
                # Process and upload each track cleanly
                for t_idx, track_path in enumerate(all_media, start=1):
                    is_audio = track_path in audio_files
                    is_video = track_path in video_files
                    t_type = "Audio" if is_audio else ("Video" if is_video else "Document")
                    
                    EDITOR_UI_STATE[task_uuid]["phase"] = f"Uploading {t_type} {t_idx}/{total_tracks}"
                    await safe_tg_edit(status_msg, f"☁️ **Uploading {t_type} {t_idx} of {total_tracks}...**\n`{track_path.name}`")
                    
                    if dest == "gofile":
                        url = await upload_to_gofile(str(track_path))
                        await app.send_message(uid, f"✅ **{t_type} {t_idx} Extracted & Uploaded!**\n\n🔗 **GoFile Link:** {url}", disable_web_page_preview=True)
                        try: os.remove(track_path)
                        except Exception: pass
                        continue

                    # Telegram Dynamic Upload Routing & >2GB Fallback
                    file_size = os.path.getsize(track_path)
                    max_size = (3980 * 1024 * 1024) if is_premium else (1980 * 1024 * 1024)
                    
                    upload_client = app
                    is_bot = True

                    if file_size > (1980 * 1024 * 1024) and is_premium:
                        if uclient and getattr(uclient, "is_connected", False):
                            upload_client = uclient
                            is_bot = False
                    else:
                        stream_bots = USER_STREAM_BOTS.get(uid, [])
                        valid_bot = None
                        import random
                        shuffled_bots = list(stream_bots)
                        random.shuffle(shuffled_bots)
                        for b in shuffled_bots:
                            try:
                                if not getattr(b, "is_connected", False): await b.connect()
                                await b.get_chat(final_chat_id)
                                valid_bot = b
                                break
                            except: pass
                            
                        if valid_bot:
                            upload_client = valid_bot
                        else:
                            try:
                                await app.get_chat(final_chat_id)
                                upload_client = app
                            except:
                                if uclient and uclient.is_connected:
                                    upload_client = uclient
                                    is_bot = False

                    EDITOR_UI_STATE[task_uuid]["uploader"] = _lbl(upload_client)
                    
                    if file_size > max_size:
                        total_parts = math.ceil(file_size / max_size)
                        EDITOR_UI_STATE[task_uuid]["phase"] = f"Splitting {t_type} {t_idx}"
                        part_num = 1
                        with open(track_path, 'rb') as f:
                            while True:
                                chunk = f.read(max_size)
                                if not chunk: break
                                part_path = temp_dir / f"{track_path.name}.{part_num:03d}"
                                with open(part_path, 'wb') as pf: pf.write(chunk)
                                part_caption = await generate_rich_caption(part_path, part_path.name)
                                await safe_send(
                                    upload_client, uid, final_chat_id, task_uuid, is_bot, upload_client.send_document,
                                    progress=progress, progress_args=["up", task_uuid],
                                    chat_id=final_chat_id, message_thread_id=upload_thread_id,
                                    document=str(part_path), thumb=str(thumb_path) if (thumb_path and thumb_path.exists()) else None,
                                    caption=part_caption
                                )
                                try: os.remove(part_path)
                                except Exception: pass
                                part_num += 1
                                await asyncio.sleep(1.5)
                        try: os.remove(track_path)
                        except Exception: pass
                    else:
                        extra_kw = {}
                        track_thumb = thumb_path
                        audio_meta = {}
                        
                        # 🟢 FORCE DOCUMENTS IF SELECTED IN UI
                        if upload_mode == "document" or not (is_audio or is_video):
                            caption_text = f"`{track_path.name}`"
                            send_fn = upload_client.send_document
                            doc_key = "document"
                        else:
                            caption_text = await generate_rich_caption(track_path, track_path.name)
                            if is_audio:
                                send_fn = upload_client.send_audio
                                doc_key = "audio"
                                audio_meta = await get_audio_metadata(track_path)
                                extra_kw.update({
                                    "duration": audio_meta.get("duration", 0),
                                    "performer": audio_meta.get("performer", "Unknown Artist"),
                                    "title": audio_meta.get("title", track_path.name)
                                })
                                if not track_thumb and audio_meta.get("thumb"):
                                    track_thumb = Path(audio_meta["thumb"])
                            elif is_video:
                                send_fn = upload_client.send_video
                                doc_key = "video"
                                extra_kw = {"supports_streaming": True}
                        
                        await safe_send(
                            upload_client, uid, final_chat_id, task_uuid, is_bot, send_fn,
                            progress=progress, progress_args=["up", task_uuid],
                            chat_id=final_chat_id, message_thread_id=upload_thread_id,
                            thumb=str(track_thumb) if track_thumb else None, 
                            caption=caption_text, **{doc_key: str(track_path)}, **extra_kw
                        )
                        
                        try: os.remove(track_path)
                        except Exception: pass
                        if audio_meta.get("thumb"):
                            try: os.remove(audio_meta["thumb"])
                            except Exception: pass
                        await asyncio.sleep(1.5)
                    
                try: await status_msg.delete()
                except Exception: pass
                await app.send_message(uid, f"✅ **Album/Archive Completed!**\nDelivered {total_tracks} tracks successfully to your selected destination.")
                
                EDITOR_UI_STATE[task_uuid]["done"] = True
                return  # Skip standard MKVToolNix remuxing

            # 🟢 REMUX OR BYPASS (Standard Video vs Audio)
            is_single_audio = str(new_name).lower().endswith(('.flac', '.mp3', '.m4a', '.wav', '.aac', '.opus', '.ogg', '.alac', '.mka', '.dsf', '.dff', '.ac3', '.eac3', '.dts'))

            # 🟢 FIX: TRACK EXTRACTION ENGINE (Rips selected tracks to standalone files!)
            if upload_mode in ["extract_audio", "extract_sub", "extract_video"]:
                EDITOR_UI_STATE[task_uuid]["phase"] = "Extracting Tracks"
                await safe_tg_edit(status_msg, f"⚙️ **Extracting Selected Tracks As-Is...**\n\n📄 `{new_name}`")
                
                extracted_files = []
                for track in config:
                    if track.get("type") in ["ext_audio", "ext_sub"]: continue 
                    
                    idx_str = str(track.get('index', '0'))
                    t_idx = idx_str.replace('v:', '').replace('a:', '').replace('s:', '')
                    t_type = track.get("type", "")
                    codec = track.get("codec", "").lower()
                    
                    if "v" in idx_str: t_type = "video"
                    elif "a" in idx_str: t_type = "audio"
                    elif "s" in idx_str: t_type = "subtitle"
                    
                    if upload_mode == "extract_audio" and t_type != "audio": continue
                    if upload_mode == "extract_sub" and t_type != "subtitle": continue
                    if upload_mode == "extract_video" and t_type != "video": continue
                    
                    # 🟢 FIX: 100% "As-Is" Raw Stream Mapping. Zero conversion.
                    if t_type == "audio":
                        ext = f".{codec}" if codec in ["aac", "ac3", "eac3", "flac", "mp3", "opus", "dts", "wav"] else ".mka"
                    elif t_type == "subtitle":
                        ext = ".srt" if codec == "subrip" else (".ass" if codec == "ass" else ".vtt")
                    else:
                        ext = ".mkv" # Safest native container for raw video chunks without transcoding
                        
                    out_name = f"Track_{t_idx}_{sanitize_filename(new_name)}{ext}"
                    out_path = temp_dir / out_name
                    
                    # -c copy ensures bit-for-bit extraction with no re-encoding
                    ex_cmd = ["ffmpeg", "-y", "-i", str(input_file), "-map", f"0:{t_idx}", "-c", "copy", str(out_path)]
                    proc = await asyncio.create_subprocess_exec(*ex_cmd, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL)
                    await proc.communicate()
                    
                    if out_path.exists(): extracted_files.append(out_path)
                
                if not extracted_files: 
                    raise Exception(f"No tracks matched your extraction choice ({upload_mode}).")
                    
                total_tracks = len(extracted_files)
                
                final_chat_id = uid if dest == "tg" else upload_chat_id
                uclient = USER_CLIENTS.get(uid)
                is_premium = False
                if uclient and uclient.is_connected:
                    try:
                        me = uclient.me or await uclient.get_me()
                        is_premium = getattr(me, "is_premium", False)
                    except: pass
                    
                for i, ex_file in enumerate(extracted_files, start=1):
                    EDITOR_UI_STATE[task_uuid]["phase"] = f"Uploading Track {i}/{total_tracks}"
                    await safe_tg_edit(status_msg, f"☁️ **Uploading Extracted Track {i} of {total_tracks}...**\n`{ex_file.name}`")
                    
                    if dest == "gofile":
                        url = await upload_to_gofile(str(ex_file))
                        await app.send_message(uid, f"✅ **Track {i} Extracted & Uploaded!**\n\n🔗 **GoFile Link:** {url}", disable_web_page_preview=True)
                        try: os.remove(ex_file)
                        except Exception: pass
                        continue

                    file_size = os.path.getsize(ex_file)
                    max_size = (3980 * 1024 * 1024) if is_premium else (1980 * 1024 * 1024)
                    
                    upload_client = app
                    is_bot = True

                    if file_size > (1980 * 1024 * 1024) and is_premium:
                        if uclient and getattr(uclient, "is_connected", False):
                            upload_client = uclient
                            is_bot = False
                    else:
                        stream_bots = USER_STREAM_BOTS.get(uid, [])
                        valid_bot = None
                        import random
                        shuffled_bots = list(stream_bots)
                        random.shuffle(shuffled_bots)
                        for b in shuffled_bots:
                            try:
                                if not getattr(b, "is_connected", False): await b.connect()
                                await b.get_chat(final_chat_id)
                                valid_bot = b
                                break
                            except: pass
                            
                        if valid_bot:
                            upload_client = valid_bot
                        else:
                            try:
                                await app.get_chat(final_chat_id)
                                upload_client = app
                            except:
                                if uclient and uclient.is_connected:
                                    upload_client = uclient
                                    is_bot = False

                    EDITOR_UI_STATE[task_uuid]["uploader"] = _lbl(upload_client)
                    
                    if file_size > max_size:
                        total_parts = math.ceil(file_size / max_size)
                        EDITOR_UI_STATE[task_uuid]["phase"] = f"Splitting Track {i} into {total_parts} parts"
                        part_num = 1
                        with open(ex_file, 'rb') as f:
                            while True:
                                chunk = f.read(max_size)
                                if not chunk: break
                                part_path = temp_dir / f"{ex_file.name}.{part_num:03d}"
                                with open(part_path, 'wb') as pf: pf.write(chunk)
                                part_caption = await generate_rich_caption(part_path, part_path.name)
                                await safe_send(
                                    upload_client, uid, final_chat_id, task_uuid, is_bot, upload_client.send_document,
                                    progress=progress, progress_args=["up", task_uuid],
                                    chat_id=final_chat_id, message_thread_id=upload_thread_id,
                                    document=str(part_path), thumb=str(thumb_path) if (thumb_path and thumb_path.exists()) else None,
                                    caption=part_caption
                                )
                                try: os.remove(part_path)
                                except Exception: pass
                                part_num += 1
                                await asyncio.sleep(1.5)
                        try: os.remove(ex_file)
                        except Exception: pass
                    else:
                        is_audio_file = str(ex_file).lower().endswith(('.flac', '.mp3', '.m4a', '.wav', '.aac', '.opus', '.ogg'))
                        if upload_mode == "extract_audio" and is_audio_file:
                            send_fn = upload_client.send_audio
                            doc_key = "audio"
                            audio_meta = await get_audio_metadata(ex_file)
                            extra_kwargs = {
                                "duration": audio_meta.get("duration", 0), "performer": audio_meta.get("performer", "Unknown Artist"),
                                "title": audio_meta.get("title", ex_file.name), "thumb": str(thumb_path) if (thumb_path and thumb_path.exists()) else audio_meta.get("thumb")
                            }
                        else:
                            send_fn = upload_client.send_document
                            doc_key = "document"
                            extra_kwargs = {"thumb": str(thumb_path) if (thumb_path and thumb_path.exists()) else None}
                            
                        cap = await generate_rich_caption(ex_file, ex_file.name)
                        await safe_send(upload_client, uid, final_chat_id, task_uuid, is_bot, send_fn, progress=progress, progress_args=["up", task_uuid], chat_id=final_chat_id, message_thread_id=upload_thread_id, caption=cap, **{doc_key: str(ex_file)}, **extra_kwargs)
                        try: os.remove(ex_file)
                        except Exception: pass
                    
                EDITOR_UI_STATE[task_uuid]["done"] = True
                await safe_tg_edit(status_msg, f"✅ **Extraction Completed!**\nDelivered {total_tracks} tracks.")
                return

            if is_single_audio:
                EDITOR_UI_STATE[task_uuid]["phase"] = "Processing Audio"
                await safe_tg_edit(status_msg, f"⚙️ **Processing Audio File (Preserving Tags)...**\n\n📄 `{new_name}`")
                
                # Re-apply cleaned global tags; empty values explicitly clear existing metadata fields.
                metadata_args = []
                for key, value in global_tags.items():
                    if re.fullmatch(r"[A-Za-z0-9_.-]+", key):
                        metadata_args.extend(["-metadata", f"{key}={clean_media_text(value)}"])
                if metadata_args:
                    ffmpeg_cmd = [
                        "ffmpeg", "-y", "-i", str(input_file),
                        "-c", "copy",
                        *metadata_args,
                        str(output_file)
                    ]
                    proc = await asyncio.create_subprocess_exec(*ffmpeg_cmd, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL)
                    await proc.communicate()
                else:
                    shutil.copy(str(input_file), str(output_file))
            else:
                EDITOR_UI_STATE[task_uuid]["phase"] = "Remuxing"
                await safe_tg_edit(status_msg, f"⚙️ **Remuxing Tracks (MKVToolNix)...**\n\n📄 `{new_name}`")
                await process_remux(str(input_file), str(output_file), config, global_tags)
            
            # 🟢 PRE-PROBE INTact MEDIA HERE (Before Zipping/Splitting)
            intact_media_info = None
            try:
                import json
                cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", str(output_file)]
                proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
                stdout, _ = await proc.communicate()
                intact_media_info = json.loads(stdout)
            except:
                pass
            
            # ZIP COMPRESSION
            if upload_mode == "zip":
                EDITOR_UI_STATE[task_uuid]["phase"] = "Zipping"
                await safe_tg_edit(status_msg, f"🗜 **Zipping Media...**\n\n📄 `{new_name}.zip`")
                zip_path = str(output_file) + ".zip"
                
                def create_stored_zip():
                    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_STORED) as zf:
                        zf.write(output_file, arcname=output_file.name)
                        
                await asyncio.to_thread(create_stored_zip)
                try: os.remove(output_file)
                except Exception: pass
                output_file = Path(zip_path)
                new_name = output_file.name

            if dest == "gofile":
                EDITOR_UI_STATE[task_uuid]["phase"] = "Uploading"
                await safe_tg_edit(status_msg, "☁️ **Uploading to GoFile...**")
                url = await upload_to_gofile(str(output_file))
                await status_msg.delete()
                await app.send_message(uid, f"✅ **Media Editor Completed!**\n\n🔗 **GoFile Link:** {url}", disable_web_page_preview=True)
            else:
                # 🟢 2. SMART UPLOAD ROUTING (Stream Bots -> Main Bot -> User)
                final_chat_id = uid if dest == "tg" else upload_chat_id
                
                uclient = USER_CLIENTS.get(uid)
                is_premium = False
                if uclient and uclient.is_connected:
                    try:
                        me = uclient.me or await uclient.get_me()
                        is_premium = getattr(me, "is_premium", False)
                    except: pass

                file_size = os.path.getsize(output_file)
                max_size = (3980 * 1024 * 1024) if is_premium else (1980 * 1024 * 1024)
                needs_split = file_size > max_size
                
                upload_client = app
                is_bot = True

                # 🟢 CRITICAL FIX: If ANY chunk is going to be >2GB, we absolutely MUST use the User Session!
                if file_size > (1980 * 1024 * 1024) and is_premium:
                    if uclient and getattr(uclient, "is_connected", False):
                        upload_client = uclient
                        is_bot = False
                else:
                    # 🟢 FIX: Bot Load Balancer (Prevents File Splits from Failing)
                    stream_bots = USER_STREAM_BOTS.get(uid, [])
                    valid_bot = None
                    import random
                    shuffled_bots = list(stream_bots)
                    random.shuffle(shuffled_bots)
                    for b in shuffled_bots:
                        try:
                            if not getattr(b, "is_connected", False): await b.connect()
                            await b.get_chat(final_chat_id)
                            valid_bot = b
                            break
                        except: pass
                        
                    if valid_bot:
                        upload_client = valid_bot
                    else:
                        try:
                            await app.get_chat(final_chat_id)
                            upload_client = app
                        except:
                            if uclient and uclient.is_connected:
                                upload_client = uclient
                                is_bot = False

                EDITOR_UI_STATE[task_uuid]["uploader"] = _lbl(upload_client)
                total_parts = math.ceil(file_size / max_size)
                final_thumb = str(thumb_path) if (thumb_path and thumb_path.exists()) else None

                # 🟢 3. MULTI-PART SPLIT UPLOAD
                if total_parts > 1:
                    EDITOR_UI_STATE[task_uuid]["phase"] = f"Splitting into {total_parts} parts"
                    await safe_tg_edit(status_msg, f"✂️ **Splitting into {total_parts} Parts...**\n({_pretty_bytes(file_size)})")
                    
                    part_num = 1
                    with open(output_file, 'rb') as f:
                        while True:
                            chunk = f.read(max_size)
                            if not chunk: break
                                
                            part_path = temp_dir / f"{new_name}.{part_num:03d}"
                            with open(part_path, 'wb') as pf: pf.write(chunk)
                                
                            EDITOR_UI_STATE[task_uuid]["phase"] = f"Uploading Part {part_num}/{total_parts}"
                            await safe_tg_edit(status_msg, f"☁️ **Uploading Part {part_num} of {total_parts}...**")
                            
                            # Generate rich caption for parts
                            part_caption = await generate_rich_caption(part_path, part_path.name, pre_probed_info=intact_media_info)
                            
                            await safe_send(
                                upload_client, uid, final_chat_id, task_uuid, is_bot, upload_client.send_document, 
                                progress=progress, progress_args=["up", task_uuid],
                                chat_id=final_chat_id, message_thread_id=upload_thread_id,
                                document=str(part_path), thumb=final_thumb,
                                caption=part_caption
                            )
                            try: os.remove(part_path)
                            except Exception: pass
                            part_num += 1
                            await asyncio.sleep(1.5)
                # 🟢 4. SINGLE FILE UPLOAD
                else:
                    EDITOR_UI_STATE[task_uuid]["phase"] = "Uploading"
                    await safe_tg_edit(status_msg, f"☁️ **Uploading Media...**\n*(Mode: {upload_mode.title()})*")
                    
                    # 🟢 THE FIX: Smart Routing for Audio vs Video with Native Metadata
                    is_video = str(output_file).lower().endswith(('.mp4', '.mkv', '.webm', '.avi', '.ts'))
                    is_audio = str(output_file).lower().endswith(('.flac', '.mp3', '.m4a', '.wav', '.aac', '.opus', '.ogg', '.alac', '.mka', '.dsf', '.dff', '.ac3', '.eac3', '.dts'))
                    
                    extra_kwargs = {}
                    track_thumb = final_thumb
                    audio_meta = {}

                    if upload_mode == "video":
                        if is_audio:
                            send_fn = upload_client.send_audio
                            doc_key = "audio"
                            audio_meta = await get_audio_metadata(output_file)
                            extra_kwargs.update({
                                "duration": audio_meta.get("duration", 0),
                                "performer": audio_meta.get("performer", "Unknown Artist"),
                                "title": audio_meta.get("title", output_file.name)
                            })
                            if not track_thumb and audio_meta.get("thumb"):
                                track_thumb = audio_meta["thumb"]
                        else:
                            send_fn = upload_client.send_video
                            doc_key = "video"
                            extra_kwargs = {"supports_streaming": True}
                    else:
                        send_fn = upload_client.send_document
                        doc_key = "document"
                    
                    # Generate rich caption for single file
                    final_caption = await generate_rich_caption(output_file, new_name, pre_probed_info=intact_media_info)
                        
                    await safe_send(
                        upload_client, uid, final_chat_id, task_uuid, is_bot, send_fn,
                        progress=progress, progress_args=["up", task_uuid],
                        chat_id=final_chat_id, message_thread_id=upload_thread_id,
                        thumb=str(track_thumb) if track_thumb else None, 
                        caption=final_caption, **{doc_key: str(output_file)}, **extra_kwargs
                    )
                    
                    if audio_meta.get("thumb"):
                        try: os.remove(audio_meta["thumb"])
                        except Exception: pass

                try: await status_msg.delete()
                except Exception: pass

                if str(final_chat_id) != str(uid):
                    await app.send_message(uid, f"✅ **Media Editor Completed!**\nFile `{new_name}` uploaded successfully.")
                    
            EDITOR_UI_STATE[task_uuid]["done"] = True
            log_file_result("editor", uid, task_uuid, "editor-input", None, new_name, "SUCCESS")
        except asyncio.CancelledError:
            # 🟢 Cleanly handle the kill signal
            EDITOR_UI_STATE[task_uuid]["phase"] = "Cancelled"
            EDITOR_UI_STATE[task_uuid]["error"] = "Cancelled by User"
            EDITOR_UI_STATE[task_uuid]["done"] = True
            log_file_result("editor", uid, task_uuid, "editor-input", None, new_name, "CANCELLED", "cancelled by user")
            try: await app.send_message(uid, f"🚫 **Task Cancelled:** `{new_name}`")
            except: pass
        except Exception as e:
            phase = EDITOR_UI_STATE.get(task_uuid, {}).get("phase", "unknown")
            EDITOR_UI_STATE[task_uuid]["phase"] = "Failed"
            EDITOR_UI_STATE[task_uuid]["error"] = str(e)
            EDITOR_UI_STATE[task_uuid]["done"] = True
            log_file_result("editor", uid, task_uuid, "editor-input", None, new_name, "FAILED", f"phase={phase}; {type(e).__name__}: {e}")
            logger.error(f"Media editor task {task_uuid} failed during {phase} for user {uid}: {e}", exc_info=True)
            try: await app.send_message(uid, f"❌ **Media Editor Failed:**\n`{str(e)}`")
            except: pass
        finally:
            shutil.rmtree(str(temp_dir), ignore_errors=True)
            EDITOR_ACTIVE_TASKS.pop(task_uuid, None) # Remove from active list
            
    # 🟢 Register the task so it can be cancelled
    task_obj = asyncio.create_task(background_editor())
    EDITOR_ACTIVE_TASKS[task_uuid] = {"task": task_obj, "user_id": uid}
    
    return web.json_response({"status": "success", "task_uuid": task_uuid})

# ==============================================================================
# --- PER-SITE COOKIES API ---
# ==============================================================================
async def _api_cookies_status(request):
    cookies_doc = await db.get_all_cookies()
    return web.json_response({
        "terabox": bool(cookies_doc.get("terabox")),
        "hxfile": bool(cookies_doc.get("hxfile")),
        "youtube": bool(cookies_doc.get("youtube"))
    })

def _get_cookie_filename(site):
    if site == "terabox": return "terabox.txt"
    if site == "hxfile": return "hxfile.txt"
    if site == "youtube": return "cookies.txt"
    return f"{site}.txt"

async def _api_cookies_upload(request):
    data = await request.post()
    site = data.get("site")
    file_field = data.get("file")
    if not site or not file_field:
        return web.Response(status=400, text="Missing site or file payload")

    content = file_field.file.read().decode("utf-8", errors="ignore")
    await db.save_cookie_file(site, content)

    filename = _get_cookie_filename(site)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    return web.json_response({"status": "success"})

async def _api_cookies_delete(request):
    data = await request.post()
    site = data.get("site")
    if not site:
        return web.Response(status=400, text="Missing site identifier")

    await db.delete_cookie_file(site)
    
    filename = _get_cookie_filename(site)
    import os
    if os.path.exists(filename):
        try: os.remove(filename)
        except Exception: pass

    return web.json_response({"status": "success"})

async def start_koyeb_health_check(host: str = "0.0.0.0"):
    if web is None: return
    global PORT
    
    # 🟢 FIX: 500MB Payload Limit for High-Res Audio/Thumbnails
    app_web = web.Application(
        client_max_size=1024**2 * 500,
        middlewares=[_api_diagnostics_middleware, _web_auth_middleware],
    )
    
    # Core & Dashboard
    app_web.router.add_get("/", _dashboard_ui_handler)
    app_web.router.add_get("/health", _dashboard_ui_handler)
    app_web.router.add_get("/manifest.json", _manifest_handler)
    app_web.router.add_get("/sw.js", _sw_handler)
    
    # Stats & Logs
    app_web.router.add_get("/api/stats", _api_stats_handler)
    app_web.router.add_get("/api/logs", _api_logs_handler)
    app_web.router.add_get("/api/logs/download", _api_download_log_handler)
    app_web.router.add_get("/api/network", _api_network_stats)
    app_web.router.add_get("/api/sos", _api_sos_handler)
    app_web.router.add_get("/api/speedtest", _api_speedtest_handler)
    
    # Auth & Settings
    app_web.router.add_post("/api/auth/login", _api_login_handler)
    app_web.router.add_post("/api/auth/forgot", _api_forgot_password_handler)
    app_web.router.add_post("/api/auth/reset", _api_reset_password_handler)
    app_web.router.add_post("/api/auth/logout", _api_logout_handler)
    app_web.router.add_post("/api/auth/stream-link", _api_stream_link_handler)
    app_web.router.add_post("/api/auth/password", _api_password_handler)
    app_web.router.add_get("/api/settings/tokens", _api_get_worker_tokens)
    app_web.router.add_post("/api/settings/tokens", _api_save_worker_tokens)
    
    # Telegram Connect
    app_web.router.add_post("/api/tg_qr/start", _api_tg_qr_start)
    app_web.router.add_get("/api/tg_qr/check", _api_tg_qr_check)
    app_web.router.add_post("/api/tg_qr/verify_2fa", _api_tg_qr_verify_2fa)
    app_web.router.add_post("/api/tg/send_code", _api_tg_send_code)
    app_web.router.add_post("/api/tg/verify", _api_tg_verify_code)
    app_web.router.add_post("/api/tg/verify_2fa", _api_tg_verify_2fa)
    app_web.router.add_post("/api/tg/logout", _api_tg_logout)
    
    # Media & Streams
    app_web.router.add_get("/api/chats", _api_chats_handler)
    app_web.router.add_get("/api/topics", _api_topics_handler)
    app_web.router.add_get("/api/cookies", _api_cookies_status)
    app_web.router.add_post("/api/cookies/upload", _api_cookies_upload)
    app_web.router.add_post("/api/cookies/delete", _api_cookies_delete)
    app_web.router.add_post("/api/mediainfo", _api_mediainfo_web_handler)
    app_web.router.add_post("/api/spectrogram", _api_spectrogram_web_handler)
    app_web.router.add_get("/api/media_probe", _api_media_probe_handler)
    app_web.router.add_get("/api/playlist", _api_playlist_handler)
    app_web.router.add_get("/api/stream", _api_stream_handler)
    app_web.router.add_get("/api/direct_stream", _api_direct_stream_handler)
    app_web.router.add_get("/api/tg_stream", _api_tg_stream_handler)
    app_web.router.add_get("/api/subtitles", _api_subtitles_handler)
    app_web.router.add_get("/api/cover", _api_cover_handler)
    
    # Tasks & Watchers
    app_web.router.add_post("/api/task/add", _api_add_task)
    app_web.router.add_post("/api/task/cancel", _api_cancel_task)
    app_web.router.add_post("/api/watcher/add", _api_add_watcher)
    app_web.router.add_post("/api/watcher/cancel", _api_cancel_watcher)
    
    # Editor & Proxies
    app_web.router.add_post("/api/edit_media", _api_edit_media_handler)
    app_web.router.add_get("/api/editor_progress", _api_editor_progress)
    app_web.router.add_get("/api/editor_active", _api_editor_active_tasks)
    app_web.router.add_post("/api/editor_cancel", _api_editor_cancel)
    app_web.router.add_get("/api/bg", _api_bg_proxy)
    app_web.router.add_get("/api/proxy/country", _api_proxy_country)
    app_web.router.add_get("/api/proxy/wiki", _api_proxy_wiki)
    app_web.router.add_get("/api/chat_details", _api_chat_details_handler)
    
    # Admin Controls API
    async def _api_admin_get_users(request):
        uid = request["authenticated_user_id"]
        if not await db.is_user_admin(uid):
            return web.json_response({"status": "error", "message": "Unauthorized"})
        
        effective_admins, effective_sudos, approved, _ = await db.get_access_control()
        
        # Consolidate users lowest-to-highest so highest privilege overwrites the dictionary
        users_dict = {}
        for x in approved: users_dict[x] = "User"
        for x in effective_sudos: users_dict[x] = "Sudo"
        for x in effective_admins: users_dict[x] = "Admin"
            
        user_data_list = []
        for a_id, role in users_dict.items():
            user_doc = await db.col.find_one({"id": a_id})
            name = user_doc.get("name", "Unknown User") if user_doc else "Unknown User"
            user_data_list.append({
                "id": a_id,
                "name": name,
                "role": role
            })
            
        return web.json_response({"status": "success", "users": user_data_list})

    async def _api_admin_add_user(request):
        data = await request.json()
        uid = int(data.get("user_id", 0))
        if not await db.is_user_admin(uid):
            return web.json_response({"status": "error", "message": "Unauthorized"})
        
        target = int(data.get("target_id", 0))
        role = data.get("role", "User")
        
        await db.add_approved_user(target, role)
        return web.json_response({"status": "success", "message": f"User {target} successfully assigned as {role}!"})

    async def _api_admin_remove_user(request):
        data = await request.json()
        uid = int(data.get("user_id", 0))
        if not await db.is_user_admin(uid):
            return web.json_response({"status": "error", "message": "Unauthorized"})
        target = int(data.get("target_id", 0))
        
        if target == uid:
            return web.json_response({"status": "error", "message": "You cannot remove yourself!"})
            
        await db.remove_user_access(target)
        return web.json_response({"status": "success", "message": f"User {target} removed!"})

    app_web.router.add_get("/api/admin/users", _api_admin_get_users)
    app_web.router.add_post("/api/admin/users/add", _api_admin_add_user)
    app_web.router.add_post("/api/admin/users/remove", _api_admin_remove_user)

    # Stop Media Task API
    async def _api_kill_stream(request):
        try:
            data = await request.json()
            uid = str(data.get("user_id", ""))
            
            if "GLOBAL_STREAM_TASKS" in globals() and uid:
                keys_to_delete = []
                for key, task in list(GLOBAL_STREAM_TASKS.items()):
                    if key.startswith(f"{uid}_"):
                        if not task.done():
                            task.cancel()
                        keys_to_delete.append(key)
                
                for k in keys_to_delete:
                    GLOBAL_STREAM_TASKS.pop(k, None)
                    
            return web.json_response({"status": "success", "message": "User streams killed cleanly."})
        except Exception as e:
            return web.json_response({"status": "error", "message": str(e)})

    app_web.router.add_post("/api/stream/kill", _api_kill_stream)
        
    # 🟢 FIX: 'access_log=None' officially kills the terminal web spam!
    runner = web.AppRunner(app_web, access_log=None) 
    await runner.setup()
    
    # 👇 CHANGE EXACTLY THIS LINE: Replace 'host' with '"0.0.0.0"'
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    
    await site.start()
    logger.info(f"🌐 Full-Stack Destiny TG Forwarder started on port {PORT}...")

# ==============================================================================
