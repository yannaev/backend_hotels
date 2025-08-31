from fastapi import Query, APIRouter, Body

from sqlalchemy import insert

from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix='/hotels', tags=['Отели'])


hotels = [
    {'id': 1, 'title': 'Hayatt', 'city': 'Moscow'},
    {'id': 2, 'title': 'Radisson', 'city': 'Yekaterinburg'},
    {'id': 3, 'title': 'Marriott', 'city': 'Saint Petersburg'},
    {'id': 4, 'title': 'Hilton', 'city': 'Kazan'},
    {'id': 5, 'title': 'Ibis', 'city': 'Novosibirsk'},
    {'id': 6, 'title': 'DoubleTree', 'city': 'Sochi'},
    {'id': 7, 'title': 'Park Inn', 'city': 'Rostov-on-Don'},
    {'id': 8, 'title': 'Sheraton', 'city': 'Nizhny Novgorod'},
    {'id': 9, 'title': 'Holiday Inn', 'city': 'Vladivostok'},
    {'id': 10, 'title': 'Four Seasons', 'city': 'Moscow'},
    {'id': 11, 'title': 'Ritz Carlton', 'city': 'Samara'}
]


@router.get('',
            summary='Получить список отелей',
            description='Получить список всех отелей, либо отель по ID, либо отель по названию')
def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(default=None, description='ID отеля'),
        title: str | None = Query(None, description='Название отеля')
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)

    return hotels_[(pagination.page - 1) * pagination.per_page:pagination.page * pagination.per_page]


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
