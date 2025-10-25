from pydantic import BaseModel, EmailStr, ConfigDict, Field


class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str


class User(BaseModel):
    id: int
    email: EmailStr


class UserWithHashedPassword(User):
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)
