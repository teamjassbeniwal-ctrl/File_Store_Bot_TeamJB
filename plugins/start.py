import asyncio
import logging
import random
import string
import time
from datetime import datetime

from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import (
    ADMINS,
    FORCE_MSG,
    START_MSG,
    FORCE_PIC,
    WELCOME_PIC,
    CUSTOM_CAPTION,
    VERIFY_EXPIRE,
    SHORTLINK_API,
    SHORTLINK_URL,
    DISABLE_CHANNEL_BUTTON,
    PROTECT_CONTENT,
    AUTO_DELETE_TIME,
    AUTO_DELETE_MSG,
    TUT_VID,
    FREE_TIME
)
from helper_func import (
    subscribed,
    decode,
    get_messages,
    get_shortlink,
    get_verify_status,
    update_verify_status,
    delete_file
)
from database.database import (
    add_user,
    del_user,
    full_userbase,
    present_user,
    is_premium_user
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====================== START COMMAND ======================
# ====================== START COMMAND ======================
@Bot.on_message(filters.command("start") & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    now = int(time.time())

    # ---------- ADD USER ----------
    if not await present_user(user_id):
        await add_user(user_id)

    verify_status = await get_verify_status(user_id)
    first_start = verify_status.get("first_start") or now
    is_verified = verify_status.get("is_verified", False)
    verified_time = verify_status.get("verified_time", 0)

    # ---------- PREMIUM CHECK ----------
    premium_info = await is_premium_user(user_id)
    is_premium = premium_info.get("is_premium") if premium_info else False
    expire_time = premium_info.get("expire_time") if premium_info else 0

    # Premium users don't have free limit
    free_time_over = (now - first_start) >= FREE_TIME if not is_premium else False

    # ---------- EXPIRE VERIFICATION ----------
    if is_verified and (now - verified_time) >= VERIFY_EXPIRE:
        await update_verify_status(user_id, is_verified=False)
        is_verified = False

    # =========================================================
    # ================= VERIFY TOKEN CLICK =====================
    # =========================================================
    if message.text.startswith("/start verify_"):
        token = message.text.split("verify_", 1)[1]

        if verify_status.get("verify_token") != token:
            await message.reply("❌ Invalid or expired token.\nUse /start again.")
            return

        await update_verify_status(
            user_id,
            is_verified=True,
            verified_time=now
        )

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("ℹ️ About", callback_data="about"),
             InlineKeyboardButton("❌ Cancel", callback_data="close")]
        ])

        text = (
            f"✅ Verification successful!\n"
            f"🔓 Access unlocked for 8 hours.\n\n"
            f"Hello {message.from_user.first_name}\n\n"
            "I can store private files in Specified Channel "
            "and other users can access it from special link."
        )

        await message.reply_photo(
            photo=WELCOME_PIC,
            caption=text,
            reply_markup=buttons,
            quote=True
        )
        return

    # =========================================================
    # ================= PREMIUM USER ==========================
    # =========================================================
    if is_premium and (not message.command or len(message.command) == 1):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("ℹ️ About", callback_data="about"),
         InlineKeyboardButton("❌ Cancel", callback_data="close")]
    ])

    expire_text = (
        f"\n⌛ Expiry: "
        f"{datetime.fromtimestamp(expire_time).strftime('%d-%m-%Y %I:%M:%S %p')}"
        if expire_time else ""
    )

    text = (
        f"👋 Hey {message.from_user.first_name},\n"
        f"✨ Thank you for purchasing Premium!{expire_text}\n\n"
        f"{START_MSG.format(first=message.from_user.first_name)}"
    )

    await message.reply_photo(
        photo=WELCOME_PIC,
        caption=text,
        reply_markup=buttons,
        quote=True
    )
    return
    # ========================================================
    # ================= FREE TIME OVER ========================
    # =========================================================
    if free_time_over and not is_verified:
        token = "".join(random.choices(string.ascii_letters + string.digits, k=10))

        await update_verify_status(
            user_id,
            verify_token=token,
            is_verified=False
        )

        verify_link = f"https://t.me/{client.username}?start=verify_{token}"
        short_link = await get_shortlink(SHORTLINK_URL, SHORTLINK_API, verify_link)

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔓 Verify Now", url=short_link)],
            [InlineKeyboardButton("📖 How to Use", url=TUT_VID)]
        ])

        await message.reply(
            "⏰ Your FREE 3 HOURS are over.\n\n"
            "🔒 Please verify to continue using the bot for 8 hours.",
            reply_markup=buttons,
            quote=True
        )
        return

    # =========================================================
    # ================= FILE REQUEST ==========================
    # =========================================================
    if message.command and len(message.command) > 1:
        try:
            base64_string = message.text.split(" ", 1)[1]
            decoded = await decode(base64_string)
        except:
            return

        parts = decoded.split("-")

        if len(parts) == 3:
            start = int(int(parts[1]) / abs(client.db_channel.id))
            end = int(int(parts[2]) / abs(client.db_channel.id))
            ids = range(start, end + 1)
        elif len(parts) == 2:
            ids = [int(int(parts[1]) / abs(client.db_channel.id))]
        else:
            return

        wait = await message.reply("⏳ Processing...")
        messages = await get_messages(client, ids)
        await wait.delete()

        sent_msgs = []

        for msg in messages:
            caption = (
                CUSTOM_CAPTION.format(
                    previouscaption=msg.caption.html if msg.caption else "",
                    filename=msg.document.file_name
                )
                if CUSTOM_CAPTION and msg.document
                else (msg.caption.html if msg.caption else "")
            )

            reply_markup = msg.reply_markup if not DISABLE_CHANNEL_BUTTON else None

            try:
                sent = await msg.copy(
                    chat_id=user_id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                    protect_content=PROTECT_CONTENT
                )
                sent_msgs.append(sent)
                await asyncio.sleep(0.5)

            except FloodWait as e:
                await asyncio.sleep(e.x)
            except Exception as e:
                logger.error(e)

        if AUTO_DELETE_TIME > 0 and sent_msgs:
            info = await message.reply_text(
                AUTO_DELETE_MSG.format(time=AUTO_DELETE_TIME)
            )
            asyncio.create_task(delete_file(sent_msgs, client, info))

        return

    # =========================================================
    # ================= VERIFIED USER WELCOME =================
    # =========================================================
    if is_verified:
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("ℹ️ About", callback_data="about"),
             InlineKeyboardButton("❌ Cancel", callback_data="close")]
        ])

        text = (
            f"🔓 VERIFIED ACCESS ACTIVE (8 HOURS)\n\n"
            f"Hello {message.from_user.first_name}\n\n"
            "You can now access files without verification."
        )

        await message.reply_photo(
            photo=WELCOME_PIC,
            caption=text,
            reply_markup=buttons,
            quote=True
        )
        return

    # =========================================================
    # ================= FREE USER WELCOME =====================
    # =========================================================
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("ℹ️ About", callback_data="about"),
         InlineKeyboardButton("❌ Cancel", callback_data="close")]
    ])

    text = (
        f"🆓 FREE ACCESS ACTIVE (3 HOURS)\n\n"
        f"Hello {message.from_user.first_name}\n\n"
        "You can use this bot freely for 3 hours."
    )

    await message.reply_photo(
        photo=WELCOME_PIC,
        caption=text,
        reply_markup=buttons,
        quote=True
        )
    
# ====================== FORCE SUBSCRIBE ======================
@Bot.on_message(filters.command("start") & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔔 Join Channel", url=client.invitelink)]])
    await message.reply_photo(
        photo=FORCE_PIC,
        caption=FORCE_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username="@" + message.from_user.username if message.from_user.username else "",
            mention=message.from_user.mention,
            id=message.from_user.id
        ),
        reply_markup=buttons,
        quote=True
    )

# ====================== USERS COUNT ======================
@Bot.on_message(filters.command("users") & filters.private & filters.user(ADMINS))
async def users_count(client: Client, message: Message):
    users = await full_userbase()
    await message.reply(f"👥 Total users: {len(users)}")

# ====================== BROADCAST ======================
@Bot.on_message(filters.command("broadcast") & filters.private & filters.user(ADMINS))
async def broadcast(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply("Reply to a message to broadcast.")

    users = await full_userbase()
    success = failed = 0

    for user_id in users:
        try:
            await message.reply_to_message.copy(user_id)
            success += 1
        except (UserIsBlocked, InputUserDeactivated):
            await del_user(user_id)
            failed += 1
        except:
            failed += 1

    await message.reply(f"✅ Broadcast complete\n\nSuccess: {success}\nFailed: {failed}")
