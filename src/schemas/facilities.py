from pydantic import BaseModel, Field


class FacilityAdd(BaseModel):
    title: str = Field(max_length=100)


class Facility(FacilityAdd):
    id: int


class RoomFacilityAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomFacility(RoomFacilityAdd):
    id: int
    room_id: int
    facility_id: int
