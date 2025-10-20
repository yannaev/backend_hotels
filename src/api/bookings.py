from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException, RoomNotFoundHTTPException
from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.schemas.rooms import Room
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
async def get_bookings(db: DBDep):
    return await BookingService(db).get_bookings()


@router.get("/me")
async def get_my_bookings(user_id: UserIdDep, db: DBDep):
    return await BookingService(db).get_my_bookings(user_id)


@router.post("")
async def create_booking(user_id: UserIdDep, booking_data: BookingAddRequest, db: DBDep):
    booking = await BookingService(db).create_booking(user_id, booking_data)
    return {"status": "OK", "data": booking}
