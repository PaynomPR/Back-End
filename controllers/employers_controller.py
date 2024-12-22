import bcrypt
from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException, status
from starlette import status
from datetime import  datetime

from database.config import session
from routers.auth import user_dependency

from models.employers import Employers
from models.companies import Companies
from models.time import Time
from utils.time_func import calculete_service_year
from utils.time_func import minutes_to_time, time_to_minutes
from schemas.employee import EmployersSchema
from passlib.context import CryptContext


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
employers_router = APIRouter()



def create_employer_controller(employer_data: Employers, company_id):
    try: 
        vacation_hours = employer_data.vacation_hours
        vacation_hours_monthly = employer_data.vacation_hours_monthly
        if not employer_data.date_admission:
            employer_data.date_admission = datetime.today()
        
        if vacation_hours == 0:
            date_admission = datetime(2017, 1, 26)
            if employer_data.date_admission <= date_admission.date():
                vacation_hours = 10
                vacation_hours_monthly = 130
            else:
                vacation_hours_monthly = 130
                service_years = calculete_service_year(employer_data.date_admission)
                if service_years <= 1:
                    vacation_hours = 4
                elif service_years <=5:
                    vacation_hours = 6               
                elif service_years <=5:
                    vacation_hours = 6
                elif service_years <=15:
                    vacation_hours = 8
                else:
                    vacation_hours = 10                                       
        if (employer_data.salary is None):
            employer_data.salary = 0
        employer_query = Employers(
            last_name=employer_data.last_name,
            mother_last_name=employer_data.mother_last_name,
            first_name=employer_data.first_name,
            middle_name=employer_data.middle_name,
            salary=employer_data.salary,
            company_id=company_id,
            work_hours = employer_data.work_hours,
            employee_type=employer_data.employee_type,
            social_security_number=employer_data.social_security_number,
            marital_status=employer_data.marital_status,
            address=employer_data.address,
            retention_type = int(employer_data.retention_type),
            address_state=employer_data.address_state,
            address_country=employer_data.address_country,
            address_number=employer_data.address_number,
            phone_number=employer_data.phone_number,
            smartphone_number=employer_data.smartphone_number,
            marbete=employer_data.marbete,
            date_marb=employer_data.date_marb,
            is_deleted=False,
            type=employer_data.type,
            clipboard=employer_data.clipboard,
            exec_personal=employer_data.exec_personal,
            choferil=employer_data.choferil,
            regular_time=employer_data.regular_time,
            period_norma=employer_data.period_norma,
            licence=employer_data.licence,
            category_cfse=employer_data.category_cfse,
            gender=employer_data.gender,
            birthday=employer_data.birthday,
            date_admission=employer_data.date_admission,
            date_egress=employer_data.date_egress,
            overtime=employer_data.overtime,
            mealtime=employer_data.mealtime,
            vacation_acum_hours = employer_data.vacation_time,
            sicks_acum_hours = employer_data.sick_time,
            vacation_time=employer_data.vacation_time,
            sick_time=employer_data.sick_time,
            vacation_hours=vacation_hours,
            vacation_hours_monthly=vacation_hours_monthly,
            vacation_date = employer_data.vacation_date,
            sicks_hours=employer_data.sicks_hours,
            sicks_hours_monthly=employer_data.sicks_hours_monthly,
            sicks_date=employer_data.sicks_date,

            number_dependents=employer_data.number_dependents,
            shared_custody=employer_data.shared_custody,
            number_concessions=employer_data.number_concessions,
            veteran=employer_data.veteran,
            type_payroll=employer_data.type_payroll,
            schedule_type=employer_data.schedule_type,
            payment_percentage=employer_data.payment_percentage,
        )
        session.add(employer_query)
        session.commit()
        session.refresh(employer_query)   
        return {"ok": True, "msg": "Empleado creado con exito", "result": employer_query}
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()

def get_all_employers_by_company_id_controller(company_id, user):
    try:
        employer_query = session.query(Employers).filter(Employers.company_id == company_id).order_by(Employers.first_name).all()


        return {
            "ok": True,
            "msg": "Los empleadores fueron recuperados con éxito",
            "result": employer_query,
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()

def get_employer_by_id_controller(employers_id,company_id,user):
    try:
        employer_query = session.query(Employers).join(Companies).filter(Employers.id == employers_id,Employers.company_id == company_id, Companies.id == Employers.company_id,Companies.code_id == user["code"]).first()

        if not employer_query:
            return {"ok": False, "msg": "Empleado no encontrado", "result": None}

        return {"ok": True, "msg": "El empleado fue recuperado con éxito", "result": employer_query} 
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()

def update_employer_controller(employers_id, employer, user):
    try: 
        employer_query = session.query(Employers).filter_by(id=employers_id).first() 
        vacation_hours = employer.vacation_hours
        vacation_hours_monthly = employer.vacation_hours_monthly
        


       
        
                                              
        if (employer.salary is None):
            employer.salary = 0
        employer_query.last_name = employer.last_name
        employer_query.mother_last_name = employer.mother_last_name
        employer_query.first_name = employer.first_name
        employer_query.middle_name = employer.middle_name
        employer_query.employee_type = employer.employee_type
        employer_query.social_security_number = employer.social_security_number
        employer_query.marital_status = employer.marital_status
        employer_query.address = employer.address
        employer_query.retention_type = int(employer.retention_type)
        employer_query.address_state = employer.address_state
        employer_query.address_country = employer.address_country
        employer_query.address_number = employer.address_number
        employer_query.phone_number = employer.phone_number
        employer_query.smartphone_number = employer.smartphone_number
        employer_query.marbete = employer.marbete
        employer_query.date_marb = employer.date_marb
        employer_query.salary = employer.salary
        employer_query.work_hours = employer.work_hours
        employer_query.type = employer.type
        employer_query.clipboard = employer.clipboard
        employer_query.exec_personal = employer.exec_personal
        employer_query.choferil = employer.choferil
        employer_query.regular_time = employer.regular_time
        employer_query.period_norma = employer.period_norma
        employer_query.licence = employer.licence
        employer_query.category_cfse = employer.category_cfse
        employer_query.gender = employer.gender
        employer_query.birthday = employer.birthday
        employer_query.date_admission = employer.date_admission
        employer_query.date_egress = employer.date_egress
      
        employer_query.sick_time = employer.sick_time,
        employer_query.vacation_hours = employer.vacation_hours,
        employer_query.vacation_hours_monthly = employer.vacation_hours_monthly
        employer_query.sicks_hours = employer.sicks_hours
        employer_query.sicks_date =  employer.sicks_date
        employer_query.sicks_hours_monthly = employer.sicks_hours_monthly        
        employer_query.vacation_time = employer.vacation_time        
        employer_query.overtime = employer.overtime
        employer_query.mealtime = employer.mealtime        


        employer_query.number_dependents = employer.number_dependents
        employer_query.shared_custody = employer.shared_custody
        employer_query.number_concessions = employer.number_concessions
        employer_query.veteran = employer.veteran
        employer_query.type_payroll = employer.type_payroll
        employer_query.schedule_type = employer.schedule_type
        employer_query.payment_percentage = employer.payment_percentage
        

        session.add(employer_query)
        session.commit()
        session.refresh(employer_query)

        return {"ok": True, "msg": "El empleado se ha actualizado con exito", "result": employer_query}
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()

def employers_controller(employers_id, user):
    try: 
        employer_query = session.query(Employers).join(Companies).filter(Employers.id == employers_id, Companies.id == Employers.company_id,Companies.code_id == user["code"]).first()
        employer_query.is_deleted = not employer_query.is_deleted    
        employer_query.deleted_at = datetime.utcnow()
        session.add(employer_query)   
        session.commit()  
        session.refresh(employer_query)   
        return {"ok": True, "msg": "El empleador fue el cambio de estado", "result": employer_query}
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()


def delete_employer_controller(employers_id, user):
    try: 
        # Verificar si la compañía tiene time asociados
        time_count = session.query(Time).filter(Time.employer_id == employers_id).count()

        if time_count > 0:   
            return {"ok": False, "msg": "El empleado tiene horas cargadas y no puede ser eliminada.", "result": None}
        # Si no hay empleados, proceder con la eliminación
        employer_query = session.query(Employers).join(Companies).filter(Employers.id == employers_id, Companies.id == Employers.company_id,Companies.code_id == user["code"]).first()
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