from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.models import TrackedItem
from services.aviasales import get_cheapest_ticket

async def check_prices(session: AsyncSession):
    result = await session.execute(select(TrackedItem))
    triggers = result.scalars().all()

    if not triggers:
        print("No active subscriptions found in the database")
        return

    for trigger in triggers:
        current_price = await get_cheapest_ticket(
            city_from = trigger.city_from,
            city_to = trigger.city_to,
            depart_date=trigger.depart_date
        )
        if current_price is None:
            print(f"Failed to fetch price for {trigger.city_from} -> {trigger.city_to}")
            continue

        date_info = f" on {trigger.depart_date}" if trigger.depart_date else ""

        if current_price <= trigger.target_price:
            print(
                f"\nMATCH FOUND! Cheap ticket deal{date_info}!\n"
                f"Route: {trigger.city_from} -> {trigger.city_to}\n"
                f"Target price: {trigger.target_price} USD\n"
                f"Current price: {current_price} USD (Savings: {trigger.target_price - current_price} USD)\n"
            )
        else:
            print(
                f"{trigger.city_from} -> {trigger.city_to}{date_info}: "
                f"current price is {current_price} USD (waiting for <= {trigger.target_price} USD)"
            )