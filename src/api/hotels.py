from fastapi import Query, APIRouter, Body

from sqlalchemy import insert, select

from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
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
        query = select(HotelsOrm)

        if title:
            query = query.filter(HotelsOrm.title.ilike(f'%{title.strip()}%'))

        if location:
            query = query.filter(HotelsOrm.location.ilike(f'%{location.strip()}%'))

        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )
        result = await session.execute(query)
        hotels_ = result.scalars().all()
        return hotels_


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
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(engine, compile_kwargs={'literal_binds': True}))
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {'status': 'OK'}


@router.put('/{hotel_id}',
            summary='Изменить отель',
            description='Изменить отель целиком')
def edit_hotel(hotel_id: int, hotel_data: Hotel):
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['title'] = hotel_data.title
            hotel['city'] = hotel_data.city
            break
    return {'status': 'OK'}


@router.patch('/{hotel_id}',
           summary='Частичное обновление данных отеля',
           description='Можно поменять один или несколько параметров')
def edit_hotel_parameter(
    hotel_id: int,
    hotel_data: HotelPATCH
):
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            if hotel_data.title:
                hotel['title'] = hotel_data.title
            if hotel_data.city:
                hotel['city'] = hotel_data.city
            break
    return {'status': 'OK'}


@router.delete('/{hotel_id}',
               summary='Удалить отель',
               description='Удалить отель из базы по ID')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}
