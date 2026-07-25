import re
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator


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
    depart_date: Optional[str] = None

    @field_validator("city_from", "city_to")
    @classmethod
    def validate_iata(cls, value: str) -> str:
        value = value.upper()
        if not re.match(r"^[A-Z]{3}$", value):
            raise ValueError(f"Code '{value}' is invalid. Expected 3 letters (e. g. WAW, FCO)")
        return value

    @field_validator(depart_date)
    @classmethod
    def validate_date(cls, value:Optional[str]) -> Optional[str]:
        if value is None:
            return value
        try:
            parsed_date = datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(f"Date '{value}' is invalid. Use YYYY-MM-DD format")

        if parsed_date < datetime.today().date():
            raise ValueError("Departure date cannot be in the past")
        return value

class TriggerResponse(BaseModel):
    id: int
    user_id: int
    city_from: str
    city_to: str
    target_price: int
    depart_date: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
