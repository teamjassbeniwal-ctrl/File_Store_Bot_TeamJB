from pyrogram import __version__
from pyrogram.errors import MessageNotModified
from bot import Bot
from config import OWNER_ID
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data

    if data == "about":
        await query.answer()

        about_text = (
            f"<b>○ Creator : <a href='tg://user?id={OWNER_ID}'>This Person</a>\n"
            f"○ Language : <code>Python3</code>\n"
            f"○ Library : <a href='https://docs.pyrogram.org/'>Pyrogram asyncio {__version__}</a>\n"
            f"○ Source Code : <a href='https://t.me/botsupdatesgroup'>Click here</a>\n"
            f"○ Channel : @teamjb1\n"
            f"○ Support Group : @botsupdatesgroup</b>"
        )

        buttons = InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔒 Close", callback_data="close")]]
        )

        try:
            # Prevent MESSAGE_NOT_MODIFIED error
            if query.message.text != about_text:
                await query.message.edit_text(
                    text=about_text,
                    disable_web_page_preview=True,
                    reply_markup=buttons
                )
        except MessageNotModified:
            pass
        except Exception as e:
            print(f"Callback Error: {e}")

    elif data == "close":
        await query.answer()

        try:
            await query.message.delete()
        except Exception:
            pass

        try:
            if query.message.reply_to_message:
                await query.message.reply_to_message.delete()
        except Exception:
            pass
