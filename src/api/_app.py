from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.database import Base, engine

from .services.bookings import router as bookings_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(bookings_router)
