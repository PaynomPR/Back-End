from sqlalchemy import or_
from datetime import  datetime

from fastapi import APIRouter,  Depends, HTTPException, status
from fastapi import BackgroundTasks
from database.config import session
from models.users import Code
from schemas.codes import CodeSchema
from routers.mail import send_email_background
code_router = APIRouter()



def create_code_controller(code_data,background_tasks):
    try:
        is_code = (
            session.query(Code)
            .where(or_(Code.code == code_data.code, Code.email == code_data.email))
            .one_or_none()        
        )

        if is_code:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Correo o código ya están registrados.")

        code_query = Code(
            code = code_data.code,

            amount = code_data.amount,
            owner = code_data.owner,
            email = code_data.email,
        )
        send_email_background(background_tasks,subject="Código de activación.",email_to=code_data.email,body={'code': code_data.code, 'title': "Código de activación",'name': code_data.owner})
        session.add(code_query)
        session.commit()
        session.refresh(code_query)

        return {"ok": True, "msg": "El codigo se ha creado con éxito", "result": code_query}
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()

def update_code_controller(code_data, code_id):
    try:
        is_code = (
            session.query(Code)
            .where(Code.id == code_id)
            .first()      
        )

        if not is_code:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Código no encontrado")
            
        is_code.amount = code_data.amount,
        is_code.owner = code_data.owner,   
        session.add(is_code)
        session.commit()
        session.refresh(is_code)   
        return {"ok": True, "msg": "El codigo se ha actualizado con éxito", "result": is_code}
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()


def get_all_codes_controller():
    try:    
        codes_query = session.query(Code).all()

        return {
            "ok": True,
            "msg": "users were successfully retrieved",
            "result": codes_query,
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()

def get_code_by_id_controller(code_id):
    try:    
        code_query = session.query(Code).filter_by(id=code_id).first()

        if not code_query:
            return {"ok": False, "msg": "Código no encontrado", "result": None}

        return {"ok": True, "msg": "Lista de codigos.", "result": code_query}
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()

def disable_code_controller(id):
    try:    
        code_query = session.query(Code).filter(Code.id == id).first()
        code_query.deleted_at = datetime.utcnow()
        code_query.is_deleted = not code_query.is_deleted    
        session.add(code_query)   
        session.commit()  
        session.refresh(code_query)   
        return {"ok": True, "msg": "El codigo se ha deshabilitado con éxito", "result": code_query}
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()