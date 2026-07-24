import ssl
import aiohttp
from typing import Optional
from core.config import settings

AVIASALES_API_URL = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates"

async def get_cheapest_ticket(city_from: str, city_to: str, depart_date: Optional[str] = None) -> Optional[int]:
    params = {
        "origin": city_from.upper(),
        "destination": city_to.upper(),
        "currency": "usd",
        "token": settings.TRAVELPAYOUTS_TOKEN,
        "direct": "true",
        "limit": 10
    }

    if depart_date:
        params["departure_at"] = depart_date

    try:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        async with aiohttp.ClientSession() as session:
            async with session.get(AVIASALES_API_URL, params=params, ssl=ssl_context) as response:
                if response.status != 200:
                    print(f"Error API: status {response.status}")
                    return None

                data = await response.json()

                if not data.get("success") or not data.get("data"):
                    return None

                prices = [item["price"] for item in data["data"] if "price" in item]
                return min(prices) if prices else None

    except Exception as e:
        print(f"Error during response: {e}")
        return None