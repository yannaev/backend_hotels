from fastapi import Depends, Query
from pydantic import BaseModel
from typing import Annotated


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(default=1, ge=1, description='Номер страницы')]
    per_page: Annotated[int | None, Query(default=5, ge=1, le=50, description='Количество на странице')]


PaginationDep = Annotated[PaginationParams, Depends()]