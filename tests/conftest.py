import pytest
import json
from httpx import AsyncClient, ASGITransport

from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pull
from src.main import app
from src.models import *
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def insert_mock_data(setup_database):
    with open("tests/mock_hotels.json", "r", encoding="utf-8") as f:
        hotels_data = json.load(f)

    with open("tests/mock_rooms.json", "r", encoding="utf-8") as f:
        rooms_data = json.load(f)

    async with DBManager(session_factory=async_session_maker_null_pull) as db:
        for hotel in hotels_data:
            await db.hotels.add(HotelAdd(**hotel))

        for room in rooms_data:
            await db.rooms.add(RoomAdd(**room))

        await db.commit()



@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post(
            "/auth/register",
            json={
                "email": "kot@pes.com",
                "password": "1234"
            }
        )