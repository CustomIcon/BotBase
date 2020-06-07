from pyrogram import InlineKeyboardMarkup, InlineKeyboardButton
from collections import defaultdict
from pyrogram import Filters
import re
import os

# Antiflood module configuration
# The antiflood works by accumulating up to MAX_UPDATE_THRESHOLD updates (user-wise)
# and when that limit is reached, perform some checks to tell if the user is actually flooding


BAN_TIME = 300  # The amount of seconds the user will be banned
MAX_UPDATE_THRESHOLD = 5   # How many updates to accumulate before starting to count
COUNT_CALLBACKS_SEPARATELY = False   # If True, callback queries and messages will have their own separate flood counter
PRIVATE_ONLY = True    # If True, the antiflood will only work in private chats
# The percentage (from 0.0 to 100.0) of updates that when below ANTIFLOOD_SENSIBILITY will trigger the anti flood
# Example, if FLOOD_PERCENTAGE == 75, if at least 75% of the messages from a user are marked as flood it will be blocked
FLOOD_PERCENTAGE = 75.0
# The minimum amount of seconds between updates. Updates that are sent faster than this limit will trigger the antiflood
# This should not be below 1, but you can experiment if you feel bold enough
ANTIFLOOD_SENSIBILITY = 1
# If you want the user to be notified of being flood-blocked, set this to the desired message, False to disable
FLOOD_NOTICE = f"🤙 **Hey dude**!\n🕐 Chill! You have been blocked for {BAN_TIME / 60:.1f} minutes"

# Various options and global variables

CACHE = defaultdict(lambda: ["none", 0])  # Global cache. DO NOT TOUCH IT, really just don't
VERSION = "1.0A"   # These will be shown in the 'Credits' section
RELEASE_DATE = "N/A"
CREDITS = "🧑‍💻 This bot was developed by nocturn9x aka @processare using Python 3.8 and Pyrogram 0.17.1" \
          f"\n⚙️ **Version**: {VERSION}\n🗓 **Release Date**: {RELEASE_DATE}"

# Telegram client configuration

MODULE_NAME = "BotBase"   # The name of the FOLDER containing the modules directory
WORKERS_NUM = 15   # The number of worker threads that pyrogram will spawn at startup.
# 10 workers means that the bot will process up to 10 users at the same time and then block until one worker has done
BOT_TOKEN = "TOKEN"     # Get it with t.me/BotFather
SESSION_NAME = "BotName"   # The name of the Telegram Session that the bot will have, will be visible from Telegram
PLUGINS_ROOT = {"root": f"{MODULE_NAME}/modules"}   # Do not change this unless you know what you're doing
API_ID = 123456   # Get it at https://my.telegram.org/apps
API_HASH = "123456abcdef"      # Same as above


# Logging configuration
# To know more about what these options mean, check https://docs.python.org/3/library/logging.html

LOGGING_FORMAT = "[%(levelname)s %(asctime)s] In thread '%(threadName)s', " \
    f"module %(module)s, function %(funcName)s at line %(lineno)d -> [{SESSION_NAME}] %(message)s"
DATE_FORMAT = "%d/%m/%Y %H:%M:%S %p"
LOGGING_LEVEL = 30

# Start module
# P.S.: {mention} in the GREET message will be replaced with a mention to the user, same applies for {id} and {username}

GREET = """👋 Hi {mention} [`{id}`]! This bot was made with BotBase by @processare!"""  # The message that will be sent as a reply to the /start command. If this string is empty the bot will not reply
SUPPORT_BUTTON = "🆘 Request support"   # The text for the button that triggers the live chat
CREDITS_BUTTON = "ℹ Credits"   # The text for the 'Credits' button
BUTTONS = InlineKeyboardMarkup([     # This keyboard will be sent along with GREET, feel free to add or remove buttons
                                [InlineKeyboardButton(CREDITS_BUTTON, "info")],
                                [InlineKeyboardButton(SUPPORT_BUTTON, "sos")]
                               ]
                               )


# Database configuration
# The only natively supported database is SQLite3, but you can easily tweak
# this section and the BotBase/database/query.py to work with any DBMS
# If you do so and want to share your code feel free to open a PR on the repo!

DB_PATH = os.path.join(os.getcwd(), f"{MODULE_NAME}/database/database.db")
DB_CREATE = """CREATE TABLE IF NOT EXISTS users(
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        tg_id INTEGER UNIQUE NOT NULL,
                        uname TEXT UNIQUE NULL DEFAULT 'null',
                        date TEXT NOT NULL,
                        banned INTEGER NOT NULL DEFAULT 0);
            """

DB_GET_USERS = "SELECT tg_id FROM users"
DB_GET_USER = "SELECT * FROM users where users.tg_id = ?"
DB_SET_USER = "INSERT INTO users (id, tg_id, uname, date, banned) VALUES(?, ?, ?, ?, ?)"
DB_BAN_USER = "UPDATE users SET banned = 1 WHERE users.tg_id = ?"
DB_UNBAN_USER = "UPDATE users SET banned = 0 WHERE users.tg_id = ?"
DB_UPDATE_NAME = "UPDATE users SET uname = ? WHERE users.tg_id = ?"

# Admin module configuration


# Edit this dict adding the ID:NAME pair of the admin that you want to add. You can add as many admins as you want
ADMINS = {1234567: "name here"}
MARKED_BUSY = "🎲 Marked as busy. You won't receive any support notification until you send /busy again"
UNMARKED_BUSY = "✍ You are now receiving support notifications"
CANNOT_BAN_ADMIN = "❌ Operation not allowed, you can't ban/unban an admin!"
USER_BANNED = "✅ User has been banned"
USER_UNBANNED = "✅ User has been unbanned"
YOU_ARE_UNBANNED = "✅ You have been unbanned from the bot"
USER_NOT_BANNED = "❌ That user is not banned"
USER_ALREADY_BANNED = "❌ That user is already banned"
YOU_ARE_BANNED = "❌ You have been banned from the bot"
WHISPER_FROM = "📣 Incoming message from {admin}: {msg}"
NAME = "tg://user?id={}"
BYPASS_FLOOD = False  # If False, admins can be flood-blocked too, otherwise the antiflood will ignore them
USER_INFO_UPDATED = "✅ User info was correctly updated"
USER_INFO_UNCHANGED = "❌ The user's info hasn't changed"
USER_INFO = """**ℹ️ User info**

🆔 **User ID**: `{uid}`
✍️ **Username**: {uname}
🗓 Registered at: {date}
**⌨️ Banned**: {status}
**💡 Admin**: {admin}"""   # The message that is sent with /getuser and /getranduser
INVALID_SYNTAX = "❌ **Invalid syntax**"  # This is sent when a command is used the wrong way
ERROR = "❌ **Error**"   # This is sent when a command returns an error
NONNUMERIC_ID = "The ID must be numeric!"   # This is sent if the parameter to /getuser is not a numerical ID
USERS_COUNT = "**Total # of users**: `{count}`"   # This is sent as a result of the /count command
NO_PARAMETERS = "<code>{command}</code> takes no parameters"  # Error saying that the given command takes no parameters
ID_MISSING = "The specified ID (<code>{uid}</code>) is not in the database"  # Error when given ID is not in database
GLOBAL_MESSAGE_STATS = """**Global message result**

✍️** Message**: {msg}
🔄 **# of send_message attempts**: {count}
**✅ Successful attempts**: {success}"""  # Statistics that are sent to the admin after /global command

# Live chat configuration

ADMINS_LIST_UPDATE_DELAY = 30    # How many seconds between an update and another

# These strings are pretty self explanatory, aren't they?
LIVE_CHAT_STATUSES = "Statuses explanation : 🟢 = Available, 🔴 = Busy\n\n"
SUPPORT_NOTIFICATION = "🔔 There's a user requesting support! Press the button below to join the chat\n\n{uinfo}"
ADMIN_JOINS_CHAT = " [{admin_name}]({admin_id}) joins the chat! Remember to be kind and to use common sense"
USER_CLOSES_CHAT = "🔔 [{user_name}]({user_id}) has terminated the chat"
USER_LEAVES_CHAT = "✅ You've left the chat"
USER_JOINS_CHAT = "✅ You've joined the chat"
CHAT_BUSY = "⚠️ Another admin has already joined the chat"
LEAVE_CURRENT_CHAT = "⚠️ Leave the current chat first!"
STATUS_FREE = "🟢 "
STATUS_BUSY = "🔴 "
SUPPORT_REQUEST_SENT = "✅ You're now in the queue, just wait for an admin to join the chat\n\n" \
                       "**🔄 Available admins**\n{queue}\n**Latest update**: {date}"
JOIN_CHAT_BUTTON = "❗ Join the chat"
USER_MESSAGE = "🗣 [{user_name}]({user_id}): {message}"
ADMIN_MESSAGE = "🧑‍💻 [{user_name}]({user_id}): {message}"
TOO_FAST = "✋ You're updating too fast! Chill and try later"

# Custom filters  - Don't touch them as well but feel free to add more!


def callback_regex(pattern: str):
    return Filters.create(lambda _, update: True if re.match(pattern, update.data) else False)


def admin_is_chatting():
    return Filters.create(lambda _, update: True if update.from_user.id in ADMINS and CACHE[update.from_user.id][0] == "IN_CHAT" else False)


def user_is_chatting():
    return Filters.create(lambda _, update: True if update.from_user.id not in ADMINS and CACHE[update.from_user.id][0] == "IN_CHAT" else False)
