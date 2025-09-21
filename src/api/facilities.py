from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Получить список всех удобств")
@cache(expire=10)
async def get_all_facilities(db: DBDep):
    print("Get all facilities")
    return await db.facilities.get_all()


@router.post("", summary="Создать новое удобство")
async def create_facility(db: DBDep, data: FacilityAdd):
    await db.facilities.add(data)
    await db.commit()
    return {"status": "OK"}