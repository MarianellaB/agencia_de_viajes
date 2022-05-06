from datetime import datetime
from pydantic import BaseModel, constr
from typing import Optional
from enum import Enum
from app.user.schema import User
from app.catalog.schema import Flight


class Booking_Base(BaseModel):
    status: BookingStatus = None
    paymentToken: str
    createdAt: datetime
    checkedIn: bool = False
    bookingReference: constr(max_length=40)

class BookingStatus(str, Enum):
    UNCONFIRMED = 'UNCONFIRMED'
    CONFIRMED = 'CONFIRMED'
    CANCELLED = 'CANCELLED'

class BookingInDBBase(Booking_Base):
    id: int
    flight: Flight
    customer: User
    class Config:
        orm_mode = True

class BookingCreate(Booking_Base):
    pass


class Booking(BookingInDBBase):
    pass

class BookingInDB(BookingInDBBase):
    pass
