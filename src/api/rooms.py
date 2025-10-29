from datetime import date

from fastapi import APIRouter, Query

from src.api.dependencies import DBDep
from src.exceptions import (
    RoomNotFoundHTTPException,
    HotelNotFoundHTTPException,
    RoomNotFoundException,
    HotelNotFoundException,
    DeleteRoomErrorException,
    DeleteRoomErrorHTTPException,
)
from src.schemas.rooms import RoomAddRequest, RoomPatchRequest
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get(
    "/{hotel_id}/rooms",
    summary="Получить список всех номеров отеля",
    description="Получить список всех номеров отеля",
)
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(examples=["2025-09-10"]),
    date_to: date = Query(examples=["2025-09-20"]),
):
    try:
        return await RoomService(db).get_rooms(hotel_id, date_from, date_to)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException


@router.get(
    "/{hotel_id}/rooms/{room_id}",
    summary="Получить номер отеля по ID",
    description="Получить один номер отеля",
)
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        return await RoomService(db).get_room(hotel_id, room_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.post(
    "/{hotel_id}/rooms",
    summary="Добавить номер в отель",
    description="Создать и добавить новый номер в отель",
)
async def create_room(hotel_id: int, room_data: RoomAddRequest, db: DBDep):
    try:
        room = await RoomService(db).create_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return {"status": "OK", "data": room}


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Полное обновление данных номера отеля",
    description="Обновить все параметры номера отеля",
)
async def update_room(hotel_id: int, room_id: int, room_data: RoomAddRequest, db: DBDep):
    try:
        await RoomService(db).update_room(hotel_id, room_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное обноление данных номера отеля",
    description="Обновить один или несколько параметров номера отеля",
)
async def edit_room_parameter(hotel_id: int, room_id: int, room_data: RoomPatchRequest, db: DBDep):
    try:
        await RoomService(db).edit_room_parameter(hotel_id, room_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": "OK"}


@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    summary="Удалить номер отеля по ID",
    description="Удалить один номер отеля",
)
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        await RoomService(db).delete_room(hotel_id, room_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except DeleteRoomErrorException:
        raise DeleteRoomErrorHTTPException
    return {"status": "OK"}
