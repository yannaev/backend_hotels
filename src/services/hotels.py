from datetime import date

from src.exceptions import check_date_to_after_date_from, ObjectNotFoundException, HotelNotFoundException, \
    ObjectAlreadyExistsException, HotelAlreadyExistsException
from src.schemas.hotels import HotelAdd, HotelPatch, Hotel
from src.services.base import BaseService


class HotelService(BaseService):
    async def get_hotels(
            self,
            pagination,
            title: str | None,
            location: str | None,
            date_from: date,
            date_to: date,
    ):
        per_page = pagination.per_page or 5
        check_date_to_after_date_from(date_from, date_to)
        return await self.db.hotels.get_filtered_by_time(
            title=title,
            location=location,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
            date_from=date_from,
            date_to=date_to,
        )

    async def get_hotel(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def create_hotel(self, data: HotelAdd):
        try:
            hotel = await self.db.hotels.add(data)
            await self.db.commit()
        except ObjectAlreadyExistsException:
            raise HotelAlreadyExistsException
        return hotel

    async def edit_hotel(self, hotel_id: int, hotel_data: HotelAdd):
        await self.db.hotels.update(id=hotel_id, data=hotel_data)
        await self.db.commit()

    async def edit_hotel_parameter(self,hotel_id: int, hotel_data: HotelPatch,):
        await self.db.hotels.update(id=hotel_id, exclude_unset=True, data=hotel_data)
        await self.db.commit()

    async def delete_hotel(self, hotel_id: int):
        await self.get_hotel_with_check(hotel_id=hotel_id)
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()

    async def get_hotel_with_check(self, hotel_id: int) -> Hotel:
        try:
            return await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException