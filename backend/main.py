from fastapi import FastAPI
from core.config import settings
from api.routers import router

app = FastAPI(title="Price Tracker API")

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "API worked!", "db_name": settings.DB_NAME}