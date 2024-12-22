import bcrypt
from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from datetime import  datetime

from database.config import session
from routers.auth import user_dependency

from models.outemployers import OutEmployers
from models.companies import Companies
from models.time_outemployer import TimeOutEmployer


from schemas.outemployers import OutEmployersSchema
from passlib.context import CryptContext


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
outemployers_router = APIRouter()


def create_employer_controller(employer_data, company_id):
    try: 
        outemployer_query = OutEmployers(        
            last_name = employer_data.last_name,
            mother_last_name = employer_data.mother_last_name,
            first_name = employer_data.first_name,
            middle_name = employer_data.middle_name,
            company_id =  company_id,
            regular_pay = employer_data.regular_pay,
            account_number = employer_data.account_number,
            email = employer_data.email,
            type_entity = employer_data.type_entity,
            withholding = employer_data.withholding,
            employer_id = employer_data.employer_id,
            address = employer_data.address,
            address_state = employer_data.address_state,
            address_country = employer_data.address_country,
            address_number = employer_data.address_number,
            phone_number = employer_data.phone_number,
            smartphone_number = employer_data.smartphone_number,
            bank_account = employer_data.bank_account,
            merchant_register= employer_data.merchant_register,
            is_deleted = False,
            
            
            
            gender = employer_data.gender,
            birthday = employer_data.birthday,
            
        )   
        session.add(outemployer_query)
        session.commit()
        session.refresh(outemployer_query)   
        return {"ok": True, "msg": "Empleado creado  con exito", "result": outemployer_query}
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()


def get_all_company_and_employer_controller(user,company_id,employers_id):
    try: 
        companies_query = session.query(OutEmployers, Companies).join(Companies, onclause=Companies.id == company_id).filter(Companies.code_id == user["code"], OutEmployers.id == employers_id).first()
        employer, company = companies_query # Desempaquetar la tupla  
        simple_query = session.query(TimeOutEmployer).filter(TimeOutEmployer.employer_id == employers_id).all()
        outemployer_query = session.query(OutEmployers).join(Companies).filter(OutEmployers.company_id == company_id, Companies.id == OutEmployers.company_id,Companies.code_id == user["code"]).all()
        return {"ok": True, "msg": "", "result": {"company": company, "employer": employer,"time": simple_query,"employers": outemployer_query}}
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()

def get_all_outemployers_by_company_id_controller(company_id,user):
    try:
        outemployer_query = session.query(OutEmployers).join(Companies).filter(OutEmployers.company_id == company_id, Companies.id == OutEmployers.company_id,Companies.code_id == user["code"]).all()

        return {
            "ok": True,
            "msg": "Los empleadores fueron recuperados con éxito",
            "result": outemployer_query,
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()


def get_employer_by_id_controller(outemployers_id,company_id,user): 
    try:    
        outemployer_query = session.query(OutEmployers).join(Companies).filter(OutEmployers.id == outemployers_id,OutEmployers.company_id == company_id, Companies.id == OutEmployers.company_id,Companies.code_id == user["code"]).first()

        if not outemployer_query:
            return {"ok": False, "msg": "Empleado no encontrado", "result": None}

        return {"ok": True, "msg": "El empleador se recuperó con éxito", "result": outemployer_query}
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()

def update_employer_controller(outemployers_id, employer, user):
    try:
        outemployer_query = session.query(OutEmployers).filter_by(id=outemployers_id).first()  
        outemployer_query.last_name = employer.last_name
        outemployer_query.mother_last_name = employer.mother_last_name
        outemployer_query.first_name = employer.first_name
        outemployer_query.middle_name = employer.middle_name    
        outemployer_query.address = employer.address   
        outemployer_query.regular_pay = employer.regular_pay
        outemployer_query.withholding = employer.withholding 
        outemployer_query.employer_id = employer.employer_id
        outemployer_query.address_state = employer.address_state
        outemployer_query.address_country = employer.address_country
        outemployer_query.address_number = employer.address_number
        outemployer_query.phone_number = employer.phone_number
        outemployer_query.type_entity = employer.type_entity
        outemployer_query.smartphone_number = employer.smartphone_number   
        outemployer_query.gender = employer.gender
        outemployer_query.birthday = employer.birthday   
        outemployer_query.merchant_register = employer.merchant_register
        outemployer_query.account_number = employer.account_number
        outemployer_query.bank_account = employer.bank_account
        session.add(outemployer_query)
        session.commit()
        session.refresh(outemployer_query)

        return {"ok": True, "msg": "Empleado actualizado con exito", "result": outemployer_query}
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()

def outemployers_delete_controller(outemployers_id, user):
    try:
        outemployer_query = session.query(OutEmployers).join(Companies).filter(OutEmployers.id == outemployers_id, Companies.id == OutEmployers.company_id,Companies.code_id == user["code"]).first()   
        outemployer_query.is_deleted = not outemployer_query.is_deleted    
        outemployer_query.deleted_at = datetime.utcnow()
        session.add(outemployer_query)   
        session.commit()  
        session.refresh(outemployer_query)   
        return {"ok": True, "msg": "El empleado cambio de estado con exito", "result": outemployer_query}
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()


def delete_outemployer_controller(employers_id, user):
    try:
        employer_query = session.query(OutEmployers).join(Companies).filter(OutEmployers.id == employers_id, Companies.id == OutEmployers.company_id,Companies.code_id == user["code"]).first()
        if employer_query:
            session.delete(employer_query)
            session.commit()
            return {"ok": True, "msg": "Empleado eliminada con éxito.", "result": employer_query}
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