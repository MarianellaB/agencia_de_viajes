from sqlalchemy.orm import Session
from . import models
from typing import Optional


async def verify_bookingreference_exist(bookingreference: str, bd_session: Session) -> Optional[models.User]:
    return bd_session.query(models.Booking).filter(models.Booking.bookingReference == bookingreference).first()