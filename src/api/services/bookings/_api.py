from fastapi import FastAPI

from ._handlers import handle_booking_not_found, handle_slot_already_booked
from ._router import router
from .exceptions import BookingNotFound, SlotAlreadyBooked


def register_bookings_service(app: FastAPI) -> None:
    app.include_router(router)

    _register_bookings_exception_handlers(app)


def _register_bookings_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(BookingNotFound, handle_booking_not_found)
    app.add_exception_handler(SlotAlreadyBooked, handle_slot_already_booked)
