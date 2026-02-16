# PhdLust - FINAL Fixed Version

import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON
from helper_func import encode


# =====================================================
# PRIVATE LINK GENERATOR (ADMIN ONLY)
# =====================================================
@Bot.on_message(filters.private & filters.user(ADMINS))
async def channel_post(client: Client, message: Message):

    # 🚫 BLOCK ALL COMMANDS HERE
    if message.text and message.text.startswith("/"):
        return

    reply_text = await message.reply_text("Please Wait...!", quote=True)

    # Copy message to database channel
    try:
        post_message = await message.copy(
            chat_id=client.db_channel.id,
            disable_notification=True
        )
    except FloodWait as e:
        await asyncio.sleep(e.value)
        post_message = await message.copy(
            chat_id=client.db_channel.id,
            disable_notification=True
        )
    except Exception as e:
        print(f"Copy Error: {e}")
        await reply_text.edit_text("Something went wrong!")
        return

    # Generate link
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"

    reply_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔁 Share URL",
                url=f"https://telegram.me/share/url?url={link}"
            )
        ]
    ])

    new_text = f"<b>Here is your link</b>\n\n{link}"

    try:
        await reply_text.edit_text(
            new_text,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    except Exception as e:
        if "MESSAGE_NOT_MODIFIED" not in str(e):
            print(f"Edit Error: {e}")

    # Add button to channel post
    if not DISABLE_CHANNEL_BUTTON:
        try:
            await post_message.edit_reply_markup(reply_markup)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await post_message.edit_reply_markup(reply_markup)
        except Exception:
            pass


# =====================================================
# AUTO BUTTON ADDER FOR NEW CHANNEL POSTS
# =====================================================
@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):

    if DISABLE_CHANNEL_BUTTON:
        return

    converted_id = message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"

    reply_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔁 Share URL",
                url=f"https://telegram.me/share/url?url={link}"
            )
        ]
    ])

    try:
        await message.edit_reply_markup(reply_markup)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await message.edit_reply_markup(reply_markup)
    except Exception:
        pass
