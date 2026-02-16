import time
import motor.motor_asyncio
from config import DB_URI, DB_NAME

# -------------------- DATABASE CONNECTION --------------------
dbclient = motor.motor_asyncio.AsyncIOMotorClient(DB_URI)
database = dbclient[DB_NAME]
user_data = database['users']

# -------------------- DEFAULT DICT --------------------
default_verify = {
    'is_verified': False,
    'verified_time': 0,
    'verify_token': "",
    'link': "",
    'first_start': 0
}

# -------------------- USER HELPERS --------------------
def new_user(user_id: int) -> dict:
    """
    Returns a new user document with default verify status
    """
    return {
        '_id': user_id,
        'verify_status': {
            'is_verified': False,
            'verified_time': 0,
            'verify_token': "",
            'link': "",
            'first_start': int(time.time())  # 3 HOURS TIMER START
        },
        'premium_status': {
            'is_premium': False,
            'expire_time': 0   # timestamp when premium expires, 0 for lifetime
        }
    }

async def present_user(user_id: int) -> bool:
    found = await user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    if not await present_user(user_id):
        user = new_user(user_id)
        await user_data.insert_one(user)

# -------------------- VERIFY STATUS --------------------
async def db_verify_status(user_id: int):
    user = await user_data.find_one({'_id': user_id})
    if user:
        return user.get('verify_status', default_verify)
    return default_verify

async def db_update_verify_status(user_id: int, verify: dict):
    await user_data.update_one(
        {'_id': user_id},
        {'$set': {'verify_status': verify}}
    )

# -------------------- FULL USERBASE --------------------
async def full_userbase():
    user_docs = user_data.find()
    return [doc['_id'] async for doc in user_docs]

# -------------------- DELETE USER --------------------
async def del_user(user_id: int):
    await user_data.delete_one({'_id': user_id})

# -------------------- PREMIUM SYSTEM --------------------

async def is_premium_user(user_id: int):
    user = await user_data.find_one({'_id': user_id})
    if not user:
        return False

    premium = user.get("premium_status", {})
    if not premium.get("is_premium", False):
        return False

    expire_time = premium.get("expire_time", 0)

    if expire_time == 0:
        return True

    if time.time() > expire_time:
        await user_data.update_one(
            {'_id': user_id},
            {'$set': {'premium_status.is_premium': False}}
        )
        return False

    return True


async def add_premium_user(user_id: int, duration: int = 0):
    expire_time = int(time.time()) + duration if duration > 0 else 0
    await user_data.update_one(
        {'_id': user_id},
        {'$set': {
            'premium_status.is_premium': True,
            'premium_status.expire_time': expire_time
        }}
    )


async def remove_premium_user(user_id: int):
    await user_data.update_one(
        {'_id': user_id},
        {'$set': {
            'premium_status.is_premium': False,
            'premium_status.expire_time': 0
        }}
    )
