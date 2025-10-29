from pathlib import Path

import aiofiles
from fastapi import UploadFile, BackgroundTasks

from src.exceptions import FileSizeException, FileResolutionException, ImageFormatException
from src.services.base import BaseService
from src.tasks.tasks import resize_image
from PIL import Image, UnidentifiedImageError
from io import BytesIO


class ImageService(BaseService):
    async def upload_image(self, file: UploadFile, background_tasks: BackgroundTasks):
        head = await file.read()

        if len(head) > 5 * 1024 * 1024:
            raise FileSizeException

        try:
            img = Image.open(BytesIO(head))
        except UnidentifiedImageError:
            raise ImageFormatException
        width, height = img.size
        if width < 200 or height < 200:
            raise FileResolutionException

        image_path = Path("src/static/images") / file.filename
        async with aiofiles.open(image_path, "wb") as out_file:
            await out_file.write(head)

        # resize_image.delay(str(image_path))
        background_tasks.add_task(resize_image, str(image_path))
