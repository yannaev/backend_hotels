from fastapi import Depends, Query, Request, HTTPException
from pydantic import BaseModel
from typing import Annotated

from src.database import async_session_maker
from src.services.auth import AuthService
from src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(default=1, ge=1, description='Номер страницы')]
    per_page: Annotated[int | None, Query(None, ge=1, le=50, description='Количество на странице')]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get('access_token', None)
    if not token:
        raise HTTPException(status_code=401, detail='Необходима авторизация, вы не предоставили токен')
    return token


def get_user_id_from_token(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token(token)
    return data['user_id']


UserIdDep = Annotated[int, Depends(get_user_id_from_token)]


def get_db_manager():
    return DBManager(session_factory=async_session_maker)


async def get_db():
    async with get_db_manager() as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]

