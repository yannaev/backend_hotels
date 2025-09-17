from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RoomDataMapper, RoomDataWithRelsMapper
from src.schemas.rooms import Room
from src.repositories.utils import rooms_ids_for_booking


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper

    async def get_filtered_by_time(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date):

        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        result = await self.session.execute(query)
        return [RoomDataWithRelsMapper.map_to_domain_entity(model) for model in result.unique().scalars().all()]

    async def get_one_or_none(self, **filters) -> Room | None:
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filters)
        )
        result = await self.session.execute(query)
        room = result.scalars().one_or_none()
        if room is None:
            return None
        return RoomDataWithRelsMapper.map_to_domain_entity(room)
