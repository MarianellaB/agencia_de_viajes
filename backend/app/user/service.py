from typing import List, Optional
from sqlalchemy.orm import Session
from . import models
from . import schema
from app.core import hashing
from app.booking import models as booking_models

async def get_all_users(bd_session: Session) -> List[models.User]:
    users = bd_session.query(models.User).all()
    return users

async def get_user_by_id(user_id: int, bd_session: Session) -> Optional[models.User]:
    user_info = bd_session.query(models.User).get(user_id)
    return user_info

async def new_user_register(user_in: schema.UserCreate, bd_session: Session) -> models.User:
    new_user = models.User(**user_in.dict())
    bd_session.add(new_user)
    bd_session.commit()
    bd_session.refresh(new_user)
    return new_user

async def delete_user_by_id(user_id: int, bd_session: Session):
    booking = bd_session.query(booking_models.Booking).filter(booking_models.Booking.customer_id == user_id).all()
    if booking:
        for b in booking:
            bd_session.delete(b)
    bd_session.commit()
    bd_session.query(models.User).filter(models.User.id == user_id).delete()
    bd_session.commit()

async def update_user(user_id: int, user: schema.UserUpdate, bd_session: Session):
    updated_user = models.User(**user.dict())
    bd_session.query(models.User).filter(models.User.id == user_id).update(
                                            {
                                                models.User.id: user_id,
                                                models.User.fullname: updated_user.fullname,
                                                models.User.username: updated_user.username,
                                                models.User.password: updated_user.password
                                            }, synchronize_session=False)
    bd_session.commit()
    return updated_user

def authenticate(*, username: str, password: str, bd_session = Session) -> Optional[models.User]:
    user = bd_session.query(models.User).filter(models.User.username == username).first()

    if not user:
        return None

    if not hashing.verify_password(password, user.password):
        return None
    
    return user