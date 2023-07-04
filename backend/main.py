import uvicorn
import os
from fastapi import FastAPI
from dotenv import load_dotenv
from app.scheduler import background_task
import sentry_sdk

# --- load .env
load_dotenv()

# ---- init sentry sdk
sentry_sdk.init(
    dsn=os.getenv("SENTRY_URL"),
    traces_sample_rate=1.0,
)

# --- init FastApi
app = FastAPI()

# --- FastAPI event handler


@app.on_event("startup")
async def startup():
    background_task()  # start APScheduler


@app.on_event("shutdown")
async def shutdown():
    pass


# --- router


@app.get("/")
async def index():
    return {"message": "Hello There"}


@app.get("/ping")
async def ping():
    return {"message": "pong"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
