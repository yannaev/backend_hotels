from src.database import async_session_maker_null_pull
from src.schemas.hotels import HotelAdd
from src.utils.db_manager import DBManager


async def test_add_hotel(db):
    hotel_data = HotelAdd(title="Континенталь", location="Москва")
    await db.hotels.add(hotel_data)
    await db.commit()