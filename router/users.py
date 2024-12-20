from fastapi import HTTPException
from fastapi import Depends
from schema import User, UserWriter
from sqlmodel import Session,select
from db import get_session
from fastapi import APIRouter
from tools import hash_password
app = APIRouter()

@app.post("/api/users")
def create_user(user:UserWriter,session:Session=Depends(get_session)) -> User:
    new_user=User(user_name=user.user_name, password_hash=hash_password(user.user_password))
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user