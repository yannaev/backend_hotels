from fastapi import APIRouter, UploadFile, HTTPException, BackgroundTasks
import aiofiles
from pathlib import Path
from PIL import Image
from io import BytesIO

from src.tasks.tasks import resize_image


router = APIRouter(prefix="/images", tags=["Изображения"])


@router.post("", summary="Загрузить изображение")
async def upload_image(file: UploadFile, background_tasks: BackgroundTasks):
    head = await file.read()

    if len(head) > 5 * 1024 * 1024:
        raise HTTPException(400, detail="Файл слишком большой (максимум 5 MB)")

    img = Image.open(BytesIO(head))
    width, height = img.size
    if width < 200 or height < 200:
        raise HTTPException(400, detail="Минимальное разрешение: 200x200")

    image_path = Path("src/static/images") / file.filename
    async with aiofiles.open(image_path, "wb") as out_file:
        await out_file.write(head)

    # resize_image.delay(str(image_path))
    background_tasks.add_task(resize_image, str(image_path))

    return {"status": "OK"}
