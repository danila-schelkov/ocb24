from collections.abc import Sequence
from datetime import date

from pydantic import TypeAdapter

from ._repository import BookingRepository
from .exceptions import BookingNotFound
from .schemas import BookingCreate, BookingId, BookingOut
from .types import BookingStatus

_booking_list_adapter = TypeAdapter(list[BookingOut])


class BookingService:
    def __init__(self, repository: BookingRepository) -> None:
        self._repository = repository

    async def create_booking(self, new_booking: BookingCreate) -> BookingOut:
        booking = await self._repository.create(
            name=new_booking.name,
            phone=new_booking.phone,
            booking_date=new_booking.booking_date,
            booking_time=new_booking.booking_time,
            guests=new_booking.guests,
        )

        return BookingOut.model_validate(booking)

    async def list_bookings(self, booking_date: date | None) -> Sequence[BookingOut]:
        bookings = await self._repository.list(booking_date=booking_date)

        return _booking_list_adapter.validate_python(bookings)

    async def get_booking(self, booking_id: BookingId) -> BookingOut:
        booking = await self._repository.get_by_id(booking_id)
        if booking is None:
            raise BookingNotFound(booking_id)

        return BookingOut.model_validate(booking)

    async def mark_as_cancelled(self, booking_id: BookingId) -> BookingOut:
        booking = await self._repository.get_by_id(booking_id)
        if booking is None:
            raise BookingNotFound(booking_id)

        updated_booking = await self._repository.update_status(
            booking, BookingStatus.CANCELLED
        )

        return BookingOut.model_validate(updated_booking)
