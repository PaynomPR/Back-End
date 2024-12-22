import bcrypt
from datetime import datetime

from sqlalchemy.orm import aliased

from fastapi import APIRouter, HTTPException, status
from database.config import session
from models.periods import Period, PeriodType
from schemas.companies import CompaniesSchema, CompaniesWithEmployersSchema
from sqlalchemy.orm import Session
from models.periods import Period
from models.companies import Companies
from models.employers import Employers
from models.taxes import Taxes
from sqlalchemy.orm import joinedload
from models.time import Time
from models.payments import Payments
from collections import defaultdict
from datetime import datetime
from typing import Dict, Any
from routers.auth import user_dependency
from sqlalchemy import func

companies_router = APIRouter()

def create_company_controller(companie_data, user):
    try:  
        companie_query = Companies(
            name=companie_data.name,
            commercial_register=companie_data.commercial_register,
            jurisdiction=companie_data.jurisdiction,
            accountant_id=companie_data.accountant_id,
            email=companie_data.email,
            employed_contribution=companie_data.employed_contribution,
            contact=companie_data.contact,
            choferil_number=companie_data.choferil_number,
            special_contribution=companie_data.special_contribution,
            contact_number=companie_data.contact_number,
            website=companie_data.website,
            w2_first_control=companie_data.w2_first_control,
            w2_last_control=companie_data.w2_last_control,
            sp_first_control=companie_data.sp_first_control,
            sp_last_control=companie_data.sp_last_control,
            number_patronal=companie_data.number_patronal,
            vacation_hours = companie_data.vacation_hours,
            vacation_date = companie_data.vacation_date,
            sicks_hours = companie_data.sicks_hours,
            sicks_date = companie_data.sicks_date,
            coml=companie_data.coml,
            date_close=companie_data.date_close,
            postal_address=companie_data.postal_address,
            zipcode_postal_address=companie_data.zipcode_postal_address,
            country_postal_address=companie_data.country_postal_address,
            state_postal_addess=companie_data.state_postal_addess,
            physical_address=companie_data.physical_address,
            zipcode_physical_address=companie_data.zipcode_physical_address,
            country_physical_address=companie_data.country_physical_address,
            state_physical_address=companie_data.state_physical_address,
            phone_number=companie_data.phone_number,
            fax_number=companie_data.fax_number,
            industrial_code=companie_data.industrial_code,
            payer=companie_data.payer,
            desem=companie_data.desem,
            disabled_percent=companie_data.disabled_percent,
            unemployment_percentage=companie_data.unemployment_percentage,
            code_id=user["code"],
            polize_number=companie_data.polize_number,
            driver_code=companie_data.driver_code,
            driver_rate=companie_data.driver_rate,
            tax_authority_first_control =companie_data.tax_authority_first_control, 
            tax_authority_second_control =companie_data.tax_authority_second_control
        )

        session.add(companie_query)

        session.commit()

        session.refresh(companie_query)
        return {"ok": True, "msg": "", "result": companie_query}
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()


def get_all_companies_controller(user):
    try:
        companies_query = (
            session.query(Companies)
            .options(joinedload(Companies.employers).joinedload(Employers.time))
            .filter(Companies.code_id == user["id"]).order_by(Companies.name)
            .all()
        )


        # Filtrar manualmente los empleados con is_deleted false para cada compañía
        for company in companies_query:
            company.employers = [employer for employer in company.employers if not employer.is_deleted]
            
        return companies_query
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
           

def calculate_total_times(periods_data) -> Dict[str, Any]:
    total_times_by_employee = defaultdict(lambda: defaultdict(float))
    
    for period in periods_data:
        for time in period["times"]:
            employer_id = time["employer_id"]
            total_times_by_employee[employer_id]["medicare"] += time["medicare"]
            total_times_by_employee[employer_id]["inability"] += time["inability"]
            total_times_by_employee[employer_id]["meal_time"] += time_to_hours(time["meal_time"])
            total_times_by_employee[employer_id]["holiday_time"] += time_to_hours(time["holiday_time"])
            total_times_by_employee[employer_id]["sick_time"] += time_to_hours(time["sick_time"])
            total_times_by_employee[employer_id]["vacation_time"] += time_to_hours(time["vacation_time"])
            # Añadir cualquier otro campo que necesites sumar

    return {k: dict(v) for k, v in total_times_by_employee.items()}

def time_to_hours(time_str: str) -> float:
    if 'hours' in time_str:
        return float(time_str.split()[0])
    hours, minutes = map(int, time_str.split(':'))
    return hours + minutes / 60

def get_all_company_and_employer_controller(user, company_id, employers_id,year):    
    try:
        # Filtramos la compañía y el empleador
        companie_query = session.query(Companies).filter(Companies.id == company_id).first()
        if not companie_query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
        
        employer_query = session.query(Employers).filter(Employers.id == employers_id).first()
        if not employer_query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employer not found")
        type_period = 0
        # Obtener el period_id del payment_type del modelo time
        if (employer_query.period_norma == 1):
            type_period = PeriodType.WEEKLY
        elif (employer_query.period_norma == 2):
            type_period = PeriodType.BIWEEKLY
        elif (employer_query.period_norma == 4):
            type_period = PeriodType.MONTHLY
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment type not found")
        
        # Consulta para obtener todos los periodos del año 2024 y con period_start mayor que la fecha actual
        periods_query = session.query(Period).filter(
        Period.year == year,
        Period.is_deleted == False,
        Period.period_type == type_period,
        datetime.now() >  Period.period_start
        ).all()

        # Consulta para obtener todos los empleados
        employers_query = session.query(Employers).filter(Employers.company_id == company_id).all()
        taxes_query = session.query(Taxes).filter(Taxes.company_id == company_id).all()

        # Consulta con joins para obtener todos los datos necesarios
        results = (session.query(Companies, Employers, Time, Taxes)
        .select_from(Companies)
        .join(Employers, Employers.company_id == Companies.id)
        .join(Time, Time.employer_id == Employers.id, isouter=True)  # LEFT JOIN
        .join(Taxes, Taxes.company_id == Companies.id , isouter=True)
        .filter(Companies.id == company_id)
        .filter(Employers.id == employers_id)
        .all())

        # Consulta para obtener todos los payments
        payments_query = session.query(Payments).filter(
        Payments.time_id.in_([t.id for row in results if row[2] for t in [row[2]]])
        ).all()

        if not results:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")

        # Organizar los datos en un formato estructurado
        times_data = []
        taxes_data = []
        payments_data = {}

        for row in results:
            companies, employers, time, taxes = row
            
            # Añadir tiempos
            if time:
                times_data.append(time)

            # Añadir impuestos
            taxes_data.append(taxes)

        # Organizar payments por time_id
        for payment in payments_query:
            if payment.time_id not in payments_data:
                payments_data[payment.time_id] = []
            payments_data[payment.time_id].append({
                "id": payment.id,
                "name": payment.name,
                "amount": payment.amount,
                "value": payment.value,
                "is_active": payment.is_active,
                "required": payment.required,
                "type_taxe": payment.type_taxe,
                "type_amount": payment.type_amount,
                "is_deleted": payment.is_deleted,
                "deleted_at": payment.deleted_at,
                "created_at": payment.created_at,
                "update_at": payment.update_at
            })

        # Crear una lista de periodos, algunos podrían no tener datos de Time
        periods_data = [
            {
                "year": period.year,
                "period_number": period.period_number,
                "period_start": period.period_start,
                "period_end": period.period_end,
                "period_type": period.period_type,
                "is_deleted": period.is_deleted,
                "id": period.id,
                "created_at": period.created_at,
                "deleted_at": period.deleted_at,
                "update_at": period.update_at,
                "times": [
                    {
                        **t.__dict__,
                        "payment": payments_data.get(t.id, [])
                    }
                    for t in times_data if t.period_id == period.id
                ]
            }
            for period in periods_query
        ]
       

        # Calcular la sumatoria de tiempos por empleado
        total_times_by_employee = calculate_total_times(periods_data)

        return {
            "ok": True,
            "msg": "",
            "result": {
                "company": companie_query,
                "employer": employer_query,
                "periods": periods_data,
                "taxes": taxes_query,
                "employers": employers_query,
                "total_times_by_employee": total_times_by_employee
            },
        }

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Se ha producido un error {str(e)}")
    finally:
        session.close()


def get_talonario_controller(user, company_id, employers_id, period_id):
    try:
        companies_query = (
            session.query(Employers, Companies)
            .join(Companies, onclause=Companies.id == company_id)
            .filter(Employers.id == employers_id)
            .first()
        )
        employer, company = companies_query  # Desempaquetar la tupla
        time_query = (
            session.query(Time)
            .filter(Time.employer_id == employers_id, Time.period_id == period_id)
            .first()
        )
        
        if time_query:
            taxes_query = session.query(Payments).filter(Payments.time_id == time_query.id).all()
        else:
            taxes_query = []

        return {
            "ok": True,
            "msg": "",
            "result": {
                "company": company,
                "employer": employer,
                "time": time_query,
                "taxes": taxes_query,
            },
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()


def get_company_controller(user, companies_id):
    try:
        companies_query = (
            session.query(Companies)
            .filter(Companies.code_id == user["code"], Companies.id == companies_id)
            .one_or_none()
        )

        return {
            "ok": True,
            "msg": "Companies were successfully retrieved",
            "result": companies_query,
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()

def get_companies_by_id_controller(companies_id):
    try:
        company_query = session.query(Companies).filter_by(id=companies_id).first()

        if not company_query:
            return {"ok": False, "msg": "Compañia no encontrada", "result": None}

        return {
            "ok": True,
            "msg": "Compañias encontrada",
            "result": company_query,
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()

def update_company_controller(companies_id, company_data):
    try:    
        company_query = session.query(Companies).filter_by(id=companies_id).one_or_none()

        if not company_query:
            return {"ok": False, "msg": "Compañias no encontradas"}
        company_query.name = company_data.name
        company_query.commercial_register = company_data.commercial_register
        company_query.jurisdiction = company_data.jurisdiction
        company_query.accountant_id = company_data.accountant_id
        company_query.email = company_data.email
        company_query.choferil_number = company_data.choferil_number
        company_query.contact = company_data.contact
        company_query.special_contribution = company_data.special_contribution
        company_query.contact_number = company_data.contact_number
        company_query.website = company_data.website
        company_query.employed_contribution = company_data.employed_contribution
        company_query.postal_address = company_data.postal_address
        company_query.zipcode_postal_address = company_data.zipcode_postal_address
        company_query.country_postal_address = company_data.country_postal_address
        company_query.state_postal_addess = company_data.state_postal_addess
        company_query.number_patronal = company_data.number_patronal
        company_query.coml = company_data.coml
        company_query.date_close= company_data.date_close
        company_query.vacation_hours = company_data.vacation_hours
        company_query.vacation_date = company_data.vacation_date
        company_query.sicks_hours = company_data.sicks_hours
        company_query.sicks_date = company_data.sicks_date
        company_query.w2_first_control=company_data.w2_first_control
        company_query.w2_last_control=company_data.w2_last_control
        company_query.sp_first_control=company_data.sp_first_control
        company_query.sp_last_control=company_data.sp_last_control
        company_query.physical_address = company_data.physical_address
        company_query.zipcode_physical_address = company_data.zipcode_physical_address
        company_query.country_physical_address = company_data.country_physical_address
        company_query.state_physical_address = company_data.state_physical_address
        company_query.phone_number = company_data.phone_number
        company_query.fax_number = company_data.fax_number
        company_query.industrial_code = company_data.industrial_code
        company_query.payer = company_data.payer
        company_query.desem = company_data.desem
        company_query.disabled_percent = company_data.disabled_percent
        company_query.unemployment_percentage = company_data.unemployment_percentage

        company_query.polize_number = company_data.polize_number
        company_query.driver_code = company_data.driver_code
        company_query.driver_rate = company_data.driver_rate
        company_query.tax_authority_first_control = company_data.tax_authority_first_control
        company_query.tax_authority_second_control = company_data.tax_authority_second_control
        

        session.add(company_query)
        session.commit()
        session.refresh(company_query)

        return {
            "ok": True,
            "msg": "Compañias se actualizó con éxito",
            "result": company_query,
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()



def disable_company_controller(id):
    try:
        companie_query = session.query(Companies).filter(Companies.id == id).first()

        companie_query.is_deleted = not companie_query.is_deleted
        companie_query.deleted_at = datetime.utcnow()
        session.add(companie_query)
        session.commit()
        session.refresh(companie_query)
        return {"ok": True, "msg": "", "result": companie_query}
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()


def delete_company_controller(id):
    try:
        # Verificar si la compañía tiene empleados asociados
        employee_count = session.query(Employers).filter(Employers.company_id == id).count()

        if employee_count > 0:
            return {
                "ok": False,
                "msg": "La compañía tiene empleados y no puede ser eliminada.",
                "result": None,
            }
        # Si no hay empleados, proceder con la eliminación
        company_query = session.query(Companies).filter(Companies.id == id).first()
        if company_query:
            session.delete(company_query)
            session.commit()
            return {
                "ok": True,
                "msg": "Compañía eliminada con éxito.",
                "result": company_query,
            }
        else:
            return {"ok": False, "msg": "Compañía no encontrada.", "result": None}
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()


def get_talonario_by_company_controller(company_id, period_id):
    try:
        company_query = (
            session.query(
                func.sum(Time.salary).label("total_salary"),
                func.sum(Time.others).label("total_others"),
                func.sum(Time.vacation_pay).label("total_vacation_pay"),
                func.sum(Time.holyday_pay).label("total_holyday_pay"),
                func.sum(Time.sick_pay).label("total_sick_pay"),
                func.sum(Time.meal_pay).label("total_meal_pay"),
                func.sum(Time.over_pay).label("total_over_pay"),
                func.sum(Time.regular_pay).label("total_regular_pay"),
                func.sum(Time.donation).label("total_donation"),
                func.sum(Time.tips).label("total_tips"),
                func.sum(Time.aflac).label("total_aflac"),
                func.sum(Time.inability).label("total_inability"),
                func.sum(Time.choferil).label("total_choferil"),
                func.sum(Time.social_tips).label("total_social_tips"),
                func.sum(Time.asume).label("total_asume"),
                func.sum(Time.concessions).label("total_concessions"),
                func.sum(Time.commissions).label("total_commissions"),
                func.sum(Time.bonus).label("total_bonus"),
                func.sum(Time.refund).label("total_refund"),
                func.sum(Time.medicare).label("total_medicare"),
                func.sum(Time.secure_social).label("total_ss"),
                func.sum(Time.tax_pr).label("total_tax_pr")
                ).join(Companies, onclause=Companies.id == company_id)
                .select_from(Period).join(
                    Time, Period.id == Time.period_id 
                    ).filter(Period.id == period_id).group_by(Period.year).all()            
        )
        
        companies_query = (
            session.query(Employers, Companies)
            .join(Companies, onclause=Companies.id == company_id)
            .filter(Employers.company_id == company_id)
            .first()
        )
        
        employer, company = companies_query  # Desempaquetar la tupla
        time_query = (
            session.query(Time)
            .join(Companies, onclause=Companies.id == company_id)
            .filter(Time.period_id == period_id)
            .all()
        )
        
        if time_query:
            taxes_query = session.query(Payments).join(Time).join(Employers).filter(Employers.company_id == company_id, Time.period_id == period_id).all()
        else:
            taxes_query = []

        return {
            "ok": True,
            "msg": "",
            "result": {
                "company": company,
                "employer": employer,
                "time": time_query,
                "taxes": taxes_query,
            },
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()
