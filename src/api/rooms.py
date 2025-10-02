from datetime import date

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.exc import IntegrityError

from src.api.dependencies import DBDep
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch

router = APIRouter(prefix='/hotels', tags=['Номера'])


@router.get('/{hotel_id}/rooms',
            summary='Получить список всех номеров отеля',
            description='Получить список всех номеров отеля')
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(examples=['2025-09-10']),
        date_to: date = Query(examples=['2025-09-20'])
):
        return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get('/{hotel_id}/rooms/{room_id}',
            summary='Получить номер отеля по ID',
            description='Получить один номер отеля')
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    room = await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
    if room is None:
        raise HTTPException(status_code=404, detail='Номер не найден')
    return room


@router.post('/{hotel_id}/rooms',
             summary='Добавить номер в отель',
             description='Создать и добавить новый номер в отель')
async def create_room(hotel_id: int, room_data: RoomAddRequest, db: DBDep):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    try:
        room = await db.rooms.add(_room_data)

        rooms_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=facility_id) for facility_id in room_data.facilities_ids]
        await db.rooms_facilities.add_bulk(rooms_facilities_data)
        await db.commit()
    except IntegrityError:
        raise HTTPException(status_code=404, detail='Отель не найден')
    return {'status': 'OK', 'data': room}


@router.put('/{hotel_id}/rooms/{room_id}',
            summary='Полное обноление данных номера отеля',
            description='Обновить все параметры номера отеля')
async def update_room(hotel_id: int, room_id: int, room_data: RoomAddRequest, db: DBDep):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    try:
        await db.rooms.update(data=_room_data, id=room_id)

        await db.rooms_facilities.update_facilities(room_id=room_id, facilities_ids=room_data.facilities_ids)

        await db.commit()
    except IntegrityError:
        raise HTTPException(status_code=404, detail='Отель не найден')
    return {'status': 'OK'}


@router.patch('/{hotel_id}/rooms/{room_id}',
              summary='Частичное обноление данных номера отеля',
              description='Обновить один или несколько параметров номера отеля')
async def edit_room_parameter(hotel_id: int, room_id: int, room_data: RoomPatchRequest, db: DBDep):
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)

    await db.rooms.update(data=_room_data, id=room_id, hotel_id=hotel_id, exclude_unset=True)

    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.update_facilities(room_id=room_id, facilities_ids=room_data.facilities_ids)

    await db.commit()
    return {'status': 'OK'}


@router.delete('/{hotel_id}/rooms/{room_id}',
               summary='Удалить номер отеля по ID',
               description='Удалить один номер отеля')
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {'status': 'OK'}



