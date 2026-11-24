from enum import StrEnum

type BookingId = int


class BookingStatus(StrEnum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
