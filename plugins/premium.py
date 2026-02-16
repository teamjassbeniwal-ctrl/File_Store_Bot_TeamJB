import time
from datetime import datetime
from pyrogram import filters
from pyrogram.enums import ParseMode
from bot import Bot
from config import ADMINS
from database.database import add_premium_user, remove_premium_user, is_premium_user

# ================================
# ADD PREMIUM
# ================================
@Bot.on_message(filters.command("addpremium") & filters.user(ADMINS))
async def add_premium(client, message):

    try:
        parts = message.text.split()
        user_id = int(parts[1])
        time_input = parts[2].lower()

        # ---- TIME CONVERT ----
        if time_input.endswith("d"):
            days = int(time_input[:-1])
            duration = days * 86400
            plan_text = f"{days} day"
        elif time_input.endswith("m"):
            months = int(time_input[:-1])
            duration = months * 30 * 86400
            plan_text = f"{months} month"
        else:
            return await message.reply("Use format: 7d or 1m")

        now = int(time.time())
        expire_time = now + duration

        # SAVE TO DATABASE
        await add_premium_user(user_id, duration)

        # DATE FORMAT
        join_date = datetime.fromtimestamp(now).strftime("%d-%m-%Y")
        join_time = datetime.fromtimestamp(now).strftime("%I:%M:%S %p")
        exp_date = datetime.fromtimestamp(expire_time).strftime("%d-%m-%Y")
        exp_time = datetime.fromtimestamp(expire_time).strftime("%I:%M:%S %p")

        user = await client.get_users(user_id)

        # ================= ADMIN MESSAGE =================
        await message.reply(
f"""ᴘʀᴇᴍɪᴜᴍ ᴀᴅᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ✅

👤 ᴜꜱᴇʀ : {user.first_name}
⚡ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>
⏰ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ : <code>{plan_text}</code>

⏳ ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ : {join_date}
⏱️ ᴊᴏɪɴɪɴɢ ᴛɪᴍᴇ : {join_time}

⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {exp_date}
⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : {exp_time}

Powered by Team JB
""",
            parse_mode=ParseMode.HTML
        )

        # ================= USER MESSAGE =================
        try:
            await client.send_message(
                user_id,
f"""👋 ʜᴇʏ {user.first_name},
ᴛʜᴀɴᴋ ʏᴏᴜ ꜰᴏʀ ᴘᴜʀᴄʜᴀꜱɪɴɢ ᴘʀᴇᴍɪᴜᴍ.
ᴇɴᴊᴏʏ !! ✨🎉

⏰ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ : <code>{plan_text}</code>
⏳ ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ : {join_date}
⏱️ ᴊᴏɪɴɪɴɢ ᴛɪᴍᴇ : {join_time}

⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {exp_date}
⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : {exp_time}
""",
                parse_mode=ParseMode.HTML
            )
        except:
            pass

    except:
        await message.reply("Usage:\n/addpremium user_id 7d")


# ================================
# REMOVE PREMIUM
# ================================
@Bot.on_message(filters.command("removepremium") & filters.user(ADMINS))
async def remove_premium_cmd(client, message):
    try:
        user_id = int(message.text.split()[1])
        await remove_premium_user(user_id)
        await message.reply("❌ Premium Removed Successfully!")
    except:
        await message.reply("Usage:\n/removepremium user_id")


# ================================
# MY PLAN
# ================================
@Bot.on_message(filters.command("myplan") & filters.private)
async def my_plan(client, message):

    user_id = message.from_user.id
    premium_check = await is_premium_user(user_id)

    # ❌ Not Premium
    if not premium_check:
        return await message.reply("🆓 You are using FREE plan.")

    # 🔹 Direct database se expire_time lo
    from database.database import user_data
    user = await user_data.find_one({'_id': user_id})
    expire_time = user.get("premium_status", {}).get("expire_time", 0)

    now = int(time.time())

    # ❌ Expired
    if expire_time != 0 and now > expire_time:
        await remove_premium_user(user_id)
        return await message.reply("🆓 Your premium expired.")

    # ✅ Active Premium
    remaining = expire_time - now

    days = remaining // 86400
    hours = (remaining % 86400) // 3600
    minutes = (remaining % 3600) // 60

    exp_date = datetime.fromtimestamp(expire_time).strftime("%d-%m-%Y")
    exp_time = datetime.fromtimestamp(expire_time).strftime("%I:%M:%S %p")

    await message.reply(
f"""⚜️ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀ ᴅᴀᴛᴀ :,

👤 ᴜꜱᴇʀ : {message.from_user.first_name}
⚡ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>
⏰ ᴛɪᴍᴇ ʟᴇꜰᴛ : {days} ᴅᴀʏꜱ, {hours} ʜᴏᴜʀꜱ, {minutes} ᴍɪɴᴜᴛᴇꜱ

⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {exp_date}
⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : {exp_time}
""",
        parse_mode=ParseMode.HTML
    )
# ================================
# PLANS
# ================================
@Bot.on_message(filters.command("plans") & filters.private)
async def plans_cmd(client, message):
    caption = """ᴀᴠᴀɪʟᴀʙʟᴇ ᴘʟᴀɴs  ♻️

• 𝟷 ᴡᴇᴇᴋ  -  ₹𝟹𝟶
• 𝟷 ᴍᴏɴᴛʜ  -  ₹𝟻𝟶
• 𝟹 ᴍᴏɴᴛʜs  -  ₹𝟷𝟶𝟶
• 𝟼 ᴍᴏɴᴛʜs  -  ₹18𝟶
• 12 ᴍᴏɴᴛʜs  -  ₹35𝟶

•─────•─────────•─────•
ᴘʀᴇᴍɪᴜᴍ ꜰᴇᴀᴛᴜʀᴇs  🎁

○ ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴠᴇʀɪꜰʏ
○ ᴅɪʀᴇᴄᴛ ꜰɪʟᴇs   
○ ᴀᴅ-ꜰʀᴇᴇ ᴇxᴘᴇʀɪᴇɴᴄᴇ 
○ ʜɪɢʜ-sᴘᴇᴇᴅ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ                         
○ ᴍᴜʟᴛɪ-ᴘʟᴀʏᴇʀ sᴛʀᴇᴀᴍɪɴɢ ʟɪɴᴋs                           
○ ᴜɴʟɪᴍɪᴛᴇᴅ files                                                                                                  
○ ʀᴇǫᴜᴇsᴛ ᴡɪʟʟ ʙᴇ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ɪɴ 𝟷ʜ
•─────•─────────•─────•

✨ ᴜᴘɪ ɪᴅ - yourupiid

ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴀᴄᴛɪᴠᴇ ᴘʟᴀɴ  /myplan

💢 ᴍᴜsᴛ sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴀꜰᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ

‼️ ᴀꜰᴛᴇʀ sᴇɴᴅɪɴɢ ᴀ sᴄʀᴇᴇɴsʜᴏᴛ ᴘʟᴇᴀsᴇ ɢɪᴠᴇ ᴍᴇ sᴏᴍᴇ ᴛɪᴍᴇ ᴛᴏ ᴀᴅᴅ ʏᴏᴜ ɪɴ ᴛʜᴇ ᴘʀᴇᴍɪᴜᴍ ᴠᴇʀsɪᴏɴ.

Message here @Team_JB
"""
buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📞 Contact Owner", url="https://t.me/TeamJB_bot")
            ],
            [
                InlineKeyboardButton("💳 Get QR Code", callback_data="show_qr")
            ]
        ]
    )

    await message.reply_photo(
        photo="https://i.ibb.co/PsqxZh2d/IMG-20251213-214014-515.jpg",  # your image file name
        caption=caption,
        reply_markup=buttons
    )


@app.on_callback_query(filters.regex("show_qr"))
async def show_qr(client, callback_query):

    await callback_query.message.reply_photo(
        photo="https://i.ibb.co/PsqxZh2d/IMG-20251213-214014-515.jpg",  # your QR image file
        caption="📲 Scan this QR and send payment screenshot."
    )

    await callback_query.answer()
