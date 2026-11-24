from collections.abc import Sequence
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Query, status

from ._dependencies import BookingServiceDep
from .schemas import BookingCreate, BookingId, BookingOut

router = APIRouter(prefix="/bookings")


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def _create_booking(
    new_booking: BookingCreate, service: BookingServiceDep
) -> BookingOut:
    return await service.create_booking(new_booking)


@router.get("")
async def _list_bookings(
    service: BookingServiceDep,
    booking_date: Annotated[date | None, Query(alias="date")] = None,
) -> Sequence[BookingOut]:
    return await service.list_bookings(booking_date)


@router.get("/{id}")
async def _get_booking(id: BookingId, service: BookingServiceDep) -> BookingOut:
    return await service.get_booking(id)


@router.delete("/{id}")
async def _delete_booking(id: BookingId, service: BookingServiceDep) -> BookingOut:
    return await service.mark_as_cancelled(id)
