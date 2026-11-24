from fastapi import Request, status
from fastapi.responses import JSONResponse

from .exceptions import BookingNotFound, SlotAlreadyBooked


async def handle_booking_not_found(
    _request: Request,
    _exc: BookingNotFound,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Booking not found"},
    )


async def handle_slot_already_booked(
    _request: Request,
    _exc: SlotAlreadyBooked,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "Slot is already booked"},
    )
