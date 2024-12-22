from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from database.config import session
from models.users import Role, User , Code , UserCode


from schemas.users import UserSchema, UserUpdateSchema
from passlib.context import CryptContext


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
user_router = APIRouter()


@user_router.post("/")
async def create_user(user_data: UserSchema):
    is_user = (
        session.query(User)
        .where(User.email == user_data.email or User.phone == user_data.phone)
        .one_or_none()
    )

    is_code = session.query(Code).where(Code.code == user_data.user_code,Code.is_deleted == False,user_data.email == Code.email).one_or_none()

    if not is_code:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Codigo no es valido."
        )

    if is_user:
        # Usamos una lista para guardar los mensajes de error
        errores = []

        # Comprobamos si el email o el teléfono coinciden con el usuario existente
        if is_user.email == user_data.email:
            errores.append(f"email: {user_data.email}")

        if is_user.phone == user_data.phone:
            errores.append(f"phone: {user_data.phone}")

        # Unimos los mensajes de error con "and" si hay más de uno
        msg = " and ".join(errores)

        # Usamos una expresión ternaria para asignar el valor de ok
        ok = False if errores else True

        # Devolvemos el resultado como un diccionario
        return {
            "ok": ok,
            "msg": f"Already exists user with {msg}" if msg else "",
            "result": is_user,
        }

    hashed_password = bcrypt_context.hash(user_data.password)

    user_query = User(
        name=user_data.name,
        lastname=user_data.lastname,
        email=user_data.email,
        phone=user_data.phone,
        password=hashed_password,
        role_id=2,
    )
    session.add(user_query)
    session.commit()
    code_query = UserCode(
        user_id=user_query.id,
        code_id=is_code.id,
    )    
    session.add(code_query)
    session.commit()
    session.refresh(user_query)
    session.refresh(code_query)
    return {"ok": True, "msg": "user was successfully created", "result": user_query}


@user_router.get("/")
async def get_all_users():
    users_query = session.query(User).join(Role).filter(User.role_id == Role.id).all()

    return {
        "ok": True,
        "msg": "users were successfully retrieved",
        "result": users_query,
    }


@user_router.get("/{user_id}")
async def get_user_by_id(user_id: int):
    user_query = session.query(User).filter_by(id=user_id).first()

    if not user_query:
        return {"ok": False, "msg": "user not found", "result": None}

    return {"ok": True, "msg": "user was successfully retrieved", "result": user_query}


@user_router.put("/{user_id}")
async def update_user(user_id: int, new_user_data: UserUpdateSchema):
    user_query = session.query(User).filter_by(id=user_id).first()

    if not user_query:
        return {"ok": False, "msg": "user not found", "result": new_user_data}
    if new_user_data.phone:
        user_query.phone = new_user_data.phone
    if new_user_data.password:
        user_query.password = new_user_data.password

    session.add(user_query)
    session.commit()
    session.refresh(user_query)

    return {"ok": True, "msg": "user was successfully updated", "result": user_query}
