from fastapi import FastAPI , Depends
from .api.routes import auth ,transaction
from .core.deps import get_current_user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(transaction.router)

@app.get("/")
def root():
    return {"message": "FinWatch API is running ✅"}

@app.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello, {current_user['email']}! 🔒 You are authenticated."}
