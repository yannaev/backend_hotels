from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Body, HTTPException, Response

from passlib.context import CryptContext
import jwt

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "8a055cfaa22528ce9c5e54c0225ff45d1ae0405ad280c7057c60e5ddd1e0e22f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


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
    hashed_password = pwd_context.hash(data.password)
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

        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail='Неверный email или пароль')

        access_token = create_access_token({'user_id': user.id})
        response.set_cookie('access_token', access_token)
        return {'access_token': access_token}
