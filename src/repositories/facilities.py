from sqlalchemy import select, insert, delete

from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import FacilityDataMapper, RoomFacilityDataMapper


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    mapper = FacilityDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    mapper = RoomFacilityDataMapper

    async def update_facilities(self, room_id: int, facilities_ids: list[int]):
        # current_facilities_ids = await self.get_filtered(room_id=room_id)
        get_current_facilities_ids = select(self.model.facility_id).filter_by(room_id=room_id)
        result = await self.session.execute(get_current_facilities_ids)
        current_facilities_ids = result.scalars().all()

        facilities_to_add = list(set(facilities_ids) - set(current_facilities_ids))
        facilities_to_delete = list(set(current_facilities_ids) - set(facilities_ids))

        if facilities_to_add:
            add_facilities_stmt = insert(self.model).values(
                [{"room_id": room_id, "facility_id": f_id} for f_id in facilities_to_add]
            )
            await self.session.execute(add_facilities_stmt)

        if facilities_to_delete:
            delete_facilities_stmt = (
                delete(self.model)
                .filter_by(room_id=room_id)
                .filter(self.model.facility_id.in_(facilities_to_delete))
            )
            await self.session.execute(delete_facilities_stmt)
