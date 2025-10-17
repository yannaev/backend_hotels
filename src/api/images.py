from fastapi import APIRouter, UploadFile, BackgroundTasks

from src.exceptions import FileSizeException, FileSizeHTTPException, FileResolutionException, \
    FileResolutionHTTPException
from src.services.images import ImageService


router = APIRouter(prefix="/images", tags=["Изображения"])


@router.post("", summary="Загрузить изображение")
async def upload_image(file: UploadFile, background_tasks: BackgroundTasks):
    try:
        await ImageService().upload_image(file, background_tasks)
    except FileSizeException:
        raise FileSizeHTTPException
    except FileResolutionException:
        raise FileResolutionHTTPException
    return {"status": "OK"}
