from pydantic import BaseModel, Field


class HotelAdd(BaseModel):
    title: str = Field(min_length=5, max_length=100)
    location: str = Field(min_length=5, max_length=100)


class Hotel(HotelAdd):
    id: int


class HotelPatch(BaseModel):
    title: str | None = Field(None, min_length=5, max_length=100)
    location: str | None = Field(None, min_length=5, max_length=100)
