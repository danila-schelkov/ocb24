from datetime import date, time

from sqlalchemy import Date, Enum, Index, String, Time, text
from sqlalchemy.orm import Mapped, mapped_column

from api.database import Base

from ._constants import MAX_GUEST_NAME_LENGTH
from .types import BookingId, BookingStatus

BOOKING_UNIQUE_INDEX_NAME = "uq_active_booking_slot"


class BookingModel(Base):
    __tablename__ = "bookings"

    __table_args__ = (
        Index(
            BOOKING_UNIQUE_INDEX_NAME,
            "booking_date",
            "booking_time",
            unique=True,
            postgresql_where=text("status != 'cancelled'"),
            sqlite_where=text("status != 'cancelled'"),
        ),
    )

    id: Mapped[BookingId] = mapped_column(primary_key=True, autoincrement=True)

    guest_name: Mapped[str] = mapped_column(String(MAX_GUEST_NAME_LENGTH))
    # NOTE: phone number is "+7" and 10 more symbols, so 12 symbols in total
    guest_phone: Mapped[str] = mapped_column(String(12), index=True)

    booking_date: Mapped[date] = mapped_column(Date, index=True)
    booking_time: Mapped[time] = mapped_column(Time)
    guests: Mapped[int]

    status: Mapped[BookingStatus] = mapped_column(
        Enum(
            BookingStatus,
            values_callable=lambda obj: [e.value for e in obj],
            native_enum=False,
        ),
        default=BookingStatus.ACTIVE,
        server_default=BookingStatus.ACTIVE,
    )
