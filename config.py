# ==============================================================================
# --- CONFIGURATION ---
# ==============================================================================

import os
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

# Load the variables from .env or config.env file
load_dotenv() 

# --------------------------------------------------------------------------
# 🔴 COMPULSORY (Core Bot Credentials & Database)
# --------------------------------------------------------------------------
# The "or 0" and "or ''" prevent crashes if a variable is accidentally left blank
API_ID = int(os.environ.get("API_ID") or 0)
API_HASH = (os.environ.get("API_HASH") or "").strip()
BOT_TOKEN = (os.environ.get("BOT_TOKEN") or "").strip()

DB_URI = (os.environ.get("DB_URI") or "").strip()
DB_NAME = (os.environ.get("DB_NAME") or "").strip()

if not DB_URI:
    print("CRITICAL ERROR: DB_URI is empty! Please check your Render Environment Variables.")

# --------------------------------------------------------------------------
# 🟡 OPTIONAL: LOG CHANNEL
# --------------------------------------------------------------------------
_raw_log = (os.environ.get("LOG_CHANNEL") or "").strip()
if _raw_log:
    LOG_CHANNEL = _raw_log if "/" in _raw_log else (int(_raw_log) if _raw_log.replace("-", "").isdigit() else 0)
else:
    LOG_CHANNEL = 0

# --------------------------------------------------------------------------
# ⚙️ OPTIONAL: SETTINGS
# --------------------------------------------------------------------------
PORT = int(os.environ.get("PORT") or 8080)
LOGIN_SYSTEM = str(os.environ.get("LOGIN_SYSTEM", "True")).strip().lower() == "true"
ERROR_MESSAGE = str(os.environ.get("ERROR_MESSAGE", "True")).strip().lower() == "true"
WAITING_TIME = int(os.environ.get("WAITING_TIME") or 3)

# --------------------------------------------------------------------------
# 👥 ACCESS CONTROL (Comma-Separated User IDs)
# --------------------------------------------------------------------------
ADMINS = [int(x) for x in str(os.environ.get("ADMINS", "")).split(",") if x.strip().isdigit()]
SUDOS = [int(x) for x in str(os.environ.get("SUDOS", "")).split(",") if x.strip().isdigit()]

# --------------------------------------------------------------------------
# --- APPLICATION STATE & HARDWARE AUTO-TUNER ---
# --------------------------------------------------------------------------
# 🟢 FIX: Dynamically scan server hardware to set safe RAM/CPU limits!
_total_ram_gb = psutil.virtual_memory().total / (1024**3)
_cpu_cores = os.cpu_count() or 2

if _total_ram_gb <= 0.8:
    DYNAMIC_CHUNK_SIZE = 1 * 1024 * 1024      # 1MB chunks for Micro VPS (<1GB RAM)
    DYNAMIC_GLOBAL_UPLOADS = 5                # Max 5 active TCP connections
    DYNAMIC_USER_UPLOADS = 2
    DYNAMIC_CONCURRENCY = 2                   # Max 2 bots per stream
elif _total_ram_gb <= 2.5:
    DYNAMIC_CHUNK_SIZE = 3 * 1024 * 1024      # 3MB chunks for Medium (1-2GB RAM)
    DYNAMIC_GLOBAL_UPLOADS = 15
    DYNAMIC_USER_UPLOADS = 3
    DYNAMIC_CONCURRENCY = 4                   # Max 4 bots per stream
else:
    DYNAMIC_CHUNK_SIZE = 5 * 1024 * 1024      # 5MB chunks for High-End (>3GB RAM)
    DYNAMIC_GLOBAL_UPLOADS = 35
    DYNAMIC_USER_UPLOADS = 5
    DYNAMIC_CONCURRENCY = 8                   # Max 8 bots per stream

logger.info(f"⚙️ Auto-Tuner: {_total_ram_gb:.1f}GB RAM | {_cpu_cores} CPUs ➔ Chunks: {DYNAMIC_CHUNK_SIZE//1024//1024}MB | Max Streams: {DYNAMIC_GLOBAL_UPLOADS}")

TASK_QUEUE = defaultdict(list) 
io_executor = ThreadPoolExecutor(max_workers=min(32, _cpu_cores * 4))

HELP_TXT = """<b>📚 ULTIMATE BOT USAGE GUIDE</b>

Welcome! This bot helps you download restricted files and auto-forward messages. Here is everything you need to know:

▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬✘▬
<blockquote expandable>
<b>🟢 CORE COMMANDS</b>
• <code>/start</code> - <b>Wake Up & Welcome:</b> Greets you and registers your account.
• <code>/help</code> - <b>The Master Guide:</b> Opens this exact menu.
• <code>/cancel</code> - <b>Stop Everything:</b> Cleanly cancels any active setup process or massive downloading task.

<b>📥 DOWNLOADING & FORWARDING</b>
• <code>/dl</code> - <b>The Smart Downloader:</b> Manually downloads/copies media from a link. 
  ├ Reply to any Telegram link with <code>/dl</code>
  ├ Or type: <code>/dl https://t.me/channel/100</code>
  └ <i>Batch DL:</i> <code>/dl https://t.me/channel/101 - 120</code>

<b>🤖 DOWNLOADING FROM BOTS OR USER PMs</b>
To extract restricted files sent to you by other Bots or Users in Direct Messages:
1. Open the PM in Plus Messenger (or similar app) to get the Message ID.
2. Format the link using their username (without the @) and the message ID.
  ├ <b>Bot Example:</b> <code>/dl https://t.me/SaveRestrictedBot/150</code>
  └ <b>User Example:</b> <code>/dl https://t.me/JohnDoe/45</code>

<b>👀 LIVE AUTO-FORWARDER (WATCHERS)</b>
• <code>/watch</code> - <b>Set It and Forget It:</b> Auto-monitor a source and forward NEW messages instantly to your chosen destination.
  ├ <i>Channel:</i> <code>/watch https://t.me/channel/123</code>
  └ <i>Bot PM:</i> <code>/watch https://t.me/AnyBotUsername/123</code>
• <code>/watchers</code> - <b>Your Active List:</b> Interactive menu showing all your live monitors.
• <code>/unwatch</code> - <b>Turn Off a Watcher:</b> Instantly stops a specific monitor.
  └ <i>Usage:</i> <code>/unwatch SOURCE_ID</code> (Use the ID it comes <i>from</i>).

<b>🔑 ACCOUNT & SESSION</b>
• <code>/login</code> - <b>Link Your Account:</b> Securely connects your personal account session so the bot can bypass "Saving Restricted" limits and read your PMs.
• <code>/logout</code> - <b>Disconnect Safely:</b> Terminates your saved session and cleans up active watchers.
• <code>/chats</code> - <b>Chats & Channel Explorer:</b> Extract IDs of all your private chats, groups, channels, or bots with expandable quotes and filters.
</blockquote>
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬✘▬"""

ADMIN_HELP_TXT = """<b>🛠️ ADMIN & SYSTEM COMMANDS</b>

These commands are strictly reserved for Bot Admins and Sudo users.

▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬✘▬
<blockquote expandable>
<b>🖥 SYSTEM HEALTH</b>
• <code>/status</code> - <b>Health Check:</b> Quick dashboard of live RAM, CPU, free disk space, and active downloads.
• <code>/sos</code> - <b>Deep Server Stats:</b> Detailed report of OS, uptime, storage breakdown, and monthly bandwidth.
• <code>/botstats</code> - <b>User Tracker:</b> Displays total users, who is logged in, and live breakdown of their tasks.
• <code>/log</code> - <b>Backend Logs:</b> Sends the live <code>bot.log</code> file to troubleshoot errors.

<b>🧰 UTILITIES</b>
• <code>/pixel</code> - <b>Pixeldrain Bypasser:</b> Converts Pixeldrain links into high-speed CDN direct-download links.
  └ <i>Usage:</i> <code>/pixel https://pixeldrain.com/u/xxxx</code>
• <code>/mediainfo</code> (or <code>/mi</code>) - <b>Technical Inspector:</b> Analyzes a media file (by link or reply) and publishes a Telegraph report of codecs, bitrates, etc.
• <code>/broadcast</code> - <b>Mass Announcements:</b> Reply to a message with this to forward it to EVERY registered user.
</blockquote>
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬✘▬"""

