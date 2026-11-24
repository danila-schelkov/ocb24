from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.database import Base, engine

from .services.bookings import register_bookings_service


@asynccontextmanager
async def lifespan(_app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

register_bookings_service(app)
