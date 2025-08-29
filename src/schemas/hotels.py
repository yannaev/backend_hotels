from pydantic import BaseModel, Field

class Hotel(BaseModel):
    title: str
    city: str

class HotelPATCH(BaseModel):
    title: str | None = Field(None)
    city: str | None = Field(None)