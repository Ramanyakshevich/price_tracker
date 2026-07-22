from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from crud import crud
from core.database import get_db
from schemas.schemas import UserResponse, UserCreate, TriggerResponse, TriggerCreate

router = APIRouter(prefix="/api", tags=["Tracker API"])

@router.post("/users", response_model=UserResponse)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_user(db, user)

@router.post("/triggers", response_model=TriggerResponse)
async def add_trigger(trigger: TriggerCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_trigger(db, trigger)

@router.get("/triggers/{tg_id}", response_model=List[TriggerResponse])
async def get_user_triggers(tg_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_user_triggers(db, tg_id)

@router.delete("/triggers/{trigger_id}")
async def remove_trigger(trigger_id: int, db: AsyncSession = Depends(get_db)):
    success = await crud.delete_trigger(db, trigger_id)
    if not success:
        raise HTTPException(status_code = 404, detail = "Trigger is not found")
    return {"message": "Trigger was deleted successfully"}