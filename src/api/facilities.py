from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd
from src.services.facilities import FacilityService

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Получить список всех удобств")
@cache(expire=10)
async def get_all_facilities(db: DBDep):
    return await FacilityService(db).get_all_facilities()


@router.post("", summary="Создать новое удобство")
async def create_facility(db: DBDep, data: FacilityAdd):
    facility = await FacilityService(db).create_facility(data)
    return {"status": "OK", "data": facility}
