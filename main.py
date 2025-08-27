from fastapi import FastAPI, Query, Body
import uvicorn

app = FastAPI()


hotels = [
    {'id': 1, 'title': 'Hayatt', 'city': 'Moscow'},
    {'id': 2, 'title': 'Radisson', 'city': 'Yekaterinburg'},
]

@app.get('/hotels')
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
@app.post('/hotels')
def create_hotel(
        title: str = Body(embed=True)
):
    global hotels
    hotels.append({
        'id': hotels[-1]['id'] + 1,
        'title': title
    })
    return {'status': 'OK'}


@app.delete('/hotels/{hotel_id}')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)