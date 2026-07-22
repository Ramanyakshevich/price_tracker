from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from models.models import User, TrackedItem
from schemas.schemas import UserCreate, TriggerCreate


async def get_user_by_tg_id(session: AsyncSession, tg_id: int) -> User | None:
    result = await session.execute(select(User).where(User.tg_id == tg_id))
    return result.scalars().first()

async def create_user(session: AsyncSession, user_data: UserCreate) -> User:
    existing_user = await get_user_by_tg_id(session, user_data.tg_id)
    if existing_user is not None:
        return existing_user

    new_user = User(
        tg_id = user_data.tg_id,
        username = user_data.username
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def create_trigger(session: AsyncSession, trigger_data: TriggerCreate) -> TrackedItem:
    user = await get_user_by_tg_id(session, trigger_data.tg_id)
    if not user:
        user = await create_user(session, UserCreate(tg_id=trigger_data.tg_id))

    new_trigger = TrackedItem(
        user_id = user.id,
        city_from = trigger_data.city_from,
        city_to = trigger_data.city_to,
        target_price = trigger_data.target_price
    )
    session.add(new_trigger)
    await session.commit()
    await session.refresh(new_trigger)
    return new_trigger

async def get_user_triggers(session: AsyncSession, tg_id: int) -> list[TrackedItem]:
    user = await get_user_by_tg_id(session, tg_id)
    if not user:
        return []
    result = await session.execute(
        select(TrackedItem).where(TrackedItem.user_id == user.id)
    )
    return list(result.scalars().all())

async def delete_trigger(session: AsyncSession, trigger_id: int) -> bool:
    result = await session.execute(
        delete(TrackedItem).where(TrackedItem.id == trigger_id)
    )
    await session.commit()
    return result.rowcount > 0