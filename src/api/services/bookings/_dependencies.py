from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_db_session

from ._repository import BookingRepository
from ._service import BookingService


def get_booking_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> BookingRepository:
    return BookingRepository(session)


def get_booking_service(
    repo: Annotated[BookingRepository, Depends(get_booking_repository)],
) -> BookingService:
    return BookingService(repo)


type BookingServiceDep = Annotated[BookingService, Depends(get_booking_service)]
