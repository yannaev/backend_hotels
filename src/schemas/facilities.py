from pydantic import BaseModel, Field


class FacilityAdd(BaseModel):
    title: str = Field(max_length=100)


class Facility(FacilityAdd):
    id: int

    model_config = {
        "from_attributes": True
    }