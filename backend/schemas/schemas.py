from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    tg_id: int
    username: Optional[str] = None

class UserResponse(UserCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)

class TriggerCreate(BaseModel):
    tg_id: int
    city_from: str
    city_to: str
    target_price: int

class TriggerResponse(BaseModel):
    id: int
    user_id: int
    city_from: str
    city_to: str
    target_price: int

    model_config = ConfigDict(from_attributes=True)
