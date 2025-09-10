from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch

router = APIRouter(prefix='/hotels', tags=['Номера'])


@router.get('/{hotel_id}/rooms',
            summary='Получить список всех номеров отеля',
            description='Получить список всех номеров отеля')
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)


@router.get('/{hotel_id}/rooms/{room_id}',
            summary='Получить номер отеля по ID',
            description='Получить один номер отеля')
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)
        if room is None:
            raise HTTPException(status_code=404, detail='Номер не найден')
        return room


@router.post('/{hotel_id}/rooms',
             summary='Добавить номер в отель',
             description='Создать и добавить новый номер в отель')
async def create_room(hotel_id: int, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        try:
            room = await RoomsRepository(session).add(_room_data)
            await session.commit()
        except IntegrityError:
            raise HTTPException(status_code=404, detail='Отель не найден')
        return {'status': 'OK', 'data': room}


@router.put('/{hotel_id}/rooms/{room_id}',
            summary='Полное обноление данных номера отеля',
            description='Обновить все параметры номера отеля')
async def update_room(hotel_id: int, room_id: int, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        try:
            await RoomsRepository(session).update(data=_room_data, id=room_id)
            await session.commit()
        except IntegrityError:
            raise HTTPException(status_code=404, detail='Отель не найден')
        return {'status': 'OK'}


@router.patch('/{hotel_id}/rooms/{room_id}',
              summary='Частичное обноление данных номера отеля',
              description='Обновить один или несколько параметров номера отеля')
async def edit_room_parameter(hotel_id: int, room_id: int, room_data: RoomPatchRequest):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomsRepository(session).update(data=_room_data, id=room_id, hotel_id=hotel_id, exclude_unset=True)
        await session.commit()
        return {'status': 'OK'}


@router.delete('/{hotel_id}/rooms/{room_id}',
               summary='Удалить номер отеля по ID',
               description='Удалить один номер отеля')
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
        return {'status': 'OK'}



