from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from starlette import status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database.config import Session as local
from models.users import User, Code, Role, UserCode
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy import or_
from datetime import datetime, timedelta


auth_router = APIRouter()

SECRET_KEY = "DEMO"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_db():
    db = local()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@auth_router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    # print({"form_data": form_data, "db": db})

    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña no son validos.",
        )

    token = create_access_token(
        user.email, user.id, user.codes.id, user.name, user.role_id, timedelta(days=3)
    )

    return {"access_token": token, "token_type": "bearer", "name": user.name}


def authenticate_user(username: str, password: str, db):
    user = (
        db.query(User)
        .filter(
            or_(User.email == username, User.phone == username),
            User.is_deleted == False,
        )
        .one_or_none()
    )

    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user


def create_access_token(
    username: str,
    user_id: int,
    code: str,
    name: str,
    role_id: int,
    expires_delta: timedelta,
):
    encode = {
        "sub": username,
        "id": user_id,
        "name": name,
        "code": code,
        "role_id": role_id,
    }
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        role_id: int = payload.get("role_id")
        code: str = payload.get("code")
        name: int = payload.get("name")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña no son validos.",
            )
        return {
            "username": username,
            "id": user_id,
            "name": name,
            "code": code,
            "role_id": role_id,
        }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no valido."
        )


user_dependency = Annotated[dict, Depends(get_current_user)]


@auth_router.get("/")
async def currentUser(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Fallo en la autenticación.")

    profile = (
        db.query(User)
        .join(Role)
        .join(UserCode)
        .filter(
            User.role_id == Role.id,
            User.id == user["id"],
            User.id == UserCode.user_id,
            User.is_deleted == False,
        )
        .one_or_none()
    )

    return {"profile": profile, "user": user}
