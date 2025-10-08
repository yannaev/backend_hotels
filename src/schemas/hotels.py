from pydantic import BaseModel, Field


class HotelAdd(BaseModel):
    title: str = Field(max_length=100)
    location: str


class Hotel(HotelAdd):
    id: int


class HotelPatch(BaseModel):
    title: str | None = Field(None, max_length=100)
    location: str | None = Field(None)
