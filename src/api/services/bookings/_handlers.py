from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .exceptions import BookingNotFound, SlotAlreadyBooked
from .schemas import ErrorResponse


async def handle_booking_not_found(
    _request: Request,
    _exc: BookingNotFound,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=jsonable_encoder(ErrorResponse(detail="Booking not found")),
    )


async def handle_slot_already_booked(
    _request: Request,
    _exc: SlotAlreadyBooked,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=jsonable_encoder(ErrorResponse(detail="Slot is already booked")),
    )
