from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException, \
    check_date_to_after_date_from, RoomNotFoundException
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.schemas.rooms import Room
from src.services.base import BaseService


class BookingService(BaseService):
    async def get_bookings(self):
        return await self.db.bookings.get_all()

    async def get_my_bookings(self, user_id: int):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def create_booking(self, user_id: int, booking_data: BookingAddRequest):
        check_date_to_after_date_from(booking_data.date_from, booking_data.date_to)
        try:
            room: Room = await self.db.rooms.get_one(id=booking_data.room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
        _booking_data = BookingAdd(user_id=user_id, price=room.price, **booking_data.model_dump())
        try:
            booking = await self.db.bookings.add_booking(_booking_data, hotel_id=room.hotel_id)
        except AllRoomsAreBookedException:
            raise AllRoomsAreBookedException
        await self.db.commit()
        return booking