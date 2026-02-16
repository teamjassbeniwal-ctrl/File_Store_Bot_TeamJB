from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
import asyncio

from bot import Bot
from config import ADMINS
from helper_func import encode, get_message_id


# =====================================================
# BATCH LINK GENERATOR
# =====================================================
@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command("batch"))
async def batch(client: Client, message: Message):

    # Ask First Message
    try:
        first_message = await client.ask(
            chat_id=message.from_user.id,
            text="Forward the First Message from DB Channel (with Quotes)\n\nor Send the DB Channel Post Link",
            filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
            timeout=60
        )
    except Exception:
        return

    f_msg_id = await get_message_id(client, first_message)

    if not f_msg_id:
        await first_message.reply_text(
            "❌ Error\n\nThis forwarded post is not from my DB Channel.",
            quote=True
        )
        return


    # Ask Last Message
    try:
        second_message = await client.ask(
            chat_id=message.from_user.id,
            text="Forward the Last Message from DB Channel (with Quotes)\n\nor Send the DB Channel Post Link",
            filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
            timeout=60
        )
    except Exception:
        return

    s_msg_id = await get_message_id(client, second_message)

    if not s_msg_id:
        await second_message.reply_text(
            "❌ Error\n\nThis forwarded post is not from my DB Channel.",
            quote=True
        )
        return


    # Generate Batch Link
    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
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

    await second_message.reply_text(
        f"<b>Here is your Batch Link</b>\n\n{link}",
        quote=True,
        reply_markup=reply_markup
    )


# =====================================================
# SINGLE LINK GENERATOR
# =====================================================
@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command("genlink"))
async def link_generator(client: Client, message: Message):

    try:
        channel_message = await client.ask(
            chat_id=message.from_user.id,
            text="Forward Message from DB Channel (with Quotes)\n\nor Send the DB Channel Post Link",
            filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
            timeout=60
        )
    except Exception:
        return

    msg_id = await get_message_id(client, channel_message)

    if not msg_id:
        await channel_message.reply_text(
            "❌ Error\n\nThis forwarded post is not from my DB Channel.",
            quote=True
        )
        return

    base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
    link = f"https://t.me/{client.username}?start={base64_string}"

    reply_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔁 Share URL",
                url=f"https://telegram.me/share/url?url={link}"
            )
        ]
    ])

    await channel_message.reply_text(
        f"<b>Here is your Link</b>\n\n{link}",
        quote=True,
        reply_markup=reply_markup
    )
