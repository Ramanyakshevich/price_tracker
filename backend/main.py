from fastapi import FastAPI
from core.config import settings

app = FastAPI(title="Price Tracker API")

@app.get("/")
async def root():
    return {"message": "API worked!", "db_name": settings.DB_NAME}