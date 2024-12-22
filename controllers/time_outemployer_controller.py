import bcrypt
from fastapi import APIRouter, HTTPException, status
from fastapi import APIRouter, Depends
from starlette.responses import FileResponse
from fastapi import  Response

from database.config import session
from routers.auth import user_dependency

from models.time_outemployer import TimeOutEmployer
from models.outemployers import OutEmployers
from models.companies import Companies





from schemas.time_outemployer import OutTimeIDShema, OutTimeShema, OutTimeIDShema2
from passlib.context import CryptContext


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
outtime_router = APIRouter()



def create_time_controller(time_data, employer_id):
    try:
        time_query = TimeOutEmployer(        
            regular_hours = time_data.regular_hours,
            regular_min = time_data.regular_min,
            regular_pay = time_data.regular_pay,
            detained = time_data.detained,
            employer_id = employer_id
        )
        session.add(time_query)
        session.commit()
        session.refresh(time_query) 
        
        return {"ok": True, "msg": "El tiempo se creó con éxito", "result": time_query}
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()


def get_time_by_employer_id_controller(employer_id):
    try:
        time_query = session.query(TimeOutEmployer).filter(TimeOutEmployer.employer_id == employer_id).all()

        return {
            "ok": True,
            "msg": "Los empleadores fueron recuperados con éxito",
            "result": time_query,
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()


def delete_employer_controller(time_id, user):
    try:
        # Verificar si la compañía tiene time asociados
        time_query = session.query(TimeOutEmployer).filter(TimeOutEmployer.id == time_id).first()

        
        if time_query:
            session.delete(time_query)
            session.commit()
            return {"ok": True, "msg": "Horas eliminadas con éxito.", "result": time_query}
        else:
            return {"ok": False, "msg": "Empleado no encontrada.", "result": None}
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()

def update_time_controller(time_id, time): 
    try:
        time_query = session.query(TimeOutEmployer).filter_by(id=time_id).first()
        if  not time_query:
            return {"ok": False, "msg": "El tiempo no se actualizo", "result": time_query}
            
        time_query.regular_hours = time.regular_hours
        time_query.regular_min = time.regular_min
        time_query.detained = time.detained
        time_query.regular_pay = time.regular_pay
        session.add(time_query)
        session.commit()
        session.refresh(time_query)
        return {"ok": True, "msg": "El tiempo se actualizó con éxito", "result": time_query}
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()
