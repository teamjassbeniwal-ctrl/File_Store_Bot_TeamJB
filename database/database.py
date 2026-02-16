# database.py - Safe Upgrade Version
import time
import motor.motor_asyncio
from config import DB_URI, DB_NAME

# -------------------- DATABASE CONNECTION --------------------
dbclient = motor.motor_asyncio.AsyncIOMotorClient(DB_URI)
database = dbclient[DB_NAME]
user_data = database['users']

# -------------------- DEFAULT DICTS --------------------
default_verify = {
    'is_verified': False,
    'verified_time': 0,
    'verify_token': "",
    'link': "",
    'first_start': 0
}

default_premium = {
    'is_premium': False,
    'plan': "",
    'expiry': 0
}

# -------------------- USER HELPERS --------------------
def new_user(user_id: int) -> dict:
    """
    Returns a new user document with default verify and premium statuses
    """
    return {
        "_id": user_id,
        "verify_status": default_verify.copy(),
        "premium_status": default_premium.copy()
    }

async def present_user(user_id: int) -> bool:
    """
    Returns True if user exists in DB, else False
    """
    user = await user_data.find_one({"_id": user_id})
    return bool(user)

async def add_user(user_id: int):
    """
    Add user to DB if not already present
    """
    if not await present_user(user_id):
        user = new_user(user_id)
        await user_data.insert_one(user)

async def del_user(user_id: int):
    """
    Delete user from DB
    """
    await user_data.delete_one({"_id": user_id})

async def full_userbase() -> list:
    """
    Returns a list of all user IDs
    """
    cursor = user_data.find()
    return [doc["_id"] async for doc in cursor]

# -------------------- VERIFY STATUS --------------------
async def get_verify_status(user_id: int) -> dict:
    """
    Returns verify_status of the user. Returns default if missing.
    """
    user = await user_data.find_one({"_id": user_id})
    if user:
        verify = user.get("verify_status", default_verify.copy())
        # Ensure all keys exist
        for key, val in default_verify.items():
            verify.setdefault(key, val)
        return verify
    return default_verify.copy()

async def update_verify_status(user_id: int, **kwargs):
    """
    Update verify_status fields for a user.
    """
    await add_user(user_id)  # ensure user exists
    await user_data.update_one(
        {"_id": user_id},
        {"$set": {f"verify_status.{k}": v for k, v in kwargs.items()}},
        upsert=True
    )

# -------------------- PREMIUM STATUS --------------------
async def get_premium(user_id: int) -> dict:
    """
    Returns premium_status of the user. Returns default if missing.
    """
    user = await user_data.find_one({"_id": user_id})
    if user:
        premium = user.get("premium_status", default_premium.copy())
        # Ensure all keys exist
        for key, val in default_premium.items():
            premium.setdefault(key, val)
        return premium
    return default_premium.copy()

async def set_premium(user_id: int, is_premium: bool, plan: str = "", expiry: int = 0):
    """
    Set premium_status for a user. Creates user if missing.
    """
    await add_user(user_id)
    await user_data.update_one(
        {"_id": user_id},
        {"$set": {
            "premium_status.is_premium": is_premium,
            "premium_status.plan": plan,
            "premium_status.expiry": expiry
        }},
        upsert=True
    )

async def is_premium(user_id: int) -> bool:
    """
    Returns True if the user has active premium
    """
    premium = await get_premium(user_id)
    return premium.get("is_premium", False) and premium.get("expiry", 0) > int(time.time())
