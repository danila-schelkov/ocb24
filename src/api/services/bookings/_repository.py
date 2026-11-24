from collections.abc import Sequence
from datetime import date, time

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import SlotAlreadyBooked
from .models import BOOKING_UNIQUE_INDEX_NAME, BookingModel
from .types import BookingId, BookingStatus


class BookingRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session

    async def create(
        self, name: str, phone: str, booking_date: date, booking_time: time, guests: int
    ) -> BookingModel:
        booking = BookingModel(
            guest_name=name,
            guest_phone=phone,
            booking_date=booking_date,
            booking_time=booking_time,
            guests=guests,
        )

        await self._create_or_raise(booking)

        return booking

    async def _create_or_raise(self, booking: BookingModel) -> None:
        self._session.add(booking)

        try:
            await self._session.flush()
        except IntegrityError as e:
            error_message = str(e.orig)
            if (
                BOOKING_UNIQUE_INDEX_NAME in error_message
                or "bookings.booking_date, bookings.booking_time" in error_message
            ):
                raise SlotAlreadyBooked from e
            raise

    async def list(self, booking_date: date | None) -> Sequence[BookingModel]:
        query = select(BookingModel)
        if booking_date is not None:
            query = query.where(BookingModel.booking_date == booking_date)

        result = await self._session.scalars(query)
        bookings = result.all()
        return bookings

    async def get_by_id(self, id: BookingId) -> BookingModel | None:
        return await self._session.get(BookingModel, id)

    async def update_status(
        self, booking: BookingModel, status: BookingStatus
    ) -> BookingModel:
        booking.status = status
        await self._session.flush()
        return booking
