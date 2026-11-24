from datetime import date, time, timedelta
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, Field

from ._constants import (
    BOOKING_TIME_MAX_HOUR,
    BOOKING_TIME_MIN_HOUR,
    BOOKING_WINDOW_DAYS,
    MAX_GUEST_COUNT,
    MAX_GUEST_NAME_LENGTH,
    MIN_GUEST_COUNT,
    MIN_GUEST_NAME_LENGTH,
)
from .types import BookingId, BookingStatus

type GuestName = Annotated[
    str, Field(min_length=MIN_GUEST_NAME_LENGTH, max_length=MAX_GUEST_NAME_LENGTH)
]
type PhoneNumber = Annotated[str, Field(pattern=r"^\+7\d{10}$")]


def validate_future_date(v: date) -> date:
    today = date.today()
    max_date = today + timedelta(days=BOOKING_WINDOW_DAYS)

    if v < today:
        raise ValueError("Дата не может быть в прошлом")
    if v > max_date:
        raise ValueError(
            f"Дата не может быть дальше чем через {BOOKING_WINDOW_DAYS} дней"
        )
    return v


type BookingDate = Annotated[date, AfterValidator(validate_future_date)]


def validate_hour_precision(v: time) -> time:
    if v.minute != 0 or v.second != 0 or v.microsecond != 0:
        raise ValueError(
            "Время должно быть указано с точностью до часов (минуты и секунды должны быть 0)"
        )
    return v


type BookingTime = Annotated[
    time,
    Field(
        ge=time(hour=BOOKING_TIME_MIN_HOUR),
        le=time(hour=BOOKING_TIME_MAX_HOUR),
        examples=["14:00", "15:00:00", "18:00:00.000Z"],
    ),
    AfterValidator(validate_hour_precision),
]


type GuestCount = Annotated[int, Field(ge=MIN_GUEST_COUNT, le=MAX_GUEST_COUNT)]


class BookingCreate(BaseModel):
    name: GuestName
    phone: PhoneNumber
    booking_date: BookingDate
    booking_time: BookingTime
    guests: GuestCount


class BookingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: BookingId
    name: GuestName = Field(validation_alias="guest_name")
    phone: PhoneNumber = Field(validation_alias="guest_phone")
    booking_date: BookingDate
    booking_time: BookingTime
    guests: GuestCount
    status: BookingStatus


class ErrorResponse(BaseModel):
    detail: str
