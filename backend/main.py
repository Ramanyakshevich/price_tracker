from contextlib import asynccontextmanager
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.config import settings
from core.database import AsyncSessionLocal
from api.routers import router
from services.checker import check_prices

scheduler = AsyncIOScheduler()

async def scheduler_check():
    async with AsyncSessionLocal() as session:
        await check_prices(session)

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.add_job(scheduler_check, "interval", minutes=1)
    scheduler.start()
    print("APScheduler started")

    yield

    scheduler.shutdown()
    print("APScheduler stopped")

app = FastAPI(title="Price Tracker API", lifespan=lifespan)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "API worked!", "db_name": settings.DB_NAME}