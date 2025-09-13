from datetime import date

from sqlalchemy import select

from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.schemas.hotels import Hotel
from src.repositories.utils import rooms_ids_for_booking


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel


    async def get_filtered_by_time(
            self,
            title,
            location,
            limit,
            offset,
            date_from: date,
            date_to: date,
    ) -> list[Hotel]:
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)

        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
            .distinct()
        )

        query = (
            select(HotelsOrm)
            .filter(HotelsOrm.id.in_(hotels_ids_to_get))
        )

        if title:
            query = query.filter(HotelsOrm.title.ilike(f'%{title.strip()}%'))

        if location:
            query = query.filter(HotelsOrm.location.ilike(f'%{location.strip()}%'))

        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)
        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]
