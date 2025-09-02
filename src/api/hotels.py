from fastapi import Query, APIRouter, Body

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix='/hotels', tags=['Отели'])


@router.get('',
            summary='Получить список отелей',
            description='Получить список всех отелей, либо отель по названию, по локации')
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description='Название отеля'),
        location: str | None = Query(None, description='Локация отеля')
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            title=title,
            location=location,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )



# body, request body
@router.post('',
             summary='Добавить отель',
             description='Создать и добавить новый отель')
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    '1': {
        'summary': 'Marriott',
        'value': {
            'title': 'Marriott',
            'location': 'London'
        }
    },
    '2': {
        'summary': 'Park INN',
        'value': {
            'title': 'Park INN',
            'location': 'Bangkok'
        }
    }
})):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {'status': 'OK', 'data': hotel}


@router.put('/{hotel_id}',
            summary='Изменить отель',
            description='Изменить отель целиком')
async def edit_hotel(hotel_id: int, hotel_data: Hotel):
    async with async_session_maker() as session:
        await HotelsRepository(session).update(id=hotel_id, data=hotel_data)
        await session.commit()
    return {'status': 'OK'}


@router.patch('/{hotel_id}',
           summary='Частичное обновление данных отеля',
           description='Можно поменять один или несколько параметров')
async def edit_hotel_parameter(
    hotel_id: int,
    hotel_data: HotelPATCH
):
    async with async_session_maker() as session:
        await HotelsRepository(session).update(id=hotel_id, exclude_unset=True, data=hotel_data)
        await session.commit()
    return {'status': 'OK'}


@router.delete('/{hotel_id}',
               summary='Удалить отель',
               description='Удалить отель из базы по ID')
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {'status': 'OK'}
