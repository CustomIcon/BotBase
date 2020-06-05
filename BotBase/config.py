from pyrogram import InlineKeyboardMarkup, InlineKeyboardButton
from collections import defaultdict
from pyrogram import Filters
import re

# Antiflood module configuration

BAN_TIME = 300
MAX_UPDATE_THRESHOLD = 5
COUNT_CALLBACKS_SEPARATELY = False
PRIVATE_ONLY = True
FLOOD_PERCENTAGE = 75.0
ANTIFLOOD_SENSIBILITY = 1
FLOOD_NOTICE = f"🤙 **Hey dude**!\n🕐 Chill! You have been blocked for {BAN_TIME / 60:.1f} minutes"

# Various options and global variables

CACHE = defaultdict(lambda: ["none", 0])  # Caches user actions
RATELIMIT = 10
VERSION = "N/1"
RELEASE_DATE = "N/A"
CREDITS = "🧑‍💻 This bot was developed by @processare using Python 3.8 and Pyrogram 0.17.1" \
          "\n⚙️ **Version**: {VERSION}\n🗓 **Release Date**: {RELEASE_DATE}"

# Telegram client configuration

MODULE_NAME = "BotBase"
WORKERS_NUM = 15
BOT_TOKEN = ""
SESSION_NAME = "BotName"
PLUGINS_ROOT = {"root": f"{MODULE_NAME}/modules"}
API_ID = 123456
API_HASH = ""


# Logging configuration


LOGGING_FORMAT = f"[%(levelname)s %(asctime)s] In thread '%(threadName)s', module %(module)s, function %(funcName)s at line %(lineno)d -> [{SESSION_NAME}] %(message)s"
DATE_FORMAT = "%d/%m/%Y %H:%M:%S %p"
LOGGING_LEVEL = 30

# Start module

GREET = """👋 Hi {mention}! This bot was made with BotBase by @processare!"""
SUPPORT_BUTTON = "🆘 Request support"
CREDITS_BUTTON = "ℹ Credits"
BUTTONS = InlineKeyboardMarkup([
                                [InlineKeyboardButton(CREDITS_BUTTON, "info")],
                                [InlineKeyboardButton(SUPPORT_BUTTON, "sos")]
                               ]
                               )

# Database configuration

DB_RELPATH = f"{MODULE_NAME}/database/users.db"
DB_CREATE = """CREATE TABLE IF NOT EXISTS users(uuid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        tg_id INTEGER UNIQUE NOT NULL,
                        uname TEXT UNIQUE NULL DEFAULT 'null',
                        date TEXT NOT NULL,
                        admin INTEGER NOT NULL DEFAULT 0);
            """

DB_GET_USERS = "SELECT tg_id FROM users;"
DB_GET_USER = "SELECT * FROM users where users.tg_id = ?"
DB_SET_USER = "INSERT INTO users (uuid, tg_id, uname, date) VALUES(?, ?, ?, ?)"

# Admin module configuration

ADMINS = {123456: "admin name"}
BYPASS_FLOOD = False  # Do Admins bypass the antiflood?
# If you want the user to be notified of being flood-blocked, set this to the desired message
USER_INFO = "**ℹ️ User info**\n\n🆔 **User ID**: `{uid}`\n✍️ **Username**: {uname}\n🗓 Registered at: {date}\n**⌨️ Account Status**: {status}"
INVALID_SYNTAX = "❌ **Invalid syntax**"
ERROR = "❌ **Error**"
NONNUMERIC_ID = "The ID must be numeric!"
USERS_COUNT = "**Total # of users**: `{count}`"
NO_PARAMETERS = "<code>{command}</code> takes no parameters"
ID_MISSING = "The specified ID (<code>{uid}</code>) is not in the database"
GLOBAL_MESSAGE_STATS = "**Global message result**\n\n✍️** Message**: {msg}\n🔄 **# of send_message attempts**: {count}\n**✅ Successul attempts**: {success}"

# Livechat configuration

ADMINS_LIST_UPDATE_DELAY = 1
STATUSES = {admin_id: [admin_name, "free"] for (admin_id, admin_name) in ADMINS.items()}
LIVE_CHAT_STATUSES = "Statuses explanation : 🟢 = Available, 🔴 = Busy\n\n"
SUPPORT_NOTIFICATION = "🔔 There's a user requesting support! Press the button below to join the chat\n\n{uinfo}"
ADMIN_JOINS_CHAT = " [{admin_name}]({admin_id}) joins the chat! Remember to be kind and to use common sense"
USER_CLOSES_CHAT = "🔔 [{user_name}]({user_id}) has terminated the chat"
USER_LEAVES_CHAT = "✅ You've left the chat"
USER_JOINS_CHAT = "✅ You've joined the chat"
CHAT_BUSY = "⚠️ Another admin has already joined the chat"
LEAVE_CURRENT_CHAT = "⚠️ Leave the current chat first!"
STATUS_FREE = "🟢 "
STATUS_BUSY = "🔴"
SUPPORT_REQUEST_SENT = "✅ You're now in the queue, just wait for an admin to join the chat\n\n" \
                       "**🔄 Available admins**\n{queue}\n**Latest update**: {date}"
JOIN_CHAT_BUTTON = "❗ Join the chat"
USER_MESSAGE = "🗣 [{user_name}]({user_id}): {message}"
ADMIN_MESSAGE = "🧑‍💻 [{user_name}]({user_id}): {message}"
TOO_FAST = "✋ You're updating too fast! Chill and try later"

# Custom filters


def callback_regex(pattern: str):
    return Filters.create(lambda _, update: True if re.match(pattern, update.data) else False)


def admin_is_chatting():
    return Filters.create(lambda _, update: True if STATUSES[update.from_user.id][0] == "IN_CHAT" else False)


def user_is_chatting():
    return Filters.create(lambda _, update: True if CACHE[update.from_user.id][0] == "IN_CHAT" else False)
