from fastapi import FastAPI , Depends
from .api.routes import auth ,transaction
from .core.deps import get_current_user

app = FastAPI()

app.include_router(auth.router)
app.include_router(transaction.router)


@app.get("/")
def root():
    return {"message": "FinWatch API is running ✅"}

@app.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello, {current_user['email']}! 🔒 You are authenticated."}
