from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi.responses import PlainTextResponse
from app.core import security
from app.database import bd
from . import schema
from . import services
from . import validation

api_router = APIRouter(tags = ['User'])


@api_router.get('/user/{user_id}', response_model = schema.User)
async def get_user_by_id(user_id: int, bd_session : Session = Depends(bd.get_bd_session)):
    user_info = await services.get_user_by_id(user_id, bd_session)
    if not user_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Non-existent user")
    return user_info

@api_router.get('/user/', response_model = List[schema.User])
async def get_all_users(bd_session: Session = Depends(bd.get_bd_session)):
    return await services.get_all_users(bd_session)

@api_router.post('/user/', status_code=status.HTTP_201_CREATED, response_model=schema.User)
async def create_user_registration(user_in: schema.UserCreate, bd_session: Session = Depends(bd.get_bd_session)):
    existingusername = await validation.verify_username_exist(user_in.username, bd_session)
    if existingusername:
        raise HTTPException(status_code=400, detail="The user with this username already exists in the system.")
    new_user = await services.new_user_register(user_in, bd_session)
    return new_user

@api_router.put('/user/{user_id}', status_code = status.HTTP_201_CREATED)
async def update_user(user_id: int, user_in: schema.UserUpdate, bd_session: Session = Depends(bd.get_bd_session),
                      current_user: schema.User = Depends(security.get_current_user)):
    existinguser = await services.get_user_by_id(user_id, bd_session)
    if not existinguser:
        raise HTTPException(status_code=404, detail = "Non-existent user")
    existingusername = await validation.verify_username_exist(user_in.username, bd_session)
    if existingusername:
        raise HTTPException(status_code=400, detail="The user with this username already exists in the system.")
    new_user = await services.update_user(user_id, user_in, bd_session)
    return new_user

@api_router.delete('/user/{user_id}', status_code=status.HTTP_200_OK, response_class=PlainTextResponse)
async def delete_user_by_id(user_id: int, bd_session: Session = Depends(bd.get_bd_session),
                            current_user: schema.User = Depends(security.get_current_user)):
    existinguser = await services.get_user_by_id(user_id, bd_session)
    if not existinguser:
        raise HTTPException(status_code=404, detail = "Non-existent user")
    deleted_user = await services.delete_user_by_id(user_id, bd_session)
    return "THE USER AND ALL HIS BOOKINGS HAVE BEEN SUCCESSFULLY DELETED."