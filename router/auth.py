
from fastapi import Depends
from fastapi import HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime, timedelta, timezone

from sqlmodel import Session, select

from db import get_session
from schema import UserWriter, User
from tools import verify_password

# 假设 SECRET_KEY 和 ALGORITHM 如下：
SECRET_KEY = "eac77e4e9a9a767b792779132e84ea37b1f4c31bec56714607f617a3fbdfbd53"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = APIRouter()

# 生成 JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 验证 Token 并返回当前用户
def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        # 查询用户
        db_user = session.exec(select(User).where(User.user_name == username)).first()
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return db_user
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# 登录并返回 token
@app.post("/api/token")
def login_for_access_token(login_user: UserWriter, session: Session = Depends(get_session)):
    query=select(User).where(User.user_name==login_user.user_name)
    # 查找用户
    db_user = session.exec(query).first()
    # 用户不存在或密码不正确
    if not db_user or not verify_password(login_user.user_password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # 生成 JWT Token
    access_token = create_access_token(data={"sub": db_user.user_name})
    return {"access_token": access_token, "token_type": "bearer"}

if __name__ == '__main__':
    print("test")
    user=UserWriter(user_name='xiao',user_password='123456')
    login_for_access_token(user)


