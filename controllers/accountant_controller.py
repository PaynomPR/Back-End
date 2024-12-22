from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from datetime import  datetime

from database.config import session
from models.users import Role, User , Code , UserCode
from models.accountant import Accountant
from models.time import Time

from schemas.accountant import Accountants
from passlib.context import CryptContext
from routers.auth import user_dependency

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
accountant_router = APIRouter()



def create_accountant_controller(accountants_data, user):
    try: 
        is_user = (
            session.query(User)
            .where(User.email == accountants_data.email or User.phone == accountants_data.phone)
            .one_or_none()
        )
    

        if is_user:
            # Usamos una lista para guardar los mensajes de error
            errores = []

            # Comprobamos si el email o el teléfono coinciden con el usuario existente
            if is_user.email == accountants_data.email:
                errores.append(f"email: {accountants_data.email}")

            if is_user.phone == accountants_data.phone:
                errores.append(f"phone: {accountants_data.phone}")

            # Unimos los mensajes de error con "and" si hay más de uno
            msg = " and ".join(errores)

            # Usamos una expresión ternaria para asignar el valor de ok
            ok = False if errores else True

            # Devolvemos el resultado como un diccionario
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="El Email y Telefono ya estan registrados.")

        hashed_password = bcrypt_context.hash("123456")

        user_query = User(
            name=accountants_data.name,
            lastname=accountants_data.first_last_name,
            email=accountants_data.email,
            phone=accountants_data.phone,
            password=hashed_password,
            
            role_id=3,
        )
        session.add(user_query)
        session.commit()
        accountant_query = Accountant(
            user_id=user_query.id,
            name = user_query.name,
            code_id=user["code"],
            email=accountants_data.email,
            middle_name=accountants_data.middle_name,
            first_last_name = accountants_data.first_last_name,
            second_last_name = accountants_data.second_last_name,
            company = accountants_data.company,
            phone = accountants_data.phone,
            country = accountants_data.country,
            state = accountants_data.state,
            zip_code = accountants_data.zip_code,
            physical_address = accountants_data.physical_address,
            physical_country = accountants_data.physical_country,
            physical_state = accountants_data.physical_state,
            physical_zip_code = accountants_data.physical_zip_code,
            address = accountants_data.address,
            identidad_ssa = accountants_data.identidad_ssa,
            identidad_bso = accountants_data.identidad_bso,
            identidad_efile = accountants_data.identidad_efile,
            
            employer_insurance_number = accountants_data.employer_insurance_number    
        )
        code_query = UserCode(
            user_id=user_query.id,
            code_id=user["code"],
        )    
        session.add(accountant_query)    
        session.add(code_query)
        session.commit()
        session.refresh(user_query)
        session.refresh(accountant_query)
        session.refresh(code_query)
        return {"ok": True, "msg": "Usuario creado exitosamente", "result": user_query}
    except HTTPException as e:
        raise e
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Se ha producido un error {str(e)}")
    finally:
        session.close()


def get_all_accountants_controller(user):
    try: 
        accountant_query = session.query(Accountant).join(User).filter(user['code'] == Accountant.code_id, User.id == Accountant.user_id ).all()
        return {
            "ok": True,
            "msg": "Contador se recuperaron con éxito",
            "result": accountant_query,
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()

def get_accountant_controller(user, id):
    try: 
        accountant_query = session.query(Accountant).join(User).filter(Accountant.id == id, User.id == Accountant.user_id ).first()
        return {
            "ok": True,
            "msg": "Contador se recuperaron con éxito",
            "result": accountant_query,
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()

def update_accountant_controller(accountants_data, user, id):
    try:
        accountant_query = session.query(Accountant).join(User).filter(Accountant.id == id, User.id == Accountant.user_id ).first() 
        accountant_query.name = accountants_data.name,
        accountant_query.code_id=user["code"],
        accountant_query.email=accountants_data.email,
        accountant_query.middle_name=accountants_data.middle_name,
        accountant_query.first_last_name = accountants_data.first_last_name,
        accountant_query.second_last_name = accountants_data.second_last_name,
        accountant_query.company = accountants_data.company,
        accountant_query.phone = accountants_data.phone,
        accountant_query.country = accountants_data.country,
        accountant_query.state = accountants_data.state,
        accountant_query.zip_code = accountants_data.zip_code,
        accountant_query.physical_address = accountants_data.physical_address,
        accountant_query.physical_country = accountants_data.physical_country,
        accountant_query.physical_state = accountants_data.physical_state,
        accountant_query.physical_zip_code = accountants_data.physical_zip_code,
        accountant_query.identidad_ssa = accountants_data.identidad_ssa,
        accountant_query.identidad_bso = accountants_data.identidad_bso,
        accountant_query.identidad_efile = accountants_data.identidad_efile,
        accountant_query.address = accountants_data.address,
        accountant_query.employer_insurance_number = accountants_data.employer_insurance_number    
        session.add(accountant_query)   
        session.commit()  
        session.refresh(accountant_query)   
        return {"ok": True, "msg": "El usuario se ha actualizado con éxito", "result": accountant_query}
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()


def disable_accountant_controller(id):
    try: 
        accountant_query = session.query(Accountant).join(User).filter(Accountant.id == id, User.id == Accountant.user_id ).first()
        accountant_query.deleted_at = datetime.utcnow()
        accountant_query.is_deleted = not accountant_query.is_deleted    
        session.add(accountant_query)   
        session.commit()  
        session.refresh(accountant_query)   
        return {"ok": True, "msg": "El usuario se ha deshabilitado con éxito", "result": accountant_query}
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()

def delete_accountant_controller(accountant_id):
    try: 
        # Verificar si el contador tiene time asociados
        time_count = session.query(Time).filter(Time.accountant_id == accountant_id).count()

        if time_count > 0:   
            return {"ok": False, "msg": "El Contador tiene horas cargadas y no puede ser eliminada.", "result": None}
        # Si no hay empleados, proceder con la eliminación
        accountant_query = session.query(Accountant).filter(Accountant.id == accountant_id).first()
        if accountant_query:
            session.delete(accountant_query)
            session.commit()
            return {"ok": True, "msg": "Empleado eliminada con éxito.", "result": accountant_query}
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