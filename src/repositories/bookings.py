from datetime import date

from fastapi import HTTPException
from sqlalchemy import select

from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.bookings import BookingAdd


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = select(self.model).filter(self.model.date_from == date.today())
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def add_booking(self, booking_data: BookingAdd, hotel_id: int):
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=booking_data.date_from,
            date_to=booking_data.date_to,
            hotel_id=hotel_id)
        rooms_ids_to_book_res = await self.session.execute(rooms_ids_to_get)
        rooms_ids_to_book = rooms_ids_to_book_res.scalars().all()

        if booking_data.room_id in rooms_ids_to_book:
            booking = await self.add(booking_data)
            return booking
        else:
            raise HTTPException(status_code=409, detail='Нет свободных номеров на эти даты')