from typing import Any
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm


from app.core.security import create_access_token
from app.user.services import authenticate
from app.database import bd 


api_router = APIRouter(tags=["Auth"])

@api_router.post("/login/")
def login(bd_session: Session= Depends(bd.get_bd_session), form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = authenticate(username=form_data.username, password=form_data.password, bd_session=bd_session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    return {
        "access_token": create_access_token(sub=user.username),
        "token_type": "Bearer",
    }