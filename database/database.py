import time
import motor.motor_asyncio
from config import DB_URI, DB_NAME

dbclient = motor.motor_asyncio.AsyncIOMotorClient(DB_URI)
database = dbclient[DB_NAME]

user_data = database['users']

default_verify = {
    'is_verified': False,
    'verified_time': 0,
    'verify_token': "",
    'link': "",
    'first_start': 0
}

def new_user(user_id):
    return {
        "_id": user_id,

        "verify_status": {
            "is_verified": False,
            "verified_time": 0,
            "verify_token": "",
            "first_start": int(time.time())
        },

        "premium_status": {
            "is_premium": False,
            "plan": "",
            "expiry": 0
        }
    }
    
async def present_user(user_id: int):
    found = await user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user = new_user(user_id)
    await user_data.insert_one(user)

async def db_verify_status(user_id: int):
    user = await user_data.find_one({'_id': user_id})
    if user:
        return user.get('verify_status', default_verify)
    return default_verify

async def db_update_verify_status(user_id: int, verify):
    await user_data.update_one(
        {'_id': user_id},
        {'$set': {'verify_status': verify}}
    )

async def full_userbase():
    user_docs = user_data.find()
    return [doc['_id'] async for doc in user_docs]

async def del_user(user_id: int):
    await user_data.delete_one({'_id': user_id})
