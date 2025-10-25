from pydantic import BaseModel, Field

from src.schemas.facilities import Facility


class RoomAddRequest(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)
    price: int = Field(gt=0)
    quantity: int = Field(ge=0)
    facilities_ids: list[int] = []


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int


class Room(RoomAdd):
    id: int


class RoomWithRels(Room):
    facilities: list[Facility]


class RoomPatchRequest(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)
    price: int | None = Field(None, gt=0)
    quantity: int | None = Field(None, ge=0)
    facilities_ids: list[int] = []


class RoomPatch(BaseModel):
    hotel_id: int | None = Field(None)
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
