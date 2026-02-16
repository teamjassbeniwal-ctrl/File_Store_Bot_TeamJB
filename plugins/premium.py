import time
from pyrogram import filters
from bot import Bot
from config import ADMINS
from database.database import user_data


# ================================
# CHECK PREMIUM
# ================================
async def is_premium(user_id):
    user = await user_data.find_one({"_id": user_id})
    if not user:
        return False

    premium = user.get("premium_status", {})
    if not premium.get("is_premium"):
        return False

    expiry = premium.get("expiry", 0)

    if expiry == 0:
        return True  # lifetime

    if time.time() > expiry:
        await remove_premium(user_id)
        return False

    return True


# ================================
# ADD PREMIUM
# ================================
@Bot.on_message(filters.command("addpremium") & filters.user(ADMINS))
async def add_premium_cmd(client, message):

    try:
        user_id = int(message.command[1])
        plan = message.command[2].lower()
    except:
        return await message.reply(
            "Usage:\n"
            "/addpremium user_id 1m\n"
            "/addpremium user_id 3m\n"
            "/addpremium user_id lifetime"
        )

    plans = {
        "1m": ("1 Month", 30),
        "3m": ("3 Months", 90),
        "lifetime": ("Lifetime", 0)
    }

    if plan not in plans:
        return await message.reply("Invalid Plan!")

    plan_name, days = plans[plan]

    if days == 0:
        expiry = 0
    else:
        expiry = int(time.time()) + (days * 86400)

    await user_data.update_one(
        {"_id": user_id},
        {"$set": {
            "premium_status.is_premium": True,
            "premium_status.plan": plan_name,
            "premium_status.expiry": expiry
        }}
    )

    await message.reply(f"✅ Premium Activated\nPlan: {plan_name}")


# ================================
# REMOVE PREMIUM
# ================================
async def remove_premium(user_id):
    await user_data.update_one(
        {"_id": user_id},
        {"$set": {
            "premium_status.is_premium": False,
            "premium_status.plan": "",
            "premium_status.expiry": 0
        }}
    )


@Bot.on_message(filters.command("removepremium") & filters.user(ADMINS))
async def remove_premium_cmd(client, message):
    try:
        user_id = int(message.command[1])
    except:
        return await message.reply("Usage: /removepremium user_id")

    await remove_premium(user_id)
    await message.reply("❌ Premium Removed")


# ================================
# USER INFO
# ================================
@Bot.on_message(filters.command("userinfo") & filters.user(ADMINS))
async def user_info(client, message):

    try:
        user_id = int(message.command[1])
    except:
        return await message.reply("Usage: /userinfo user_id")

    user = await user_data.find_one({"_id": user_id})

    if not user:
        return await message.reply("User not found")

    premium = user.get("premium_status", {})

    if not premium.get("is_premium"):
        return await message.reply("User is FREE")

    expiry = premium.get("expiry")

    if expiry == 0:
        exp_text = "Lifetime"
    else:
        exp_text = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(expiry))

    await message.reply(
        f"👤 User: {user_id}\n"
        f"💎 Plan: {premium.get('plan')}\n"
        f"⏳ Expiry: {exp_text}"
  )
