from fastapi import Query, APIRouter, Body

from src.api.dependencies import PaginationDep, DBDep
from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import HotelPatch, HotelAdd

router = APIRouter(prefix='/hotels', tags=['Отели'])


@router.get('',
            summary='Получить список отелей',
            description='Получить список всех отелей, либо отель по названию, по локации')
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(None, description='Название отеля'),
        location: str | None = Query(None, description='Локация отеля')
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_all(
        title=title,
        location=location,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )


@router.get('/{hotel_id}',
            summary='Получить отель по ID',
            description='Получить один отель')
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)


# body, request body
@router.post('',
             summary='Добавить отель',
             description='Создать и добавить новый отель')
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(openapi_examples={
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
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {'status': 'OK', 'data': hotel}


@router.put('/{hotel_id}',
            summary='Изменить отель',
            description='Изменить отель целиком')
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await db.hotels.update(id=hotel_id, data=hotel_data)
    await db.commit()
    return {'status': 'OK'}


@router.patch('/{hotel_id}',
           summary='Частичное обновление данных отеля',
           description='Можно поменять один или несколько параметров')
async def edit_hotel_parameter(
    hotel_id: int,
    hotel_data: HotelPatch,
    db: DBDep
):
    await db.hotels.update(id=hotel_id, exclude_unset=True, data=hotel_data)
    await db.commit()
    return {'status': 'OK'}


@router.delete('/{hotel_id}',
               summary='Удалить отель',
               description='Удалить отель из базы по ID')
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {'status': 'OK'}
