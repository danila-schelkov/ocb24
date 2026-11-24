from collections.abc import Sequence
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Query, status

from ._dependencies import BookingServiceDep
from .schemas import BookingCreate, BookingId, BookingOut, ErrorResponse

router = APIRouter(prefix="/bookings")


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "model": ErrorResponse,
            "description": "Бронь с указанной датой и временем уже существует",
        }
    },
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


@router.get(
    "/{id}",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Бронь с указанным ID не найдена",
        }
    },
)
async def _get_booking(id: BookingId, service: BookingServiceDep) -> BookingOut:
    return await service.get_booking(id)


@router.delete(
    "/{id}",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Бронь с указанным ID не найдена",
        }
    },
)
async def _delete_booking(id: BookingId, service: BookingServiceDep) -> BookingOut:
    return await service.mark_as_cancelled(id)
