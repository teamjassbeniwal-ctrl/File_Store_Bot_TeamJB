import time
from pyrogram import filters
from bot import Bot
from config import ADMINS
from database.database import user_data


# =========================================
# CHECK PREMIUM
# =========================================
async def is_premium(user_id: int):
    user = await user_data.find_one({"_id": user_id})

    if not user:
        return False

    premium = user.get("premium_status", {})

    if premium.get("is_premium") and premium.get("expiry", 0) > int(time.time()):
        return True

    return False


# =========================================
# ADD PREMIUM (ADMIN)
# =========================================
@Bot.on_message(filters.command("addpremium") & filters.private & filters.user(ADMINS))
async def add_premium(client, message):

    if len(message.command) != 3:
        return await message.reply(
            "Usage:\n/addpremium user_id time\nExample:\n/addpremium 123456789 1d"
        )

    user_id = int(message.command[1])
    time_text = message.command[2]

    if time_text.endswith("m"):
        seconds = int(time_text[:-1]) * 60
    elif time_text.endswith("h"):
        seconds = int(time_text[:-1]) * 3600
    elif time_text.endswith("d"):
        seconds = int(time_text[:-1]) * 86400
    else:
        return await message.reply("Use m (minutes), h (hours), d (days)")

    expiry = int(time.time()) + seconds

    await user_data.update_one(
        {"_id": user_id},
        {"$set": {
            "premium_status.is_premium": True,
            "premium_status.plan": time_text,
            "premium_status.expiry": expiry
        }},
        upsert=True
    )

    await message.reply(f"✅ Premium added to {user_id} for {time_text}")


# =========================================
# REMOVE PREMIUM (ADMIN)
# =========================================
@Bot.on_message(filters.command("removepremium") & filters.private & filters.user(ADMINS))
async def remove_premium(client, message):

    if len(message.command) != 2:
        return await message.reply("Usage:\n/removepremium user_id")

    user_id = int(message.command[1])

    await user_data.update_one(
        {"_id": user_id},
        {"$set": {
            "premium_status.is_premium": False,
            "premium_status.plan": "",
            "premium_status.expiry": 0
        }}
    )

    await message.reply(f"❌ Premium removed from {user_id}")


# =========================================
# MY PLAN (USER)
# =========================================
@Bot.on_message(filters.command("myplan") & filters.private)
async def my_plan(client, message):

    user_id = message.from_user.id
    user = await user_data.find_one({"_id": user_id})

    if not user:
        return await message.reply("❌ No data found.")

    premium = user.get("premium_status", {})

    if not premium.get("is_premium"):
        return await message.reply("❌ You don't have Premium.")

    expiry = premium.get("expiry", 0)
    remaining = expiry - int(time.time())

    if remaining <= 0:
        return await message.reply("❌ Your Premium expired.")

    hours = remaining // 3600
    minutes = (remaining % 3600) // 60

    await message.reply(
        f"💎 Premium Active\n\n"
        f"Plan: {premium.get('plan')}\n"
        f"Remaining: {hours}h {minutes}m"
    )
