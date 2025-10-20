from fastapi import APIRouter, Body, HTTPException, Response

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import UserAlreadyExistsException, UserEmailAlreadyExistsHTTPException, EmailNotRegisteredException, \
    EmailNotRegisteredHTTPException, IncorrectPasswordException, IncorrectPasswordHTTPException
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post(
    "/register",
    summary="Регистрация пользователя",
    description="Регистрация пользователя по email",
)
async def register_user(
    db: DBDep,
    data: UserRequestAdd = Body(
        openapi_examples={
            "1": {
                "summary": "User 1",
                "value": {"email": "123456@mail.ru", "password": "123456"},
            },
            "2": {
                "summary": "User 2",
                "value": {"email": "alex@mail.ru", "password": "qwerty"},
            },
        }
    ),
):


    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException


    return {"status": "OK"}


@router.post("/login")
async def login_user(
    db: DBDep,
    response: Response,
    data: UserRequestAdd = Body(
        openapi_examples={
            "1": {
                "summary": "User 1",
                "value": {"email": "123456@mail.ru", "password": "123456"},
            },
            "2": {
                "summary": "User 2",
                "value": {"email": "alex@mail.ru", "password": "qwerty"},
            },
        }
    ),
):
    try:
        access_token = await AuthService(db).login_user(data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
async def get_me(user_id: UserIdDep, db: DBDep):
    return await AuthService(db).get_one_or_none_user(user_id)


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
