from fastapi import Query, Body, Path, APIRouter


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
def create_hotel(
        title: str = Body(embed=True)
):
    global hotels
    hotels.append({
        'id': hotels[-1]['id'] + 1,
        'title': title
    })
    return {'status': 'OK'}


@router.put('/{hotel_id}',
            summary='Изменить отель',
            description='Изменить отель целиком')
def edit_hotel(
        hotel_id: int = Path(description='ID отеля'),
        title: str = Body(),
        city: str = Body()
):
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['title'] = title
            hotel['city'] = city
            break
    return {'status': 'OK'}


@router.patch('/{hotel_id}',
           summary='Частичное обновление данных отеля',
           description='Можно поменять один или несколько параметров')
def edit_hotel_parameter(
    hotel_id: int,
    title: str | None = Body(default=None),
    city: str | None = Body(default=None)
):
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            if title:
                hotel['title'] = title
            if city:
                hotel['city'] = city
            break
    return {'status': 'OK'}


@router.delete('/{hotel_id}',
               summary='Удалить отель',
               description='Удалить отель из базы по ID')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}
