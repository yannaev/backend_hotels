from datetime import date

from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import ObjectNotFoundException, HotelNotFoundHTTPException, HotelAlreadyExistsException, \
    HotelAlreadyExistsHTTPException, HotelNotFoundException
from src.schemas.hotels import HotelPatch, HotelAdd
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    "",
    summary="Получить список отелей",
    description="Получить список всех отелей, либо отель по названию, по локации",
)
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Локация отеля"),
    date_from: date = Query(examples=["2024-08-01"]),
    date_to: date = Query(examples=["2024-08-10"]),
):
    return await HotelService(db).get_hotels(
        pagination,
        title,
        location,
        date_from,
        date_to
    )


@router.get("/{hotel_id}", summary="Получить отель по ID", description="Получить один отель")
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.post("", summary="Добавить отель", description="Создать и добавить новый отель")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Marriott",
                "value": {"title": "Marriott", "location": "London"},
            },
            "2": {
                "summary": "Park INN",
                "value": {"title": "Park INN", "location": "Bangkok"},
            },
        }
    ),
):
    try:
        hotel = await HotelService(db).create_hotel(hotel_data)
    except HotelAlreadyExistsException:
        raise HotelAlreadyExistsHTTPException
    
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Изменить отель", description="Изменить отель целиком")
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    try:
        await HotelService(db).edit_hotel(hotel_id, hotel_data)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных отеля",
    description="Можно поменять один или несколько параметров",
)
async def edit_hotel_parameter(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    await HotelService(db).edit_hotel_parameter(hotel_id, hotel_data)
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удалить отель", description="Удалить отель из базы по ID")
async def delete_hotel(hotel_id: int, db: DBDep):
    try:
        await HotelService(db).delete_hotel(hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK"}
