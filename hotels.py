from fastapi import Query, APIRouter, Body

from schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix='/hotels', tags=['Отели'])


hotels = [
    {'id': 1, 'title': 'Hayatt', 'city': 'Moscow'},
    {'id': 2, 'title': 'Radisson', 'city': 'Yekaterinburg'},
]


@router.get('',
            summary='Получить список отелей',
            description='Получить список всех отелей, либо отель по ID, либо отель по названию')
def get_hotels(
        id: int | None = Query(default=None, description='ID отеля'),
        title:str | None = Query(None, description='Название отеля'),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)

    return hotels_


# body, request body
@router.post('',
             summary='Добавить отель',
             description='Создать и добавить новый отель')
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    '1': {
        'summary': 'Marriott',
        'value': {
            'title': 'Marriott',
            'city': 'London'
        }
    },
    '2': {
        'summary': 'Park INN',
        'value': {
            'title': 'Park INN',
            'city': 'Bangkok'
        }
    }
})):
    global hotels
    hotels.append({
        'id': hotels[-1]['id'] + 1,
        'title': hotel_data.title,
        'city': hotel_data.city
    })
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
