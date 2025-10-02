from src.database import async_session_maker_null_pull
from src.schemas.hotels import HotelAdd
from src.utils.db_manager import DBManager


async def test_add_hotel():
    hotel_data = HotelAdd(title="Континенталь", location="Москва")

    async with DBManager(session_factory=async_session_maker_null_pull) as db:
        await db.hotels.add(hotel_data)
        await db.commit()