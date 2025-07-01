from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message":"FinWatch API is running"}