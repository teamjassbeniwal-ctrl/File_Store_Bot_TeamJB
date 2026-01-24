"""Get full user details
Syntax: /id
"""

from pyrogram import filters
from pyrogram.types import Message
from bot import Bot


@Bot.on_message(filters.command("id") & filters.private)
async def showid(client: Bot, message: Message):
    user = message.from_user

    first_name = user.first_name or "None"
    last_name = user.last_name or "None"
    user_id = user.id
    username = f"@{user.username}" if user.username else "None"
    user_link = user.mention
    is_premium = user.is_premium or False
    language_code = user.language_code or "None"

    try:
        status = user.status.name.replace("_", " ").title()
    except:
        status = "Unknown"

    text = (
        "<b>User Details :</b>\n\n"
        f"🦚 <b>First Name :</b> {first_name}\n\n"
        f"🐧 <b>Last Name :</b> {last_name}\n\n"
        f"👤 <b>User Id :</b> <code>{user_id}</code>\n\n"
        f"👦 <b>Username :</b> {username}\n\n"
        f"🔗 <b>User Link :</b> {user_link}\n\n"
        f"🌟 <b>Telegram Premium :</b> {is_premium}\n\n"
        f"📃 <b>Language Code :</b> {language_code}\n\n"
        f"💫 <b>Status :</b> {status}\n\n"
        "<i>If you need user id, Then just tap and copy.</i>"
    )

    await message.reply_text(text, quote=True)
