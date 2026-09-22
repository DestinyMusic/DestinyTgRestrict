# -*- coding: utf-8 -*-
import os
import psutil
import time
import asyncio
import json
import uvloop

# --- 1. EVENT LOOP INITIALIZATION (FOR PYROFORK/WZGRAM) ---
uvloop.install()
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())
# ----------------------------------------------------------

# --- 2. BULLETPROOF KURIGRAM CRASH FIX ---
import pyrogram.enums
if not hasattr(pyrogram.enums, "ButtonStyle"):
    class DummyButtonStyle:
        DEFAULT = 0
    pyrogram.enums.ButtonStyle = DummyButtonStyle
# -----------------------------------------

import re
import shutil
import subprocess
import gc
import datetime
import uuid
from pathlib import Path
from collections import defaultdict, OrderedDict
import motor.motor_asyncio

from pyrogram import Client, filters, enums, idle
from pyrogram.raw.functions.messages import GetDialogs
from pyrogram.raw.types import InputPeerEmpty

# --- UNIVERSAL FORK & PYROMOD SUBSCRIPTABLE PATCH ---
# This bridges the gap between Pyromod's dictionary expectations 
# and modern Telegram forks' custom ListenerRegistry objects.
try:
    from pyrogram.dispatcher import ListenerRegistry
    
    if not hasattr(ListenerRegistry, "__getitem__"):
        def _reg_getitem(self, key):
            for attr in ["registry", "_registry", "data", "_data", "listeners"]:
                val = getattr(self, attr, None)
                if isinstance(val, dict):
                    return val[key]
            return getattr(self, key, {})
        ListenerRegistry.__getitem__ = _reg_getitem

    if not hasattr(ListenerRegistry, "__setitem__"):
        def _reg_setitem(self, key, value):
            for attr in ["registry", "_registry", "data", "_data", "listeners"]:
                val = getattr(self, attr, None)
                if isinstance(val, dict):
                    val[key] = value
                    return
            setattr(self, key, value)
        ListenerRegistry.__setitem__ = _reg_setitem

    if not hasattr(ListenerRegistry, "get"):
        def _reg_get(self, key, default=None):
            try:
                return self[key]
            except (KeyError, TypeError):
                return default
        ListenerRegistry.get = _reg_get
except ImportError:
    pass
# --------------------------------------------------

from pyrogram.errors import (
    FloodWait, UserIsBlocked, InputUserDeactivated, UserAlreadyParticipant,
    InviteHashExpired, UsernameNotOccupied, FileReferenceExpired, UserNotParticipant,
    ApiIdInvalid, PhoneNumberInvalid, PhoneCodeInvalid, PhoneCodeExpired,
    SessionPasswordNeeded, PasswordHashInvalid, PeerIdInvalid, AuthKeyUnregistered, UserDeactivated
)
from pyrogram import StopPropagation
from pyrogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton, Message, 
    BotCommand, BotCommandScopeDefault, BotCommandScopeChat, CallbackQuery
)
from concurrent.futures import ThreadPoolExecutor
import traceback                        
import html
import math
import aiohttp
from urllib.parse import unquote, urlparse, quote
import platform
import socket
import logging                          
from telegraph import Telegraph
from bson.objectid import ObjectId      # <-- REQUIRED FOR UNIQUE ROUTING
import speedtest                        # <-- REQUIRED FOR SPEEDTEST
import numpy as np
from scipy.io import wavfile
from scipy.signal import welch, stft
from PIL import Image, ImageDraw, ImageFont
from mutagen import File as MutagenFile
import base64

try:
    import pyloudnorm as pyln
    HAS_PYLN = True
except ImportError:
    HAS_PYLN = False

# --- MASTER LOGGING SETUP ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"), 
        logging.StreamHandler()                           
    ]
)
logger = logging.getLogger("BotLogger")

# 🟢 FIX: Completely silence the spammy Uvicorn/Aiohttp 200 OK access logs and Pyrogram's Ping/Session connection spam!
# Only actual Warnings and Errors will be printed from them now.
logging.getLogger("aiohttp.access").setLevel(logging.WARNING)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
# ----------------------------

# --- TELEGRAPH SETUP FOR MEDIAINFO ---
telegraph = Telegraph(domain="graph.org") # Bypasses Cloudflare Datacenter IP Blocks!

def load_telegraph_token():
    token_file = Path("./telegraph_token.txt")
    if token_file.exists():
        with open(token_file, "r") as f:
            return f.read().strip()
    try:
        response = telegraph.create_account(short_name='MediaInfoBot')
        token = response.get('access_token')
        if token:
            tmp = token_file.with_suffix(".tmp")
            with open(tmp, "w") as f:
                f.write(token)
            tmp.replace(token_file)
            return token
    except Exception as e:
        logger.error(f"[Telegraph] Failed to create account: {e}", exc_info=True)
    return None

saved_token = load_telegraph_token()
if saved_token:
    try:
        telegraph.access_token = saved_token
    except Exception:
        pass


# ------------------------------------------------------------------------------
# DestinyRestrict split loader
# The original script is intentionally executed in one shared global namespace.
# This keeps cross-section references, decorators, mutable state, and function
# lookup semantics equivalent to the original monolithic file.
# ------------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent

def _load_split_file(relative_path):
    path = BASE_DIR / relative_path
    source = path.read_text(encoding="utf-8")
    exec(compile(source, str(path), "exec"), globals(), globals())

_load_split_file("config.py")
_load_split_file("database/mongo.py")

# ==============================================================================
# --- CLIENT & GLOBAL STATE ---
# ==============================================================================

import inspect
import os

def get_transmission_kwargs(workers: int = 8, is_bot: bool = False) -> dict:
    """
    Dynamically detects fork support for concurrent transmissions.
    Strictly forces User Sessions to 1 to prevent MTProto Bufferbloat disconnects.
    """
    sig = inspect.signature(Client.__init__)
    if "max_concurrent_transmissions" not in sig.parameters:
        return {}

    # 🟢 CRITICAL FIX: User sessions MUST use 1 concurrent transmission
    if not is_bot:
        return {"max_concurrent_transmissions": 1}

    env_val = os.environ.get("MAX_CONCURRENT_TRANSMISSIONS", "").strip()
    if env_val.isdigit() and int(env_val) > 0:
        val = int(env_val)
    else:
        # 🟢 FIX: Cap transmissions independently from workers so sockets don't choke and timeout
        cpu_cores = os.cpu_count() or 2
        val = min(15, max(2, cpu_cores * 2))

    return {"max_concurrent_transmissions": val}

# 🟢 FIX: Scale Pyrogram workers down drastically if server lacks RAM
bot_workers = min(32, (_cpu_cores * 4) if _total_ram_gb < 1.0 else (_cpu_cores * 8))

app = Client(
    name="RestrictedBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=bot_workers,
    sleep_threshold=120, 
    ipv6=False,
    hide_password=True,        # 🟢 FIX: Keeps logs clean
    **get_transmission_kwargs(workers=bot_workers, is_bot=True) 
)

import random

REACTIONS = [
    "👍", "👎", "❤", "🔥", "🥰", "👏", "😁", "🤔", "🤯", "😱", 
    "🤬", "😢", "🎉", "🤩", "🤮", "💩", "🙏", "👌", "🕊", "🤡", 
    "🥱", "🥴", "😍", "🐳", "❤‍🔥", "🌚", "🌭", "💯", "🤣", "⚡", 
    "🍌", "🏆", "💔", "🤨", "😐", "🍓", "🍾", "💋", "🖕", "😈", 
    "😴", "😭", "🤓", "👻", "👨‍💻", "👀", "🎃", "🙈", "😇", "😨", 
    "🤝", "✍", "🤗", "🫡", "🎅", "🎄", "☃", "💅", "🤪", "🗿", 
    "🆒", "💘", "🙉", "🦄", "😘", "💊", "🙊", "😎", "👾", "🤷‍♂️", 
    "🤷", "🤷‍♀️", "😡"
]

ALL_COMMANDS = [
    "start", "help", "login", "logout", "dl", "watch", "unwatch", 
    "watchers", "cancel", "broadcast", "botstats", "status", 
    "log", "pixel", "sos", "mediainfo", "mi", "chats", "speedtest", "spectrogram", "spec"
]

@app.on_message(filters.command(ALL_COMMANDS), group=-1)
async def global_command_reactor(client: Client, message: Message):
    try:
        await message.react(emoji=random.choice(REACTIONS), big=True)
    except Exception as e:
        logger.debug(f"Reaction failed for msg {message.id}: {e}")

@app.on_message(filters.private | filters.group, group=-2)
async def access_control_guard(client: Client, message: Message):
    if message.from_user:
        user_id = message.from_user.id
    elif message.sender_chat:
        user_id = message.sender_chat.id
    else:
        return
        
    # 1. Stop if not approved for basic bot usage
    if not await db.is_user_approved(user_id):
        raise StopPropagation
        
    # 2. Dynamic Admin Shield: Prevent revoked admins from using Admin Commands
    if message.text and message.text.startswith("/"):
        cmd = message.text.split()[0].lower().strip("/")
        admin_cmds = ["log", "pixel", "speedtest", "status", "botstats", "sos", "broadcast", "spectrogram", "spec", "mi", "mediainfo"]
        if cmd in admin_cmds:
            if not await db.is_user_admin(user_id):
                raise StopPropagation

BOT_START_TIME = time.time()
WATCHER_LAST_RUN = {} # Tracks strict delays between live watcher messages
ACTIVE_PROCESSES = defaultdict(dict)  
CANCEL_FLAGS = {} 

def cleanup_task_memory(user_id, task_uuid):
    CANCEL_FLAGS.pop(task_uuid, None)
    if user_id in ACTIVE_PROCESSES:
        ACTIVE_PROCESSES[user_id].pop(task_uuid, None)
        if not ACTIVE_PROCESSES[user_id]:
            ACTIVE_PROCESSES.pop(user_id, None)

batch_temp = type("BT", (), {})()
batch_temp.ACTIVE_TASKS = defaultdict(int)
batch_temp.IS_BATCH = defaultdict(bool)
batch_temp.SKIP_IDS = defaultdict(set) # ALBUM BATCHING TRACKER
WATCHER_MEDIA_GROUPS = {}              # ALBUM WATCHER TRACKER
WATCHER_DEDUPE_CACHE = defaultdict(OrderedDict)  # bounded per-watcher event dedupe
WATCHER_DEDUPE_LIMIT = 2000

# 👇 NEW: Instant Memory Cache & Firewall Filter
GLOBAL_WATCHER_SOURCES = set() 

async def check_if_watched(_, __, message):
    return bool(message.chat and message.chat.id in GLOBAL_WATCHER_SOURCES)

is_watched_chat = filters.create(check_if_watched)
# 👆 END NEW

# 🟢 FIX: Apply the dynamic RAM-based limits to prevent server nukes
SERVER_UPLOAD_LIMIT = asyncio.Semaphore(int(os.environ.get("SERVER_UPLOAD_LIMIT", DYNAMIC_GLOBAL_UPLOADS))) 
USER_SEMAPHORE_LIMIT = DYNAMIC_USER_UPLOADS 
USER_SEMAPHORES = defaultdict(lambda: asyncio.Semaphore(USER_SEMAPHORE_LIMIT))
USER_DOWNLOAD_SEMAPHORES = defaultdict(lambda: asyncio.Semaphore(DYNAMIC_USER_UPLOADS))

from collections import defaultdict

class FloodController:
    def __init__(self):
        self.locked_until = 0

    async def wait_if_locked(self):
        now = time.time()
        if now < self.locked_until:
            wait_time = self.locked_until - now
            print(f"🚦 User Rate Limit! Task pausing for {wait_time:.1f}s.")
            await asyncio.sleep(wait_time)

    def set_lock(self, wait_seconds):
        unlock_time = time.time() + wait_seconds
        if unlock_time > self.locked_until:
            self.locked_until = unlock_time

USER_FLOOD_LOCKS = defaultdict(FloodController)

# --- PAUSE & WAIT INTERCEPTOR ---
from pyrogram.errors import ChatWriteForbidden, ChatAdminRequired, ChannelPrivate, UserBannedInChannel, PeerIdInvalid, FloodWait

BOT_WARNING_SENT = set() # Remembers if we already warned you about a broken destination

async def check_dest_access(client_to_use, dest_chat_id):
    """Silently tests if the client still has access to the destination."""
    if str(dest_chat_id).startswith("-"):
        try:
            await client_to_use.get_chat(dest_chat_id)
            return True
        except Exception:
            return False
    return True

async def wait_for_access(client_to_use, dest_chat_id, user_id, error_str, task_uuid=None):
    warning_msg = (
        f"🛑 **CRITICAL: User Session Disconnected!**\n\n"
        f"Task fully paused because your **User Session** ALSO lost Admin rights or was removed from the destination (`{dest_chat_id}`).\n"
        f"**Error:** `{error_str}`\n\n"
        f"🔄 **Action Required:** Please ensure your account has access and Admin rights in the destination. The task will resume automatically."
    )
    notify = None
    try: notify = await app.send_message(user_id, warning_msg)
    except: pass

    while True:
        if task_uuid and CANCEL_FLAGS.get(task_uuid): raise Exception("CANCELLED_BY_USER")
        if batch_temp.IS_BATCH.get(user_id): raise Exception("CANCELLED_BY_USER")
            
        await asyncio.sleep(10)
        if await check_dest_access(client_to_use, dest_chat_id): break 
            
    try:
        if notify: await notify.edit_text("✅ **User Session Access Restored! Resuming task...**")
    except: pass

async def safe_send(client_to_use, user_id, dest_chat_id, task_uuid, is_bot, coro_func, *args, **kwargs):
    """Wraps Pyrogram methods. Falls back to User Session if Bot fails. Pauses if User Session fails."""
    while True:
        try:
            res = await coro_func(*args, **kwargs)
            
            # If the Bot successfully sent it, check if we were previously broken.
            warning_key = f"{user_id}_{dest_chat_id}"
            if is_bot and warning_key in BOT_WARNING_SENT:
                BOT_WARNING_SENT.remove(warning_key) # Clear the warning flag
                try: await app.send_message(user_id, f"✅ **Bot Access Restored to `{dest_chat_id}`!**\nResuming high-speed Bot routing.")
                except: pass
                
            return res
            
        except Exception as e:
            if isinstance(e, FloodWait):
                raise e # Let FloodWaits be handled safely by the outer loops
                
            err_str = str(e)
            has_dest_access = await check_dest_access(client_to_use, dest_chat_id)
            
            # If we lost destination access, OR we got a write error (kicked/demoted)
            if not has_dest_access or isinstance(e, (ChatWriteForbidden, ChatAdminRequired, UserBannedInChannel)):
                if is_bot:
                    warning_key = f"{user_id}_{dest_chat_id}"
                    if warning_key not in BOT_WARNING_SENT:
                        msg = (f"⚠️ **Bot Removed or Demoted!**\n\n"
                               f"I lost Admin rights or was removed from `{dest_chat_id}`. I am smoothly falling back to your **User Session** to continue forwarding!\n\n"
                               f"🔄 **Note:** I will keep testing the Bot in the background. If you promote me back to Admin, I will instantly switch back to high-speed Bot routing.")
                        try: await app.send_message(user_id, msg)
                        except: pass
                        BOT_WARNING_SENT.add(warning_key)
                    # Bubble the error up so the main script immediately triggers the User Session Fallback!
                    raise e 
                else:
                    # The User Session ALSO failed. Now we must TRULY pause.
                    await wait_for_access(client_to_use, dest_chat_id, user_id, err_str, task_uuid)
                    continue
            else:
                # Source error (ChannelPrivate). Bubble up to User Session.
                raise e
# --------------------------------

PENDING_TASKS = {}
PROGRESS = {}
LAST_UI_EDIT = {}  # 🟢 NEW: Global UI Clock
SESSION_STRING_SIZE = 351

MAX_CONCURRENT_TASKS_PER_USER = int(os.environ.get("MAX_TASKS_PER_USER", "3"))
USER_CLIENTS = {}
ALL_MSG_TYPES = ["Video", "Document", "Text", "Audio", "Photo", "Voice", "Animation", "Sticker"]


_load_split_file("bot/utils.py")
_load_split_file("media/editor.py")
_load_split_file("bot/plugins/downloader.py")
_load_split_file("bot/plugins/admin.py")
_load_split_file("bot/plugins/watchers.py")
_load_split_file("core/batch_engine.py")
_load_split_file("core/router.py")
_load_split_file("streaming/direct_stream.py")
_load_split_file("media/probe.py")
_load_split_file("media/transcode.py")
_load_split_file("streaming/tg_stream.py")
_load_split_file("streaming/zip_engine.py")
_load_split_file("web/server.py")
_load_split_file("media/dsp_analyzer.py")
_load_split_file("core/live_engine.py")

# --- DASHBOARD UPDATER ---
# ==============================================================================
import datetime

# ==============================================================================
# --- MAIN ENTRY POINT ---
# ==============================================================================

INSTANCE_ID = uuid.uuid4().hex[:8]

async def cleanup_startup():
    folder = Path(f"./downloads_{INSTANCE_ID}")
    try:
        if folder.exists():
            shutil.rmtree(folder)
            logger.info(f"🧹 Startup: Cleared temporary downloads folder for {INSTANCE_ID}.")
    finally:
        folder.mkdir(parents=True, exist_ok=True)

# 👇 NEW: AUTO-WIPE DEAD SESSION HELPER
async def auto_wipe_dead_session(client, user_id):
    logger.error(f"🚨 Session dead for user {user_id}. Auto-wiping from database...")
    if client in USER_CLIENTS.values():
        USER_CLIENTS.pop(user_id, None)
    try: await client.stop()
    except Exception: pass
    
    await db.set_session(user_id, None)
    await db.set_api_id(user_id, None)
    await db.set_api_hash(user_id, None)
    
    user_tasks = list(ACTIVE_PROCESSES.get(user_id, {}).keys())
    for tid in user_tasks: CANCEL_FLAGS[tid] = True
    batch_temp.IS_BATCH[user_id] = True
    try: await db.db.active_tasks.delete_many({"user_id": user_id})
    except Exception: pass
# 👆 END NEW
    
async def main():
    global USER_CLIENTS
    
    await cleanup_startup()
    asyncio.create_task(cleanup_watchdog())
    logger.info("🛡️ Auto-Cleanup Watchdog Started") 

    # Attach the listener to the main bot so it functions without a User Session!
    app.add_handler(MessageHandler(user_watcher_handler, is_watched_chat))

    await app.start()
    logger.info("🤖 Bot Started") 
    
    logger.info("📝 Updating Bot Commands...")
    try:
        public_commands = [
            BotCommand("start", "⚡ Check if bot is alive"),
            BotCommand("help", "📚 View the detailed usage guide"),
            BotCommand("chats", "💬 List your chat & channel IDs"),
            BotCommand("dl", "📥 Download or forward from a link"),
            BotCommand("watch", "👀 Setup a live auto-forwarder"),
            BotCommand("watchers", "📋 List your active watchers"),
            BotCommand("unwatch", "🗑 Stop watching a source"),
            BotCommand("cancel", "🚫 Cancel an ongoing task"),
            BotCommand("login", "🔑 Login to your Telegram session"),
            BotCommand("logout", "🚪 Logout from your session")
        ]

        admin_commands = public_commands + [
            BotCommand("broadcast", "🗞 Broadcast a message to users"),
            BotCommand("botstats", "📊 Check detailed user & task stats"),
            BotCommand("status", "🖥 Check system RAM/CPU/Uptime"),
            BotCommand("log", "📄 Fetch backend bot logs"),
            BotCommand("pixel", "✨ Bypass Pixeldrain links"),
            BotCommand("sos", "⚙️ Deep System Statistics"),
            BotCommand("mediainfo", "🔍 Technical File MetaData"),
            BotCommand("speedtest", "🚀 Test Server Speed"),
            BotCommand("spectrogram", "📉 Audio Spectrogram")
        ]

        await app.set_bot_commands(public_commands, scope=BotCommandScopeDefault())

        all_admins = set(ADMINS + SUDOS)
        
        for admin_id in all_admins:
            try:
                await app.set_bot_commands(
                    admin_commands, 
                    scope=BotCommandScopeChat(chat_id=admin_id)
                )
            except Exception as e:
                logger.warning(f"⚠️ Could not set commands for Admin {admin_id}: {e}")
                
        logger.info("✅ Commands Updated: Public vs Admin scopes set!")
        
    except Exception as e:
        logger.error(f"⚠️ Failed to set commands: {e}", exc_info=True)
    
    logger.info("🔄 Loading Sessions for Active Watchers...")
    
    active_watcher_users = set()
    cursor = await db.get_all_watchers()
    async for w in cursor:
        active_watcher_users.add(w['user_id'])
        GLOBAL_WATCHER_SOURCES.add(w['source_id'])

    async def _init_single_watcher(user_id):
        user_session = await db.get_session(user_id)
        if not user_session or user_id in USER_CLIENTS:
            return
            
        try:
            logger.info(f"👤 Starting Watcher Session for: {user_id}")
            
            u_api = await db.get_api_id(user_id) or API_ID
            u_hash = await db.get_api_hash(user_id) or API_HASH
            
            user_client = Client(
                f"User_{user_id}", 
                session_string=user_session, 
                api_id=u_api, 
                api_hash=u_hash, 
                workers=100,
                ipv6=False,
                no_updates=False 
            )
            
            user_client.add_handler(MessageHandler(user_watcher_handler, is_watched_chat))
            
            await user_client.start()
            USER_CLIENTS[user_id] = user_client
            logger.info(f"✅ Active: {user_id}")
            
        except (AuthKeyUnregistered, UserDeactivated):
            logger.warning(f"❌ Session {user_id} was revoked. Auto-deleting...")
            await auto_wipe_dead_session(user_client, user_id)
        except Exception as e:
            logger.error(f"❌ Failed to load {user_id}: {e}")

    watcher_tasks = [_init_single_watcher(uid) for uid in active_watcher_users]
    if watcher_tasks:
        logger.info(f"⚡ Igniting {len(watcher_tasks)} watcher sessions concurrently...")
        await asyncio.gather(*watcher_tasks)

    logger.info(f"🔥 Total Live Listeners: {len(USER_CLIENTS)}")

    # Initialize per-user worker bots on startup
    await init_worker_bots()

    # Start the web health check
    asyncio.create_task(start_koyeb_health_check())
    
    # ==========================================
    # --- 🟢 WATCHER CATCH-UP ENGINE ---
    # ==========================================
    logger.info("🔄 Checking Watchers for missed messages (Catch-Up Engine)...")
    watcher_cursor = await db.get_all_watchers()
    async for w in watcher_cursor:
        wid = str(w["_id"])
        source_id = w["source_id"]
        source_thread = w.get("source_thread")
        last_processed = int(w.get("last_msg_id", 0) or 0)
        owner_id = w["user_id"]

        owner_client = USER_CLIENTS.get(owner_id)
        fetcher = owner_client if (owner_client and owner_client.is_connected) else app

        # Always start the worker, even when history is temporarily unavailable.
        await start_watcher_worker(wid)

        if last_processed <= 0:
            continue

        try:
            # IMPORTANT: do not manufacture every integer message ID. Telegram
            # message IDs can have gaps (deleted messages, service messages, etc.).
            # Queue actual messages returned by history, oldest first.
            missed = []
            async for m in fetcher.get_chat_history(source_id):
                if not m or m.empty:
                    continue
                if m.id <= last_processed:
                    break
                missed.append(m.id)

            if missed:
                missed.reverse()
                logger.info(
                    f"⚡ Watcher {wid} found {len(missed)} actual missed messages "
                    f"after ID {last_processed}. Queueing chronologically..."
                )
                for missing_id in missed:
                    await WATCHER_QUEUES[wid].put(int(missing_id))

        except Exception as e:
            logger.warning(f"Could not fetch history for Watcher Catch-up {wid}: {e}")

    # ==========================================
    # --- 🟢 BATCH AUTO-RESUME ENGINE ---
    # ==========================================
    logger.info("🔄 Checking database for interrupted batch tasks...")
    pending_tasks = await db.get_all_active_tasks()
    
    async def _resume_single_task(task):
        t_user_id = task["user_id"]
        t_uuid = task["task_uuid"]
        
        log_msg = (
            f"♻️ **AUTO-RESUME ACTIVATED!**\n"
            f"🤖 **User ID:** `{t_user_id}`\n"
            f"📁 **Source:** `{task.get('source_title', 'Unknown')}`\n"
            f"🎯 **Destination:** `{task.get('dest_title', 'Unknown')}`\n"
            f"▶️ **Resuming From ID:** `{task['current_msg_id']}`"
        )
        
        await send_log(log_msg)
        try:
            await app.send_message(t_user_id, log_msg)
        except Exception:
            pass
            
        asyncio.create_task(
            process_links_logic(
                client=app,
                message=None,
                text=task["link"],
                dest_chat_id=task["dest_chat_id"],
                dest_thread_id=task["dest_thread_id"],
                dest_title=task["dest_title"],
                delay=task["delay"],
                acc_user_id=t_user_id,
                task_uuid=t_uuid,
                is_restricted=task["is_restricted"],
                allowed_types=task["allowed_types"],
                resume_from_id=task["current_msg_id"],
                saved_source_title=task.get("source_title")
            )
        )
        logger.info(f"▶️ Auto-Resumed task {t_uuid} for User {t_user_id}")

    resuming_tasks = []
    async for task in pending_tasks:
        resuming_tasks.append(_resume_single_task(task))
        
    if resuming_tasks:
        await asyncio.gather(*resuming_tasks)

    await idle()
    
    await app.stop()
    for uid, client in USER_CLIENTS.items():
        try: await client.stop()
        except: pass
        
if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(main())
    except (KeyboardInterrupt, SystemExit):
        pass
