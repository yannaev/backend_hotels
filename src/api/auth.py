from fastapi import APIRouter, Body, HTTPException, Response

from src.api.dependencies import UserIdDep
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'])


@router.post('/register',
             summary='Регистрация пользователя',
             description='Регистрация пользователя по email')
async def register_user(data: UserRequestAdd = Body(openapi_examples={
    '1': {
        'summary': 'User 1',
        'value': {
            'email': '123456@mail.ru',
            'password': '123456'
        },
    },
    '2': {
        'summary': 'User 2',
        'value': {
            'email': 'alex@mail.ru',
            'password': 'qwerty'
        },
    },

})):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)

    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {'status': 'OK'}


@router.post('/login')
async def login_user(
        response: Response,
        data: UserRequestAdd = Body(openapi_examples={
    '1': {
        'summary': 'User 1',
        'value': {
            'email': '123456@mail.ru',
            'password': '123456'
        },
    },
    '2': {
        'summary': 'User 2',
        'value': {
            'email': 'alex@mail.ru',
            'password': 'qwerty'
        },
    }})):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)

        if not user or not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail='Неверный email или пароль')

        access_token = AuthService().create_access_token({'user_id': user.id})
        response.set_cookie('access_token', access_token)
        return {'access_token': access_token}


@router.get('/me')
async def get_me(user_id: UserIdDep):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
    return user