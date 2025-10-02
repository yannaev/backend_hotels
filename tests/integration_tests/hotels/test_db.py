from src.database import async_session_maker
from src.schemas.hotels import HotelAdd
from src.utils.db_manager import DBManager


async def test_add_hotel():
    hotel_data = HotelAdd(title="Континенталь", location="Москва")

    async with DBManager(session_factory=async_session_maker) as db:
        new_hotel_data = await db.hotels.add(hotel_data)
        await db.commit()
        print(f"{new_hotel_data=}")