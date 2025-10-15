from contextlib import asynccontextmanager
import logging
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

sys.path.append(str(Path(__file__).parent.parent))
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

from src.api.hotels import router as router_hotels
from src.api.auth import router as router_auth
from src.api.rooms import router as router_rooms
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities
from src.api.images import router as router_images
from src.init import redis_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    logging.info("FastAPI Cache initialized with Redis backend")
    yield
    # Shutdown
    await redis_manager.close()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # или ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)
app.include_router(router_images)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
