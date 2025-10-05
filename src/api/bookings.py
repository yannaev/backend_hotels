from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequest

router = APIRouter(prefix='/bookings', tags=['Бронирования'])


@router.get('')
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get('/me')
async def get_my_bookings(user_id: UserIdDep, db: DBDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post('')
async def create_booking(user_id: UserIdDep, booking_data: BookingAddRequest, db: DBDep):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    hotel = await db.hotels.get_one_or_none(id=room.hotel_id)
    _booking_data = BookingAdd(user_id=user_id, price=room.price, **booking_data.model_dump())
    booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    await db.commit()
    return {'status': 'OK', 'data': booking}