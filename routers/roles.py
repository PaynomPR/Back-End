from fastapi import APIRouter

from database.config import session
from models.users import Role
from schemas.roles import RoleSchema


role_router = APIRouter()


@role_router.post("/")
async def create_role(role: RoleSchema):
    # print("role:", role)
    is_role = session.query(Role).where(Role.role == role.role).one_or_none()

    if is_role:
        return {
            "ok": False,
            "msg": f"Already exists role {role.role}",
            "result": is_role,
        }

    role_query = Role(
        role=role.role,
    )
    session.add(role_query)
    session.commit()
    session.refresh(role_query)
    return {"ok": True, "msg": "role was successfully created", "result": role_query}


@role_router.get("/")
async def get_all_roles():
    roles_query = await session.query(Role).all()
    return {
        "ok": True,
        "msg": "users were successfully retrieved",
        "result": roles_query,
    }


@role_router.get("/{role_id}")
async def get_role_by_id(role_id: int):
    role_query = session.query(Role).filter_by(id=role_id).first()

    if not role_query:
        return {"ok": False, "msg": "user not found", "result": None}

    return {"ok": True, "msg": "user was successfully retrieved", "result": role_query}


@role_router.put("/{role_id}")
async def update_role(role_id: int, new_role: RoleSchema):
    role_query = session.query(Role).filter_by(id=role_id).first()

    if not role_query:
        return {"ok": False, "msg": "role not found", "result": new_role}

    role_query.phone = new_role.role

    session.add(role_query)
    session.commit()
    session.refresh(role_query)

    return {"ok": True, "msg": "user was successfully updated", "result": role_query}
