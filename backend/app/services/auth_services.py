from passlib.context import CryptContext
from ..db.mongo import db
from bson import ObjectId
from ..core.security import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_user(user_data):
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        return None
    hashed_pw = pwd_context.hash(user_data.password)
    new_user = {
        "email": user_data.email,
        "hashed_password": hashed_pw,
        "is_active": True
    }
    result = await db.users.insert_one(new_user)
    return str(result.inserted_id)

async def authenticate_user(email: str, password: str):
    user = await db.users.find_one({"email": email})
    if user and pwd_context.verify(password, user["hashed_password"]):
        return user
    return None

async def get_user_by_email(email: str):
    return await db.users.find_one({"email": email})
