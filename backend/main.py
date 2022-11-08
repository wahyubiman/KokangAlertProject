import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from app.scheduler import background_task

load_dotenv()
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
