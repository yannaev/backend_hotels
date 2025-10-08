from fastapi import APIRouter, Body, HTTPException, Response

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'])


@router.post('/register',
             summary='Регистрация пользователя',
             description='Регистрация пользователя по email')
async def register_user(db: DBDep, data: UserRequestAdd = Body(openapi_examples={
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
    try:
        hashed_password = AuthService().hash_password(data.password)
        new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
        await db.users.add(new_user_data)
        await db.commit()
    except: # noqa: E722
        raise HTTPException(status_code=400, detail='Пользователь с таким email уже существует')

    return {'status': 'OK'}



@router.post('/login')
async def login_user(
        db: DBDep,
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
    user = await db.users.get_user_with_hashed_password(email=data.email)

    if not user or not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Неверный email или пароль')

    access_token = AuthService().create_access_token({'user_id': user.id})
    response.set_cookie('access_token', access_token)
    return {'access_token': access_token}


@router.get('/me')
async def get_me(user_id: UserIdDep, db: DBDep):
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie('access_token')
    return {'status': 'OK'}