from datetime import date

from fastapi import HTTPException


class NabronirovalException(Exception):
    detail = 'Неожиданная ошибка'

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(NabronirovalException):
    detail = 'Объект не найден'

class RoomNotFoundException(ObjectNotFoundException):
    detail = 'Номер не найден'

class HotelNotFoundException(ObjectNotFoundException):
    detail = 'Отель не найден'


class ObjectAlreadyExistsException(NabronirovalException):
    detail = 'Похожий объект уже существует'


class AllRoomsAreBookedException(NabronirovalException):
    detail = 'Не осталось свободных номеров'


class WrongDatesException(NabronirovalException):
    detail = 'Дата выезда должна быть больше даты заезда'


class IntegrityErrorException(NabronirovalException):
    detail = 'Ошибка добавления'

class FileSizeException(NabronirovalException):
    detail = 'Превышен максимальный размер файла'

class FileResolutionException(NabronirovalException):
    detail = 'Превышен максимальный размер файла'

class NabronirovalHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = 'Отель не найден'


class RoomNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = 'Номер не найден'

class FileSizeHTTPException(NabronirovalHTTPException):
    status_code = 400
    detail = 'Превышен максимальный размер файла'


class FileResolutionHTTPException(NabronirovalHTTPException):
    status_code = 400
    detail = 'Минимальное разрешение: 200x200'

def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(status_code=422, detail="Дата заезда не может быть позже даты выезда")