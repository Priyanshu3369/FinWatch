from fastapi import APIRouter, HTTPException, status
from ...schemas.user import UserCreate, UserLogin, UserOut
from ...services.auth_services import create_user, authenticate_user
from ...core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    user_id = await create_user(user)
    if not user_id:
        raise HTTPException(status_code=400, detail="User already exists")
    return {"id": user_id, "email": user.email, "is_active": True}

@router.post("/login")
async def login(user: UserLogin):
    auth_user = await authenticate_user(user.email, user.password)
    if not auth_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token({"sub": str(auth_user["_id"])})
    return {"access_token": access_token, "token_type": "bearer"}
