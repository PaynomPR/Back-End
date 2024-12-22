from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
import fitz  # PyMuPDF

import calendar
import datetime as date_time
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse, Response
from jinja2 import Template
from sqlalchemy.sql import func
from models.vacation_times import VacationTimes

from sqlalchemy import cast, Integer
from datetime import date

from database.config import session
from models.companies import Companies
from models.employers import Employers
from models.periods import Period
from models.time import Time
from models.payments import Payments
from models.queries.queryFormW2pr import queryFormW2pr
from utils.time_func import minutes_to_time, time_to_minutes

from utils.form_499 import form_withheld_499_pdf_generator
from utils.from_choferil import form_choferil_pdf_generator
from utils.pdfkit.pdfhandled import create_pdf
from weasyprint import HTML
from utils.form_940 import form_940_pdf_generator
from utils.form_491 import form_941_pdf_generator
from utils.form_wages import form_wages_txt_generator
from utils.form_493 import form_943_pdf_generator
from utils.unemployment import form_unemployment_pdf_generator
from utils.form_w2p_txt import form_w2p_txt_generator
from utils.form_w2psse_txt import form_w2psse_txt_generator

from utils.form_w2pr import form_w2pr_pdf_generate
from collections import defaultdict
from models.queries.queryUtils import   getAmountCSFECompany , getBonusCompany

report_router = APIRouter()



def counterfoil_by_range_controller(company_id, employer_id,start,end):
    
    # Obtener la información de la empresa
    company = session.query(Companies).filter(Companies.id == company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Compañoa no encontrada"
        )
    
    start = date_time.datetime.fromisoformat(str(start)).strftime("%Y-%m-%d")
    end = date_time.datetime.fromisoformat(str(end)).strftime("%Y-%m-%d")
    
    print(start)
    print(end)
    # Obtener la información del empleado
    employer = session.query(Employers).filter(Employers.id == employer_id).first()
    if not employer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empleado no encontrado"
        )

    # Función para convertir una cadena de tiempo a minutos
    def time_to_minutes(time_str):
     
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes
    

    

    time_period_query = session.query(Period).select_from(Period).join(Time, Period.id == Time.period_id and Time.employer_id == employer_id).filter(Period.period_end >= start , Period.period_end <= end).first()
    print(time_period_query)
    year = time_period_query.period_end.year
    month = time_period_query.period_end.month

    vacation_time_query = session.query(
        func.sum(VacationTimes.vacation_hours).label("vacation_hours"),
        func.sum(VacationTimes.sicks_hours).label("sicks_hours")
    ).select_from(VacationTimes).filter(     
        VacationTimes.employer_id == employer_id,        
        cast(VacationTimes.month, Integer) < month,
        cast(VacationTimes.year, Integer) <= year
    ).group_by(VacationTimes.year).all()

    

    # employer time
    
    all_time_query = session.query(func.sum(Time.salary).label("total_salary"),
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
                    func.sum(Time.tax_pr).label("total_tax_pr")).select_from(Period).join(Time, Period.id == Time.period_id and Time.employer_id == employer_id
                    ).filter(Time.employer_id == employer_id,Period.period_end >= start , Period.period_end <= end,Time.employer_id == employer_id
                    ).group_by(Time.employer_id).all()


    all_times_query = session.query(Time).select_from(Period).join(Time, Period.id == Time.period_id and Time.employer_id == employer_id).filter(Time.employer_id == employer_id,Period.period_end >= start , Period.period_end <= end).all()

    total_regular_time  = "00:00"
    total_regular_time_seconds = 0

    total_over_time  = "00:00"
    total_over_time_seconds = 0

    total_mealt_time  = "00:00"
    total_mealt_time_seconds = 0

    total_vacation_time  = "00:00"
    total_vacation_time_seconds = 0

    total_sick_time  = "00:00"
    total_sick_time_seconds = 0

    total_holiday_time  = "00:00"
    total_holiday_time_seconds = 0
    for time_entry in all_times_query:
        regular_time = time_entry.regular_time
        over_time = time_entry.over_time
        mealt_time = time_entry.meal_time
        vacation_time = time_entry.vacation_time
        sick_time = time_entry.sick_time
        holiday_time = time_entry.holiday_time



        try:
            # Convertir la cadena a horas y minutos
            regular_hours, regular_minutes = map(int, regular_time.split(':'))

            # Convertir a segundos
            regular_total_seconds = regular_hours * 3600 + regular_minutes * 60

            # Convertir la cadena a horas y minutos
            over_hours, over_minutes = map(int, over_time.split(':'))

            # Convertir a segundos
            over_total_seconds = over_hours * 3600 + over_minutes * 60

            # Convertir la cadena a horas y minutos
            mealt_hours, mealt_minutes = map(int, mealt_time.split(':'))

            # Convertir a segundos
            mealt_total_seconds = mealt_hours * 3600 + mealt_minutes * 60

            # Convertir la cadena a horas y minutos
            vacation_hours, vacation_minutes = map(int, vacation_time.split(':'))

            # Convertir a segundos
            vacation_total_seconds = vacation_hours * 3600 + vacation_minutes * 60

            # Convertir la cadena a horas y minutos
            sick_hours, sick_minutes = map(int, sick_time.split(':'))

            # Convertir a segundos
            sick_total_seconds = sick_hours * 3600 + sick_minutes * 60

            # Convertir la cadena a horas y minutos
            holiday_hours, holiday_minutes = map(int, holiday_time.split(':'))

            # Convertir a segundos
            holiday_total_seconds = holiday_hours * 3600 + holiday_minutes * 60

        except ValueError:
            # Manejar formatos de tiempo inválidos (opcional)
            print(f"Formato de tiempo inválido: {regular_time}")
            continue  # Saltar a la siguiente entrada

        # Sumar los segundos al total
        total_regular_time_seconds += regular_total_seconds
        total_mealt_time_seconds += mealt_total_seconds
        total_over_time_seconds += over_total_seconds
        total_sick_time_seconds += sick_total_seconds
        total_vacation_time_seconds += vacation_total_seconds
        total_holiday_time_seconds += holiday_total_seconds


        # Convertir los segundos totales a horas y minutos
        regular_hours, remaining_seconds = divmod(total_regular_time_seconds, 3600)
        regular_minutes, regular_seconds = divmod(remaining_seconds, 60)
        total_regular_time = f"{regular_hours:02d}:{regular_minutes:02d}"
        # Convertir los segundos totales a horas y minutos
        over_hours, remaining_seconds = divmod(total_over_time_seconds, 3600)
        over_minutes, over_seconds = divmod(remaining_seconds, 60)
        total_over_time = f"{over_hours:02d}:{over_minutes:02d}"
        # Convertir los segundos totales a horas y minutos
        sick_hours, remaining_seconds = divmod(total_sick_time_seconds, 3600)
        sick_minutes, sick_seconds = divmod(remaining_seconds, 60)
        total_sick_time = f"{sick_hours:02d}:{sick_minutes:02d}"
        # Convertir los segundos totales a horas y minutos
        mealt_hours, remaining_seconds = divmod(total_mealt_time_seconds, 3600)
        mealt_minutes, mealt_seconds = divmod(remaining_seconds, 60)
        total_mealt_time = f"{mealt_hours:02d}:{mealt_minutes:02d}"
        # Convertir los segundos totales a horas y minutos
        vacation_hours, remaining_seconds = divmod(total_vacation_time_seconds, 3600)
        vacation_minutes, vacation_seconds = divmod(remaining_seconds, 60)
        total_vacation_time = f"{vacation_hours:02d}:{vacation_minutes:02d}"
        # Convertir los segundos totales a horas y minutos
        holiday_hours, remaining_seconds = divmod(total_holiday_time_seconds, 3600)
        holiday_minutes, holiday_seconds = divmod(remaining_seconds, 60)
        total_holiday_time = f"{holiday_hours:02d}:{holiday_minutes:02d}"





    payment_query = session.query(Payments).select_from(Period).join(Time, Period.id == Time.period_id ).join(Payments, Payments.time_id == Time.id).filter(Period.period_end >= end,Period.period_end <= end,Time.employer_id == employer_id).all()
    payment_texts = ""
    # Crear lista de textos de pagos
    total_payment_amount = 0
    payment_amount = 0
    total_amount_by_tax_id = defaultdict(int)  # Dictionary to store total per tax_id

    # Calculate total amount by tax_id
    for payment in payment_query:
      
        if (payment.is_active or payment.required == 2):
            total_amount_by_tax_id[payment.taxe_id] += payment.amount
        

    for payment in payment_query:
        if (payment.is_active or payment.required == 2):
            total_payment_amount += payment.amount
            
            total_for_current_tax_id = total_amount_by_tax_id.get(payment.taxe_id, 0)

            payment_texts += f" <tr><td>{payment.name}:</td><td>${total_for_current_tax_id}</td></tr>"
        else:            
            total_for_current_tax_id = total_amount_by_tax_id.get(payment.taxe_id, 0)
            payment_texts += f" <tr><td>{payment.name}:</td><td>${total_for_current_tax_id}</td></tr>"
    


    # calculo del overtime_pay
    def convertir_horas_decimales(hh_mm_str):
        hours, minutes = map(int, hh_mm_str.split(':'))
        return hours + minutes / 60.0

    def regular_pay(regular_amount , regular_time, salary, others, bonus):
        time_hours = convertir_horas_decimales(regular_time)
        return regular_amount * time_hours + salary + others +bonus


    def calculate_payment(payment_type, regular_amount):
        payment_hours = convertir_horas_decimales(payment_type)
        payment_pay = payment_hours * regular_amount
        return Decimal(payment_pay).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


    def calculate_year_curr(period_type, regular_pay):
        if period_type == "monthly":
            return regular_pay * 12
        elif period_type == "biweekly":
            return regular_pay * 24
        elif period_type == "weekly":
            return regular_pay * 52  

    vacation_acum = 0
    sicks_acum = 0
    if vacation_time_query is not None and len(vacation_time_query) > 0:
        vacation_acum = vacation_time_query[0].vacation_hours
        sicks_acum = vacation_time_query[0].sicks_hours        
    

    print("----------------vacation_acum"+ str(vacation_acum))
    print("----------------sicks_acum"+ str(sicks_acum))
        
    
    info = {
        # EMPLOYERS INFO
        "first_name": employer.first_name,
        
        "vacation_time": minutes_to_time(( vacation_acum* 60)+time_to_minutes(employer.vacation_time)- time_to_minutes(total_vacation_time)),
        "sick_time": minutes_to_time((sicks_acum * 60)+time_to_minutes(employer.sick_time)- time_to_minutes(total_sick_time)),
        
        "total_ss":round(all_time_query[0].total_ss, 2) ,
        "total_tax_pr":round(all_time_query[0].total_tax_pr, 2) ,
        "total_medicare":round(all_time_query[0].total_medicare, 2) ,
        "total_refund":round(all_time_query[0].total_refund, 2) ,
        "total_bonus":round(all_time_query[0].total_bonus, 2) ,
        "total_commissions" : round(all_time_query[0].total_commissions, 2) ,
        "total_tips" : round(all_time_query[0].total_tips, 2) ,
        "total_choferil" : round(all_time_query[0].total_choferil, 2) ,
        "total_inability" : round(all_time_query[0].total_inability, 2) ,
        "total_others" : round(all_time_query[0].total_others, 2) ,
        "total_asume" : round(all_time_query[0].total_asume, 2) ,
        "total_aflac" : round(all_time_query[0].total_aflac, 2) ,
        "total_donation" : round(all_time_query[0].total_donation, 2) ,
        "total_concessions" : round(all_time_query[0].total_concessions, 2) ,
        "total_social_tips" : round(all_time_query[0].total_social_tips, 2) ,
        "total_regular_pay": round(all_time_query[0].total_regular_pay, 2) ,
        "total_over_pay": round(all_time_query[0].total_over_pay, 2) ,
        "total_meal_pay": round(all_time_query[0].total_meal_pay, 2) ,
        "total_holyday_pay": round(all_time_query[0].total_holyday_pay, 2) ,
        "total_sick_pay": round(all_time_query[0].total_sick_pay, 2) ,
        "total_vacation_pay": round(all_time_query[0].total_vacation_pay, 2) ,
        "total_salary" : round(all_time_query[0].total_salary, 2) ,
        "total_regular_time" : total_regular_time ,
        "total_over_time" : total_over_time ,
        "total_meal_time" : total_mealt_time ,
       
        "total_holiday_pay" : all_time_query[0].total_holyday_pay ,

        "total_holiday_time" : total_holiday_time ,
        "total_sick_time" : total_sick_time ,
        "total_vacation_time" : total_vacation_time ,
       
        "total_col_1_year" : round(all_time_query[0].total_regular_pay+all_time_query[0].total_over_pay+all_time_query[0].total_meal_pay+all_time_query[0].total_holyday_pay+all_time_query[0].total_sick_pay+all_time_query[0].total_vacation_pay+ all_time_query[0].total_tips+ all_time_query[0].total_commissions+ all_time_query[0].total_concessions, 2) ,
        
       
        "total_col_2_year" : round(all_time_query[0].total_asume+all_time_query[0].total_donation+total_payment_amount+all_time_query[0].total_aflac-all_time_query[0].total_refund, 2) ,

       
        "total_col_3_year" : round(all_time_query[0].total_tax_pr+all_time_query[0].total_ss+all_time_query[0].total_choferil+all_time_query[0].total_inability+all_time_query[0].total_medicare+all_time_query[0].total_social_tips, 2) ,
        

     
        "last_name": employer.last_name,
        "employer_address": employer.address,
        "employer_state": employer.address_state,
        "employer_address_number": employer.address_number,
        "employer_phone": employer.phone_number,
        "social_security_number": employer.social_security_number,
        #PERIOD INFO
      
        "start_date": start,
        "end_date": end,
        
        # COMPANY INFO
        "company": company.name,
        "physical_address": company.physical_address,
        "payment_texts" : payment_texts,
     
       
    }


    # Plantilla HTML
    template_html = """
        <!DOCTYPE html>
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Recibo de Pago</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    font-size: 10px; /* Tamaño de fuente más pequeño */
                    margin: 0;
                    background-color: #fff;
                    color: #000;
                }
                    .cheque {
    border: 2px solid black;
    padding: 20px;
    margin-top: 10px;

}
.titulo-cheque {
    font-weight: bold;
    font-size: 24px;
    text-align: center;
}
                .container {
                    width: 100%;

                    border: 1px solid #000;
                    padding: 12px;
                    box-sizing: border-box;
                }
                .header {
                    margin-bottom: 20px;
                }
                .header p {
                    margin:  0;
                }
                .flex-container {
                    display: flex;
                    justify-content: space-between;
                }
                table{
                    width: 100%;}
                .section {
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 20px;
                }
                .column {
                    width: 33%;
                    padding: 10px;
                    box-sizing: border-box;
                }
                .cheque  .column {
                    width:50%; }
                .totals {
                    text-align: right;
                }
                .totals p {
                    font-size: 1.2em;
                    font-weight: bold;
                }
                .grid-container {
                    display: grid;
                    grid-template-columns: auto auto;
                    column-gap: 20px;
                }
                .grid-container p {
                    margin: 5px 0;
                }
                .grid-container p.amount {
                    text-align: right;
                }
                .middle-column, .year-column {
                    width: 10%;
                    padding: 10px;
                    box-sizing: border-box;
                    margin-left: -30px;
                }
                .middle-column h4, .year-column h4 {
                    text-align: center;
                }
                .year-column p {
                    text-align: right;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">


                    <div class="flex-container">
                        <div class="column">
                        <p>NUMERO DE CHEQUE {{ company }}</p>
                    
                            <p>{{ first_name }} {{ last_name }}</p>
                            <p>{{ employer_address }}</p>
                            <p>{{ employer_state  }} {{ employer_address_number }}</p>
                        </div>
                        <div class="column">
                            <p>{{ first_name }} {{ last_name }}</p>
                            <p>NUMERO CHEQUE: {{ company }} {{ actual_date }}</p>
                            <p>MEMO: NÓMINA {{ start_date }} - {{ end_date }}</p>
                        </div>
                    </div>
                </div>
                <div style="width: 100%;display: flex;flex-direction: row;">
                    <div class="column">
                <table >
                    <tr>
                        <th>WAGES</th>
                  
                        <th>AMOUNT</th>
                    </tr>
                    <tr>
                        <td>REG. PAY:</td>
                      
                        <td>${{total_regular_pay}}</td>
                    </tr>
                    <tr>
                        <td>VACATIONS:</td>
                      
                        <td>${{ total_vacation_pay }}</td>
                    </tr>
                        <tr>
                        <td>SICK PAY:</td>
                        
                        <td>${{ total_sick_pay }}</td>
                    </tr>
                        <tr>
                        <td>OVER TIME:</td>
                     
                        <td>${{ total_over_pay }}</td>
                    </tr>
                        <tr>
                        <td>MEAL TIME:</td>
                        
                        <td>${{ total_meal_pay }}</td>
                    </tr>
                    <tr>
                        <td>HOLIDAY TIME:</td>
                        
                        <td>${{ total_holiday_pay }}</td>
                    </tr>
                        <tr>
                        <td>COMMI:</td>
                        
                        <td>${{ total_commissions }}</td>
                    </tr>
                        <tr>
                        <td>TIPS:</td>
                        
                        <td>${{ total_tips }}</td>
                    </tr>
                    <tr>
                        <td>CONCESSIONS:</td>
                      
                        <td>${{ total_concessions }}</td>
                    </tr>
                        <tr>
                        <td>SALARY:</td>
                      
                        <td>${{ total_salary }}</td>
                    </tr>
                        <tr>
                        <td>BONUS:</td>
                      
                        <td>${{ total_bonus }}</td>
                    </tr>
                        <tr>
                        <td>OTHER 1:</td>
                       
                        <td>${{ total_others }}</td>
                    </tr>
                    <tr>
                        <td>Total:</td>
                       
                        <td>${{total_col_1_year}}</td>
                    </tr>
                </table>
                </div>
                <div class="column">
                <table >
                    <tr>
                        <th></th>
                       
                        <th>AMOUNT</th>
                    </tr>
                    <tr>
                        <td>
Gastos Reembolsados:</td>
                      
                        <td>${{ total_refund }}</td>
                    </tr>
                    <tr>
                        <td>ASUME:</td>
                     
                        <td>${{total_asume}}</td>
                    </tr>
                        <tr>
                        <td>DONATIVOS:</td>
                        
                        <td>${{ total_donation }}</td>
                    </tr>
                        <tr>
                        <td>AFLAC:</td>
                      
                        <td>${{ total_aflac }}</td>
                    </tr>

                     {{payment_texts}}


                    
                      
                        <tr>
                        <td>Total:</td>
                       
                        <td>${{ total_col_2_year }}</td>
                    </tr>
                        <tr>
                        <td></td>
                        
                        <td></td>
                    </tr>
                        <tr>
                        <td></td>
                      
                        <td></td>
                    </tr>
                        <tr>
                        <td></td>
                     
                        <td></td>
                    </tr>
                    
                       
                   
                </table>
                </div>
                <div class="column">
                <table >
                    <tr>
                        <th></th>
                     
                        <th>AMOUNT</th>
                    </tr>
                    <tr>
                        <td>INC TAX:</td>
                        
                        <td>${{ total_tax_pr }}</td>
                    </tr>

                    <tr>
                        <td>SEGURO SOCIAL:</td>
                      
                        <td>${{total_ss}}</td>
                    </tr>

                        <tr>
                        <td>SS TIPS:</td>
                        
                        <td>${{ total_social_tips }}</td>
                    </tr>
                        <tr>
                        <td>MEDICARE:</td>
                       
                        <td>${{ total_medicare }}</td>
                    </tr>
                        <tr>
                        <td>DISABILITY:</td>
                       
                        <td>${{ total_inability }}</td>
                    </tr>
                        <tr>
                        <td>CHAUFFEUR W:</td>
                      
                        <td>${{ total_choferil }}</td>
                    </tr>
                    
                        <tr>
                        <td>Total:</td>
                       
                        <td>${{ total_col_3_year }}</td>
                    </tr>
                        <tr>
                        <td></td>
                        
                        <td></td>
                    </tr>
                        <tr>
                        <td></td>
                      
                        <td></td>
                    </tr>
                        <tr>
                        <td></td>
                       
                        <td></td>
                    </tr>
                        <tr>
                        <td>REG. HOURS:</td>
                      
                        <td>{{ total_regular_time }}</td>
                    </tr>
                    <tr>
                        <td>VAC HOURS:</td>
                       
                        <td>{{ total_vacation_time }}</td>
                    </tr>
                    <tr>
                        <td>MEAL HOURS:</td>
                      
                        <td>{{ total_meal_time }}</td>
                    </tr>
                        <tr>
                        <td>SICK HOURS:</td>
                      
                        <td>{{ total_sick_time }}</td>
                    </tr>
                        <tr>
                        <td>OVER. HOURS:</td>
                      
                        <td>{{ total_over_time }}</td>
                    </tr>
                    <tr>
                        <td>HOLIDAY HOURS:</td>
                       
                        <td>{{ total_holiday_time }}</td>
                    </tr>
                </table>
                </div>
</div>
<div class="footer" style="  padding-left: 12px;">
                    <p>VAC ACUM: {{vacation_time}} ENF ACUM: {{sick_time}}</p>
                </div>
            </div>
    """

    template = Template(template_html)
    rendered_html = template.render(info)

    # Generar el PDF usando WeasyPrint
    pdf_file = "voucher_pago.pdf"
    HTML(string=rendered_html).write_pdf(pdf_file)

    return FileResponse(
        pdf_file,
        media_type="application/pdf",
        filename="Talonario_de_Pagos.pdf"
    )

def counterfoil_controller(company_id, employer_id, time_id):
    
    # Obtener la información de la empresa
    company = session.query(Companies).filter(Companies.id == company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Compañoa no encontrada"
        )

    # Obtener la información del empleado
    employer = session.query(Employers).filter(Employers.id == employer_id).first()
    if not employer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empleado no encontrado"
        )

    # Función para convertir una cadena de tiempo a minutos
    def time_to_minutes(time_str):
     
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes
    

    

    time_period_query = session.query(Period,Time).select_from(Period).join(Time, Period.id == Time.period_id and Time.employer_id == employer_id).filter(Time.id == time_id).first()
    year = time_period_query.Period.period_end.year
    month = time_period_query.Period.period_end.month

    vacation_time_query = session.query(
        func.sum(VacationTimes.vacation_hours).label("vacation_hours"),
        func.sum(VacationTimes.sicks_hours).label("sicks_hours")
    ).select_from(VacationTimes).filter(     
        VacationTimes.employer_id == employer_id,        
        cast(VacationTimes.month, Integer) < month,
        cast(VacationTimes.year, Integer) <= year
    ).group_by(VacationTimes.year).all()

    
    date_start = date(year, 1, 1)
    # employer time
    time_query = session.query(Time).filter(Time.id == time_id).first()
    all_time_query = session.query(func.sum(Time.salary).label("total_salary"),
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
                    func.sum(Time.tax_pr).label("total_tax_pr")).select_from(Period).join(Time, Period.id == Time.period_id and Time.employer_id == employer_id
                    ).filter(Period.year == year,Time.employer_id == employer_id,Period.period_end >= date_start,Period.period_end <= time_period_query.Period.period_end,Time.employer_id == employer_id
                    ).group_by(Period.year).all()


    all_times_query = session.query(Time).select_from(Period).join(Time, Period.id == Time.period_id and Time.employer_id == employer_id).filter(Period.year == year,Time.employer_id == employer_id,Period.period_start <= time_period_query.Period.period_start).all()

    total_regular_time  = "00:00"
    total_regular_time_seconds = 0

    

    total_over_time  = "00:00"
    total_over_time_seconds = 0

    total_mealt_time  = "00:00"
    total_mealt_time_seconds = 0

    total_vacation_time  = "00:00"
    total_vacation_time_seconds = 0

    total_sick_time  = "00:00"
    total_sick_time_seconds = 0

    total_holiday_time  = "00:00"
    total_holiday_time_seconds = 0
    for time_entry in all_times_query:
        regular_time = time_entry.regular_time
        hours_worked_salary = time_entry.hours_worked_salary
        over_time = time_entry.over_time
        mealt_time = time_entry.meal_time
        vacation_time = time_entry.vacation_time
        sick_time = time_entry.sick_time
        holiday_time = time_entry.holiday_time



        try:
            # Convertir la cadena a horas y minutos
            regular_hours, regular_minutes = map(int, regular_time.split(':'))

            # Convertir a segundos
            regular_total_seconds = regular_hours + hours_worked_salary * 3600 + regular_minutes * 60

            # Convertir la cadena a horas y minutos
            over_hours, over_minutes = map(int, over_time.split(':'))

            # Convertir a segundos
            over_total_seconds = over_hours * 3600 + over_minutes * 60

            # Convertir la cadena a horas y minutos
            mealt_hours, mealt_minutes = map(int, mealt_time.split(':'))

            # Convertir a segundos
            mealt_total_seconds = mealt_hours * 3600 + mealt_minutes * 60

            # Convertir la cadena a horas y minutos
            vacation_hours, vacation_minutes = map(int, vacation_time.split(':'))

            # Convertir a segundos
            vacation_total_seconds = vacation_hours * 3600 + vacation_minutes * 60

            # Convertir la cadena a horas y minutos
            sick_hours, sick_minutes = map(int, sick_time.split(':'))

            # Convertir a segundos
            sick_total_seconds = sick_hours * 3600 + sick_minutes * 60

            # Convertir la cadena a horas y minutos
            holiday_hours, holiday_minutes = map(int, holiday_time.split(':'))

            # Convertir a segundos
            holiday_total_seconds = holiday_hours * 3600 + holiday_minutes * 60

        except ValueError:
            # Manejar formatos de tiempo inválidos (opcional)
            print(f"Formato de tiempo inválido: {regular_time}")
            continue  # Saltar a la siguiente entrada

        # Sumar los segundos al total
        total_regular_time_seconds += regular_total_seconds
        total_mealt_time_seconds += mealt_total_seconds
        total_over_time_seconds += over_total_seconds
        total_sick_time_seconds += sick_total_seconds
        total_vacation_time_seconds += vacation_total_seconds
        total_holiday_time_seconds += holiday_total_seconds


        # Convertir los segundos totales a horas y minutos
        regular_hours, remaining_seconds = divmod(total_regular_time_seconds, 3600)
        regular_minutes, regular_seconds = divmod(remaining_seconds, 60)
        total_regular_time = f"{regular_hours:02d}:{regular_minutes:02d}"
        # Convertir los segundos totales a horas y minutos
        over_hours, remaining_seconds = divmod(total_over_time_seconds, 3600)
        over_minutes, over_seconds = divmod(remaining_seconds, 60)
        total_over_time = f"{over_hours:02d}:{over_minutes:02d}"
        # Convertir los segundos totales a horas y minutos
        sick_hours, remaining_seconds = divmod(total_sick_time_seconds, 3600)
        sick_minutes, sick_seconds = divmod(remaining_seconds, 60)
        total_sick_time = f"{sick_hours:02d}:{sick_minutes:02d}"
        # Convertir los segundos totales a horas y minutos
        mealt_hours, remaining_seconds = divmod(total_mealt_time_seconds, 3600)
        mealt_minutes, mealt_seconds = divmod(remaining_seconds, 60)
        total_mealt_time = f"{mealt_hours:02d}:{mealt_minutes:02d}"
        # Convertir los segundos totales a horas y minutos
        vacation_hours, remaining_seconds = divmod(total_vacation_time_seconds, 3600)
        vacation_minutes, vacation_seconds = divmod(remaining_seconds, 60)
        total_vacation_time = f"{vacation_hours:02d}:{vacation_minutes:02d}"
        # Convertir los segundos totales a horas y minutos
        holiday_hours, remaining_seconds = divmod(total_holiday_time_seconds, 3600)
        holiday_minutes, holiday_seconds = divmod(remaining_seconds, 60)
        total_holiday_time = f"{holiday_hours:02d}:{holiday_minutes:02d}"





    payment_query = session.query(Payments).select_from(Period).join(Time, Period.id == Time.period_id ).join(Payments, Payments.time_id == Time.id).filter(Period.year == year,Period.period_start <= time_period_query.Period.period_start,Time.employer_id == employer_id).all()
    payment_texts = ""
    # Crear lista de textos de pagos
    total_payment_amount = 0
    payment_amount = 0
    total_amount_by_tax_id = defaultdict(int)  # Dictionary to store total per tax_id

    # Calculate total amount by tax_id
    for payment in payment_query:
      
        if (payment.is_active or payment.required == 2):
            total_amount_by_tax_id[payment.taxe_id] += payment.amount
        

    for payment in payment_query:
        if (payment.is_active or payment.required == 2):
            total_payment_amount += payment.amount
            if payment.time_id == time_id:
                amount = payment.amount;
                if (payment.amount< 0):
                    amount = payment.amount * -1
                total_for_current_tax_id = total_amount_by_tax_id.get(payment.taxe_id, 0)

                payment_texts += f" <tr><td>{payment.name}:</td><td>${amount}</td><td>${total_for_current_tax_id}</td></tr>"
        else:
            if payment.time_id == time_id:
                total_for_current_tax_id = total_amount_by_tax_id.get(payment.taxe_id, 0)
                payment_texts += f" <tr><td>{payment.name}:</td><td>$0</td><td>${total_for_current_tax_id}</td></tr>"


    if not time_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Time not found"
        )





    # Obtener la información del periodo
    period = session.query(Period).filter(Period.id == time_query.period_id).first()
    if not period:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Periodo no encontrado"
        )


    # calculo del overtime_pay
    def convertir_horas_decimales(hh_mm_str):
        hours, minutes = map(int, hh_mm_str.split(':'))
        return hours + minutes / 60.0

    def regular_pay(regular_amount , regular_time, salary, others, bonus):
        time_hours = convertir_horas_decimales(regular_time)
        return regular_amount * time_hours + salary + others +bonus


    def calculate_payment(payment_type, regular_amount):
        payment_hours = convertir_horas_decimales(payment_type)
        payment_pay = payment_hours * regular_amount
        return Decimal(payment_pay).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


    def calculate_year_curr(period_type, regular_pay):
        if period_type == "monthly":
            return regular_pay * 12
        elif period_type == "biweekly":
            return regular_pay * 24
        elif period_type == "weekly":
            return regular_pay * 52

    def calculate_income():
        regu_pay = regular_pay(time_query.regular_amount, time_query.regular_time,time_query.salary,time_query.others,time_query.bonus)
        overtime_pay = calculate_payment(time_query.over_time, time_query.over_amount)
        meal_time_pay= calculate_payment(time_query.meal_time, time_query.meal_amount)
        holiday_time_pay = calculate_payment(time_query.holiday_time, time_query.regular_amount)
        sick_pay = calculate_payment(time_query.sick_time, time_query.regular_amount)
        vacation_pay = calculate_payment(time_query.vacation_time, time_query.regular_amount)
        tips_pay = time_query.tips
        commission_pay = time_query.commissions
        concessions = time_query.concessions
        return float(regu_pay)+ float(overtime_pay) + float(meal_time_pay) + float(holiday_time_pay) + float(sick_pay) + float(vacation_pay) + float(tips_pay) + float(commission_pay) + float(concessions) + float(time_query.refund)

    def calculate_egress():
        secure_social = time_query.secure_social
        ss_tips = time_query.social_tips
        medicare = time_query.medicare
        inability = time_query.inability
        choferil = time_query.choferil
        tax_pr = time_query.tax_pr

        aflac = time_query.aflac

        return float(secure_social) + float(ss_tips) + float(medicare) + float(inability) + float(choferil) + float(tax_pr)  + float(aflac) + float(time_query.asume) + float(time_query.donation)
    # Function to add hours to HH:MM time string (new function)
    def add_hours_to_time(time_str, hours_to_add):
        try:
            hours, minutes = map(int, time_str.split(':'))
            total_minutes = hours * 60 + minutes
            total_minutes += hours_to_add * 60  # Add the hours
            new_hours, new_minutes = divmod(total_minutes, 60)
            return f"{new_hours:02d}:{new_minutes:02d}"
        except ValueError:
            return "Invalid Time Format"  # Or handle the error as needed
    def calculate_payments():
        amount = 0
        for payment in payment_query:
            if (payment.is_active == True or payment.required == 2):
                if (payment.time_id == time_id):
                    if payment.type_taxe == 1 and payment.amount > 0:
                        amount -= payment.amount
                    else:
                        amount += payment.amount
        
        return amount

    def calculate_total():
        income = calculate_income()
        egress = calculate_egress()
        adicional_amount = calculate_payments()

        return round(income - egress + adicional_amount, 2)
    payment_amount = calculate_payments()
    if (payment_amount < 0 ):
        payment_amount = payment_amount * -1

    vacation_acum = 0
    sicks_acum = 0
    if vacation_time_query is not None and len(vacation_time_query) > 0:
        vacation_acum = vacation_time_query[0].vacation_hours
        sicks_acum = vacation_time_query[0].sicks_hours        
    

    print("----------------vacation_acum"+ str(vacation_acum))
    print("----------------sicks_acum"+ str(sicks_acum))
        
    
    info = {
        # EMPLOYERS INFO
        "first_name": employer.first_name,
        "salary": time_query.salary,
        "others": time_query.others,
        "vacation_time": minutes_to_time(( vacation_acum* 60)+time_to_minutes(employer.vacation_time)- time_to_minutes(total_vacation_time)),
        "sick_time": minutes_to_time((sicks_acum * 60)+time_to_minutes(employer.sick_time)- time_to_minutes(total_sick_time)),
        "others": time_query.others,
        "total_ss":round(all_time_query[0].total_ss, 2) ,
        "total_tax_pr":round(all_time_query[0].total_tax_pr, 2) ,
        "total_medicare":round(all_time_query[0].total_medicare, 2) ,
        "total_refund":round(all_time_query[0].total_refund, 2) ,
        "total_bonus":round(all_time_query[0].total_bonus, 2) ,
        "total_commissions" : round(all_time_query[0].total_commissions, 2) ,
        "total_tips" : round(all_time_query[0].total_tips, 2) ,
        "total_choferil" : round(all_time_query[0].total_choferil, 2) ,
        "total_inability" : round(all_time_query[0].total_inability, 2) ,
        "total_others" : round(all_time_query[0].total_others, 2) ,
        "total_asume" : round(all_time_query[0].total_asume, 2) ,
        "total_aflac" : round(all_time_query[0].total_aflac, 2) ,
        "total_donation" : round(all_time_query[0].total_donation, 2) ,
        "total_concessions" : round(all_time_query[0].total_concessions, 2) ,
        "total_social_tips" : round(all_time_query[0].total_social_tips, 2) ,
        "total_regular_pay": round(all_time_query[0].total_regular_pay, 2) ,
        "total_over_pay": round(all_time_query[0].total_over_pay, 2) ,
        "total_meal_pay": round(all_time_query[0].total_meal_pay, 2) ,
        "total_holyday_pay": round(all_time_query[0].total_holyday_pay, 2) ,
        "total_sick_pay": round(all_time_query[0].total_sick_pay, 2) ,
        "total_vacation_pay": round(all_time_query[0].total_vacation_pay, 2) ,
        "total_salary" : round(all_time_query[0].total_salary, 2) ,
        "total_regular_time" : total_regular_time ,
        "total_over_time" : total_over_time ,
        "total_meal_time" : total_mealt_time ,
        "holiday_time_pay" : time_query.holyday_pay,
        "total_holiday_pay" : all_time_query[0].total_holyday_pay ,

        "total_holiday_time" : total_holiday_time ,
        "total_sick_time" : total_sick_time ,
        "total_vacation_time" : total_vacation_time ,
        "total_col_1" : round(time_query.regular_pay+time_query.over_pay+time_query.meal_pay+time_query.holyday_pay+time_query.sick_pay+time_query.vacation_pay+ time_query.tips+ time_query.commissions+ time_query.concessions, 2) ,
        "total_col_1_year" : round(all_time_query[0].total_regular_pay+all_time_query[0].total_over_pay+all_time_query[0].total_meal_pay+all_time_query[0].total_holyday_pay+all_time_query[0].total_sick_pay+all_time_query[0].total_vacation_pay+ all_time_query[0].total_tips+ all_time_query[0].total_commissions+ all_time_query[0].total_concessions, 2) ,
        
        "total_col_2" : round(time_query.asume+time_query.donation+payment_amount+time_query.aflac-time_query.refund, 2) ,
        "total_col_2_year" : round(all_time_query[0].total_asume+all_time_query[0].total_donation+total_payment_amount+all_time_query[0].total_aflac-all_time_query[0].total_refund, 2) ,

        "total_col_3" : round(time_query.tax_pr+time_query.secure_social+time_query.choferil+time_query.inability+time_query.medicare+time_query.social_tips, 2) ,
        "total_col_3_year" : round(all_time_query[0].total_tax_pr+all_time_query[0].total_ss+all_time_query[0].total_choferil+all_time_query[0].total_inability+all_time_query[0].total_medicare+all_time_query[0].total_social_tips, 2) ,
        

        "asume" : time_query.asume,

        "bonus": time_query.bonus,
        "aflac": time_query.aflac,

        "refund": time_query.refund,
        "donation": time_query.donation,
        "last_name": employer.last_name,
        "employer_address": employer.address,
        "employer_state": employer.address_state,
        "employer_address_number": employer.address_number,
        "employer_phone": employer.phone_number,
        "social_security_number": employer.social_security_number,
        #PERIOD INFO
        "actual_date": datetime.now().strftime("%d-%m-%Y"),
        "start_date": period.period_start,
        "end_date": period.period_end,
        "period_type": period.period_type.value,
        # COMPANY INFO
        "company": company.name,
        "physical_address": company.physical_address,
        # TIME INFO
        "regular_hours": add_hours_to_time(time_query.regular_time, time_query.hours_worked_salary),  # Use the new function

        "over_hours": time_query.over_time,
        "meal_hours": time_query.meal_time,
        "holiday_hours": time_query.holiday_time,
        "sick_hours": time_query.sick_time,


        "vacation_hours": time_query.vacation_time,
        # PAY INFO
        "regular_pay": regular_pay(time_query.regular_amount, time_query.regular_time,time_query.salary,time_query.others,time_query.bonus),
        "overtime_pay": calculate_payment(time_query.over_time, time_query.over_amount),
        "meal_time_pay": calculate_payment(time_query.meal_time, time_query.meal_amount),
        "sick_pay": calculate_payment(time_query.sick_time, time_query.regular_amount),
        "vacation_pay": calculate_payment(time_query.vacation_time, time_query.regular_amount),
        "tips_pay": time_query.tips,
        "comissions": time_query.commissions,
        "income": calculate_income(),
        "concessions" : time_query.concessions,
        "payment_texts" : payment_texts,
        # YEAR INFO
        "year_curr":calculate_year_curr(period.period_type.value, regular_pay(time_query.regular_amount, time_query.regular_time,time_query.salary,time_query.others,time_query.bonus)),
        #RATE
        "regular_rate": time_query.regular_amount,
        "mealt_rate": time_query.meal_amount,
        "over_rate": time_query.over_amount,
        "employer_retained" : time_query.employer_retained,
        # DESCUENTOS INFO
        "secure_social": time_query.secure_social,
        "ss_tips": time_query.social_tips,
        "medicare": time_query.medicare,
        "inability": time_query.inability,
        "choferil": time_query.choferil,
        "egress": calculate_egress(),
        "tax_pr": time_query.tax_pr,
        # TOTAL INFO
        "total": calculate_total()
    }


    # Plantilla HTML
    template_html = """
        <!DOCTYPE html>
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Recibo de Pago</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    font-size: 10px; /* Tamaño de fuente más pequeño */
                    margin: 0;
                    background-color: #fff;
                    color: #000;
                }
                    .cheque {
    border: 2px solid black;
    padding: 20px;
    margin-top: 10px;

}
.titulo-cheque {
    font-weight: bold;
    font-size: 24px;
    text-align: center;
}
                .container {
                    width: 100%;

                    border: 1px solid #000;
                    padding: 12px;
                    box-sizing: border-box;
                }
                .header {
                    margin-bottom: 20px;
                }
                .header p {
                    margin:  0;
                }
                .flex-container {
                    display: flex;
                    justify-content: space-between;
                }
                table{
                    width: 100%;}
                .section {
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 20px;
                }
                .column {
                    width: 33%;
                    padding: 10px;
                    box-sizing: border-box;
                }
                .cheque  .column {
                    width:50%; }
                .totals {
                    text-align: right;
                }
                .totals p {
                    font-size: 1.2em;
                    font-weight: bold;
                }
                .grid-container {
                    display: grid;
                    grid-template-columns: auto auto;
                    column-gap: 20px;
                }
                .grid-container p {
                    margin: 5px 0;
                }
                .grid-container p.amount {
                    text-align: right;
                }
                .middle-column, .year-column {
                    width: 10%;
                    padding: 10px;
                    box-sizing: border-box;
                    margin-left: -30px;
                }
                .middle-column h4, .year-column h4 {
                    text-align: center;
                }
                .year-column p {
                    text-align: right;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">


                    <div class="flex-container">
                        <div class="column">
                        <p>NUMERO DE CHEQUE {{ company }}</p>
                    <p>Fecha: {{ actual_date }}</p>
                            <p>{{ first_name }} {{ last_name }}</p>
                            <p>{{ employer_address }}</p>
                            <p>{{ employer_state  }} {{ employer_address_number }}</p>
                        </div>
                        <div class="column">
                            <p>{{ first_name }} {{ last_name }}</p>
                            <p>NUMERO CHEQUE: {{ company }} {{ actual_date }}</p>
                            <p>MEMO: NÓMINA {{ start_date }} - {{ end_date }}</p>
                        </div>
                    </div>
                </div>
                <div style="width: 100%;display: flex;flex-direction: row;">
                    <div class="column">
                <table >
                    <tr>
                        <th>WAGES</th>
                        <th>CURR</th>
                        <th>YEAR</th>
                    </tr>
                    <tr>
                        <td>REG. PAY:</td>
                        <td>${{ regular_pay }}</td>
                        <td>${{total_regular_pay}}</td>
                    </tr>
                    <tr>
                        <td>VACATIONS:</td>
                        <td>${{ vacation_pay }}</td>
                        <td>${{ total_vacation_pay }}</td>
                    </tr>
                        <tr>
                        <td>SICK PAY:</td>
                        <td>${{ sick_pay }}</td>
                        <td>${{ total_sick_pay }}</td>
                    </tr>
                        <tr>
                        <td>OVER TIME:</td>
                        <td>${{ overtime_pay }}</td>
                        <td>${{ total_over_pay }}</td>
                    </tr>
                        <tr>
                        <td>MEAL TIME:</td>
                        <td>${{ meal_time_pay }}</td>
                        <td>${{ total_meal_pay }}</td>
                    </tr>
                    <tr>
                        <td>HOLIDAY TIME:</td>
                        <td>${{ holiday_time_pay }}</td>
                        <td>${{ total_holiday_pay }}</td>
                    </tr>
                        <tr>
                        <td>COMMI:</td>
                        <td>${{ comissions }}</td>
                        <td>${{ total_commissions }}</td>
                    </tr>
                        <tr>
                        <td>TIPS:</td>
                        <td>${{ tips_pay }}</td>
                        <td>${{ total_tips }}</td>
                    </tr>
                    <tr>
                        <td>CONCESSIONS:</td>
                        <td>${{ concessions }}</td>
                        <td>${{ total_concessions }}</td>
                    </tr>
                        <tr>
                        <td>SALARY:</td>
                        <td>${{ salary }}</td>
                        <td>${{ total_salary }}</td>
                    </tr>
                        <tr>
                        <td>BONUS:</td>
                        <td>${{ bonus }}</td>
                        <td>${{ total_bonus }}</td>
                    </tr>
                        <tr>
                        <td>OTHER 1:</td>
                        <td>${{ others }}</td>
                        <td>${{ total_others }}</td>
                    </tr>
                    <tr>
                        <td>Total:</td>
                        <td>${{ total_col_1 }}</td>
                        <td>${{total_col_1_year}}</td>
                    </tr>
                </table>
                </div>
                <div class="column">
                <table >
                    <tr>
                        <th></th>
                        <th>CURR</th>
                        <th>YEAR</th>
                    </tr>
                    <tr>
                        <td>
Gastos Reembolsados:</td>
                        <td>${{ refund }}</td>
                        <td>${{ total_refund }}</td>
                    </tr>
                    <tr>
                        <td>ASUME:</td>
                        <td>${{ asume }}</td>
                        <td>${{total_asume}}</td>
                    </tr>
                        <tr>
                        <td>DONATIVOS:</td>
                        <td>${{ donation }}</td>
                        <td>${{ total_donation }}</td>
                    </tr>
                        <tr>
                        <td>AFLAC:</td>
                        <td>${{ aflac }}</td>
                        <td>${{ total_aflac }}</td>
                    </tr>

                    


                    
                        {{payment_texts}}
                        <tr>
                        <td>Total:</td>
                        <td>${{ total_col_2 }}</td>
                        <td>${{ total_col_2_year }}</td>
                    </tr>
                        <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>
                        <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>
                        <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>
                    
                        <tr>
                        <td>REG RATE:</td>
                        <td>${{ regular_rate }}</td>
                        <td></td>
                    </tr>
                    <tr>
                        <td>MEALT RATE:</td>
                        <td>${{ mealt_rate }}</td>
                        <td></td>
                    </tr>
                    <tr>
                        <td>OVER RATE:</td>
                        <td>${{ over_rate }}</td>
                        <td></td>
                    </tr>
                    <tr>
                        <td>% RETENCIÓN:</td>
                        <td>${{ employer_retained }} %</td>
                        <td></td>
                    </tr>

                </table>
                </div>
                <div class="column">
                <table >
                    <tr>
                        <th></th>
                        <th>CURR</th>
                        <th>YEAR</th>
                    </tr>
                    <tr>
                        <td>INC TAX:</td>
                        <td>${{ tax_pr }}</td>
                        <td>${{ total_tax_pr }}</td>
                    </tr>

                    <tr>
                        <td>SEGURO SOCIAL:</td>
                        <td>${{ secure_social }}</td>
                        <td>${{total_ss}}</td>
                    </tr>

                        <tr>
                        <td>SS TIPS:</td>
                        <td>${{ ss_tips }}</td>
                        <td>${{ total_social_tips }}</td>
                    </tr>
                        <tr>
                        <td>MEDICARE:</td>
                        <td>${{ medicare }}</td>
                        <td>${{ total_medicare }}</td>
                    </tr>
                        <tr>
                        <td>DISABILITY:</td>
                        <td>${{ inability }}</td>
                        <td>${{ total_inability }}</td>
                    </tr>
                        <tr>
                        <td>CHAUFFEUR W:</td>
                        <td>${{ choferil }}</td>
                        <td>${{ total_choferil }}</td>
                    </tr>
                    
                        <tr>
                        <td>Total:</td>
                        <td>${{ total_col_3 }}</td>
                        <td>${{ total_col_3_year }}</td>
                    </tr>
                        <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>
                        <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>
                        <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>
                        <tr>
                        <td>REG. HOURS:</td>
                        <td>{{ regular_hours }}</td>
                        <td>{{ total_regular_time }}</td>
                    </tr>
                    <tr>
                        <td>VAC HOURS:</td>
                        <td>{{ vacation_hours }}</td>
                        <td>{{ total_vacation_time }}</td>
                    </tr>
                    <tr>
                        <td>MEAL HOURS:</td>
                        <td>{{ meal_hours }}</td>
                        <td>{{ total_meal_time }}</td>
                    </tr>
                        <tr>
                        <td>SICK HOURS:</td>
                        <td>{{ sick_hours }}</td>
                        <td>{{ total_sick_time }}</td>
                    </tr>
                        <tr>
                        <td>OVER. HOURS:</td>
                        <td>{{ over_hours }}</td>
                        <td>{{ total_over_time }}</td>
                    </tr>
                    <tr>
                        <td>HOLIDAY HOURS:</td>
                        <td>{{ holiday_hours }}</td>
                        <td>{{ total_holiday_time }}</td>
                    </tr>
                        
                    
                    
                    
                </table>
                </div>
</div>
<div class="footer" style="  padding-left: 12px;">
                    <p>VAC ACUM: {{vacation_time}} ENF ACUM: {{sick_time}}</p>
                </div>
                <div class="totals">
                    <p>Total: ${{ total }}</p>
                </div>

                

            
            </div>
                    <div class="cheque">
<div>


                    <div style="font-size: 14px;" class="flex-container">
                        <div class="column" style="width: 70%;">



                                                    <p > {{ company }}</p>
                                                    <p style="margin-top: 0px"> {{ physical_address }}</p>

                            <p style="margin-top: 24px;width: 100%;            ">PAY TO ORDER OF: <span style="border-bottom: 1px solid black;padding: 2px 16px 2px 16px;">      {{ first_name }} {{ last_name }}             </p>
                        
                    
                            
                            <p style="margin-top: 24px;">FOR: ________________</p>
                            
                        </div>
                        <div class="column" style="text-align: right;width: 30%;">
                            <p>Fecha: {{ actual_date }}</p>
                            <p   style="margin-top: 48px;">Total: ${{ total }}</p>
                            <p style="margin-top: 32px;">FOR: ________________</p>
                        </div>
                    </div>
                </div>


                    

    """

    template = Template(template_html)
    rendered_html = template.render(info)

    # Generar el PDF usando WeasyPrint
    pdf_file = "voucher_pago.pdf"
    HTML(string=rendered_html).write_pdf(pdf_file)

    return FileResponse(
        pdf_file,
        media_type="application/pdf",
        filename="Talonario_de_Pagos.pdf"
    )
    
def counterfoil_by_period_controller(company_id, employer_id, period_id):
    
    # Obtener la información de la empresa
    company = session.query(Companies).filter(Companies.id == company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Compañoa no encontrada"
        )

    # Obtener la información del empleado
    employer = session.query(Employers).filter(Employers.id == employer_id).first()
    if not employer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empleado no encontrado"
        )

    # Función para convertir una cadena de tiempo a minutos
    def time_to_minutes(time_str):
     
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes
    

    

    time_period_query = session.query(Period,Time).select_from(Period).join(Time, Period.id == Time.period_id and Time.employer_id == employer_id).filter(Time.period_id == period_id).first()
    year = time_period_query.Period.period_end.year
    month = time_period_query.Period.period_end.month

    vacation_time_query = session.query(
        func.sum(VacationTimes.vacation_hours).label("vacation_hours"),
        func.sum(VacationTimes.sicks_hours).label("sicks_hours")
    ).select_from(VacationTimes).filter(     
        VacationTimes.employer_id == employer_id,        
        cast(VacationTimes.month, Integer) < month,
        cast(VacationTimes.year, Integer) <= year
    ).group_by(VacationTimes.year).all()

    
    date_start = date(year, 1, 1)
    # employer time
    time_query = session.query(Time).filter(Time.period_id == period_id).first()
    all_time_query = session.query(func.sum(Time.salary).label("total_salary"),
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
                    func.sum(Time.tax_pr).label("total_tax_pr")).select_from(Period).join(Time, Period.id == Time.period_id and Time.employer_id == employer_id
                    ).filter(Period.year == year,Time.employer_id == employer_id,Period.period_end >= date_start,Period.period_end <= time_period_query.Period.period_end,Time.employer_id == employer_id
                    ).group_by(Period.year).all()


    all_times_query = session.query(Time).select_from(Period).join(Time, Period.id == Time.period_id and Time.employer_id == employer_id).filter(Period.year == year,Time.employer_id == employer_id,Period.period_start <= time_period_query.Period.period_start).all()

    total_regular_time  = "00:00"
    total_regular_time_seconds = 0

    total_over_time  = "00:00"
    total_over_time_seconds = 0

    total_mealt_time  = "00:00"
    total_mealt_time_seconds = 0

    total_vacation_time  = "00:00"
    total_vacation_time_seconds = 0

    total_sick_time  = "00:00"
    total_sick_time_seconds = 0

    total_holiday_time  = "00:00"
    total_holiday_time_seconds = 0
    for time_entry in all_times_query:
        regular_time = time_entry.regular_time
        over_time = time_entry.over_time
        mealt_time = time_entry.meal_time
        vacation_time = time_entry.vacation_time
        sick_time = time_entry.sick_time
        holiday_time = time_entry.holiday_time



        try:
            # Convertir la cadena a horas y minutos
            regular_hours, regular_minutes = map(int, regular_time.split(':'))

            # Convertir a segundos
            regular_total_seconds = regular_hours * 3600 + regular_minutes * 60

            # Convertir la cadena a horas y minutos
            over_hours, over_minutes = map(int, over_time.split(':'))

            # Convertir a segundos
            over_total_seconds = over_hours * 3600 + over_minutes * 60

            # Convertir la cadena a horas y minutos
            mealt_hours, mealt_minutes = map(int, mealt_time.split(':'))

            # Convertir a segundos
            mealt_total_seconds = mealt_hours * 3600 + mealt_minutes * 60

            # Convertir la cadena a horas y minutos
            vacation_hours, vacation_minutes = map(int, vacation_time.split(':'))

            # Convertir a segundos
            vacation_total_seconds = vacation_hours * 3600 + vacation_minutes * 60

            # Convertir la cadena a horas y minutos
            sick_hours, sick_minutes = map(int, sick_time.split(':'))

            # Convertir a segundos
            sick_total_seconds = sick_hours * 3600 + sick_minutes * 60

            # Convertir la cadena a horas y minutos
            holiday_hours, holiday_minutes = map(int, holiday_time.split(':'))

            # Convertir a segundos
            holiday_total_seconds = holiday_hours * 3600 + holiday_minutes * 60

        except ValueError:
            # Manejar formatos de tiempo inválidos (opcional)
            print(f"Formato de tiempo inválido: {regular_time}")
            continue  # Saltar a la siguiente entrada

        # Sumar los segundos al total
        total_regular_time_seconds += regular_total_seconds
        total_mealt_time_seconds += mealt_total_seconds
        total_over_time_seconds += over_total_seconds
        total_sick_time_seconds += sick_total_seconds
        total_vacation_time_seconds += vacation_total_seconds
        total_holiday_time_seconds += holiday_total_seconds


        # Convertir los segundos totales a horas y minutos
        regular_hours, remaining_seconds = divmod(total_regular_time_seconds, 3600)
        regular_minutes, regular_seconds = divmod(remaining_seconds, 60)
        total_regular_time = f"{regular_hours:02d}:{regular_minutes:02d}"
        # Convertir los segundos totales a horas y minutos
        over_hours, remaining_seconds = divmod(total_over_time_seconds, 3600)
        over_minutes, over_seconds = divmod(remaining_seconds, 60)
        total_over_time = f"{over_hours:02d}:{over_minutes:02d}"
        # Convertir los segundos totales a horas y minutos
        sick_hours, remaining_seconds = divmod(total_sick_time_seconds, 3600)
        sick_minutes, sick_seconds = divmod(remaining_seconds, 60)
        total_sick_time = f"{sick_hours:02d}:{sick_minutes:02d}"
        # Convertir los segundos totales a horas y minutos
        mealt_hours, remaining_seconds = divmod(total_mealt_time_seconds, 3600)
        mealt_minutes, mealt_seconds = divmod(remaining_seconds, 60)
        total_mealt_time = f"{mealt_hours:02d}:{mealt_minutes:02d}"
        # Convertir los segundos totales a horas y minutos
        vacation_hours, remaining_seconds = divmod(total_vacation_time_seconds, 3600)
        vacation_minutes, vacation_seconds = divmod(remaining_seconds, 60)
        total_vacation_time = f"{vacation_hours:02d}:{vacation_minutes:02d}"
        # Convertir los segundos totales a horas y minutos
        holiday_hours, remaining_seconds = divmod(total_holiday_time_seconds, 3600)
        holiday_minutes, holiday_seconds = divmod(remaining_seconds, 60)
        total_holiday_time = f"{holiday_hours:02d}:{holiday_minutes:02d}"





    payment_query = session.query(Payments,Time).select_from(Period).join(Time, Period.id == Time.period_id ).join(Payments, Payments.time_id == Time.id).filter(Period.year == year,Period.period_start <= time_period_query.Period.period_start,Time.employer_id == employer_id).all()
    payment_texts = ""
    # Crear lista de textos de pagos
    total_payment_amount = 0
    payment_amount = 0
    total_amount_by_tax_id = defaultdict(int)  # Dictionary to store total per tax_id

    # Calculate total amount by tax_id
    for payment in payment_query:
      
        if (payment.Payments.is_active or payment.Payments.required == 2):
            total_amount_by_tax_id[payment.Payments.taxe_id] += payment.Payments.amount
        

    for payment in payment_query:
        if (payment.Payments.is_active or payment.Payments.required == 2):
            total_payment_amount += payment.Payments.amount
            if payment.Time.period_id == period_id:
                amount = payment.Payments.amount;
                if (payment.Payments.amount< 0):
                    amount = payment.Payments.amount * -1
                total_for_current_tax_id = total_amount_by_tax_id.get(payment.Payments.taxe_id, 0)

                payment_texts += f" <tr><td>{payment.Payments.name}:</td><td>${amount}</td><td>${total_for_current_tax_id}</td></tr>"
        else:
            if  payment.Time.period_id == period_id:
                total_for_current_tax_id = total_amount_by_tax_id.get(payment.Payments.taxe_id, 0)
                payment_texts += f" <tr><td>{payment.Payments.name}:</td><td>$0</td><td>${total_for_current_tax_id}</td></tr>"


    if not time_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Time not found"
        )





    # Obtener la información del periodo
    period = session.query(Period).filter(Period.id == time_query.period_id).first()
    if not period:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Periodo no encontrado"
        )


    # calculo del overtime_pay
    def convertir_horas_decimales(hh_mm_str):
        hours, minutes = map(int, hh_mm_str.split(':'))
        return hours + minutes / 60.0

    def regular_pay(regular_amount , regular_time, salary, others, bonus):
        time_hours = convertir_horas_decimales(regular_time)
        return regular_amount * time_hours + salary + others +bonus


    def calculate_payment(payment_type, regular_amount):
        payment_hours = convertir_horas_decimales(payment_type)
        payment_pay = payment_hours * regular_amount
        return Decimal(payment_pay).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


    def calculate_year_curr(period_type, regular_pay):
        if period_type == "monthly":
            return regular_pay * 12
        elif period_type == "biweekly":
            return regular_pay * 24
        elif period_type == "weekly":
            return regular_pay * 52

    def calculate_income():
        regu_pay = regular_pay(time_query.regular_amount, time_query.regular_time,time_query.salary,time_query.others,time_query.bonus)
        overtime_pay = calculate_payment(time_query.over_time, time_query.over_amount)
        meal_time_pay= calculate_payment(time_query.meal_time, time_query.meal_amount)
        holiday_time_pay = calculate_payment(time_query.holiday_time, time_query.regular_amount)
        sick_pay = calculate_payment(time_query.sick_time, time_query.regular_amount)
        vacation_pay = calculate_payment(time_query.vacation_time, time_query.regular_amount)
        tips_pay = time_query.tips
        commission_pay = time_query.commissions
        concessions = time_query.concessions
        return float(regu_pay)+ float(overtime_pay) + float(meal_time_pay) + float(holiday_time_pay) + float(sick_pay) + float(vacation_pay) + float(tips_pay) + float(commission_pay) + float(concessions) + float(time_query.refund)

    def calculate_egress():
        secure_social = time_query.secure_social
        ss_tips = time_query.social_tips
        medicare = time_query.medicare
        inability = time_query.inability
        choferil = time_query.choferil
        tax_pr = time_query.tax_pr

        aflac = time_query.aflac

        return float(secure_social) + float(ss_tips) + float(medicare) + float(inability) + float(choferil) + float(tax_pr)  + float(aflac) + float(time_query.asume) + float(time_query.donation)

    def calculate_payments():
        amount = 0
        for payment in payment_query:
            if (payment.Payments.is_active == True or payment.Payments.required == 2):
                if payment.Time.period_id == period_id:
                    if payment.Payments.type_taxe == 1 and payment.Payments.amount > 0:
                        amount -= payment.Payments.amount
                    else:
                        amount += payment.Payments.amount
        
        return amount

    def calculate_total():
        income = calculate_income()
        egress = calculate_egress()
        adicional_amount = calculate_payments()

        return round(income - egress + adicional_amount, 2)
    payment_amount = calculate_payments()
    if (payment_amount < 0 ):
        payment_amount = payment_amount * -1

    vacation_acum = 0
    sicks_acum = 0
    if vacation_time_query is not None and len(vacation_time_query) > 0:
        vacation_acum = vacation_time_query[0].vacation_hours
        sicks_acum = vacation_time_query[0].sicks_hours        
    

    print("----------------vacation_acum"+ str(vacation_acum))
    print("----------------sicks_acum"+ str(sicks_acum))
        
    
    info = {
        # EMPLOYERS INFO
        "first_name": employer.first_name,
        "salary": time_query.salary,
        "others": time_query.others,
        "vacation_time": minutes_to_time(( vacation_acum* 60)+time_to_minutes(employer.vacation_time)- time_to_minutes(total_vacation_time)),
        "sick_time": minutes_to_time((sicks_acum * 60)+time_to_minutes(employer.sick_time)- time_to_minutes(total_sick_time)),
        "others": time_query.others,
        "total_ss":round(all_time_query[0].total_ss, 2) ,
        "total_tax_pr":round(all_time_query[0].total_tax_pr, 2) ,
        "total_medicare":round(all_time_query[0].total_medicare, 2) ,
        "total_refund":round(all_time_query[0].total_refund, 2) ,
        "total_bonus":round(all_time_query[0].total_bonus, 2) ,
        "total_commissions" : round(all_time_query[0].total_commissions, 2) ,
        "total_tips" : round(all_time_query[0].total_tips, 2) ,
        "total_choferil" : round(all_time_query[0].total_choferil, 2) ,
        "total_inability" : round(all_time_query[0].total_inability, 2) ,
        "total_others" : round(all_time_query[0].total_others, 2) ,
        "total_asume" : round(all_time_query[0].total_asume, 2) ,
        "total_aflac" : round(all_time_query[0].total_aflac, 2) ,
        "total_donation" : round(all_time_query[0].total_donation, 2) ,
        "total_concessions" : round(all_time_query[0].total_concessions, 2) ,
        "total_social_tips" : round(all_time_query[0].total_social_tips, 2) ,
        "total_regular_pay": round(all_time_query[0].total_regular_pay, 2) ,
        "total_over_pay": round(all_time_query[0].total_over_pay, 2) ,
        "total_meal_pay": round(all_time_query[0].total_meal_pay, 2) ,
        "total_holyday_pay": round(all_time_query[0].total_holyday_pay, 2) ,
        "total_sick_pay": round(all_time_query[0].total_sick_pay, 2) ,
        "total_vacation_pay": round(all_time_query[0].total_vacation_pay, 2) ,
        "total_salary" : round(all_time_query[0].total_salary, 2) ,
        "total_regular_time" : total_regular_time ,
        "total_over_time" : total_over_time ,
        "total_meal_time" : total_mealt_time ,
        "holiday_time_pay" : time_query.holyday_pay,
        "total_holiday_pay" : all_time_query[0].total_holyday_pay ,

        "total_holiday_time" : total_holiday_time ,
        "total_sick_time" : total_sick_time ,
        "total_vacation_time" : total_vacation_time ,
        "total_col_1" : round(time_query.regular_pay+time_query.over_pay+time_query.meal_pay+time_query.holyday_pay+time_query.sick_pay+time_query.vacation_pay+ time_query.tips+ time_query.commissions+ time_query.concessions, 2) ,
        "total_col_1_year" : round(all_time_query[0].total_regular_pay+all_time_query[0].total_over_pay+all_time_query[0].total_meal_pay+all_time_query[0].total_holyday_pay+all_time_query[0].total_sick_pay+all_time_query[0].total_vacation_pay+ all_time_query[0].total_tips+ all_time_query[0].total_commissions+ all_time_query[0].total_concessions, 2) ,
        
        "total_col_2" : round(time_query.asume+time_query.donation+payment_amount+time_query.aflac-time_query.refund, 2) ,
        "total_col_2_year" : round(all_time_query[0].total_asume+all_time_query[0].total_donation+total_payment_amount+all_time_query[0].total_aflac-all_time_query[0].total_refund, 2) ,

        "total_col_3" : round(time_query.tax_pr+time_query.secure_social+time_query.choferil+time_query.inability+time_query.medicare+time_query.social_tips, 2) ,
        "total_col_3_year" : round(all_time_query[0].total_tax_pr+all_time_query[0].total_ss+all_time_query[0].total_choferil+all_time_query[0].total_inability+all_time_query[0].total_medicare+all_time_query[0].total_social_tips, 2) ,
        

        "asume" : time_query.asume,

        "bonus": time_query.bonus,
        "aflac": time_query.aflac,

        "refund": time_query.refund,
        "donation": time_query.donation,
        "last_name": employer.last_name,
        "employer_address": employer.address,
        "employer_state": employer.address_state,
        "employer_address_number": employer.address_number,
        "employer_phone": employer.phone_number,
        "social_security_number": employer.social_security_number,
        #PERIOD INFO
        "actual_date": datetime.now().strftime("%d-%m-%Y"),
        "start_date": period.period_start,
        "end_date": period.period_end,
        "period_type": period.period_type.value,
        # COMPANY INFO
        "company": company.name,
        "physical_address": company.physical_address,
        # TIME INFO
        "regular_hours": time_query.regular_time,
        "over_hours": time_query.over_time,
        "meal_hours": time_query.meal_time,
        "holiday_hours": time_query.holiday_time,
        "sick_hours": time_query.sick_time,


        "vacation_hours": time_query.vacation_time,
        # PAY INFO
        "regular_pay": regular_pay(time_query.regular_amount, time_query.regular_time,time_query.salary,time_query.others,time_query.bonus),
        "overtime_pay": calculate_payment(time_query.over_time, time_query.over_amount),
        "meal_time_pay": calculate_payment(time_query.meal_time, time_query.meal_amount),
        "sick_pay": calculate_payment(time_query.sick_time, time_query.regular_amount),
        "vacation_pay": calculate_payment(time_query.vacation_time, time_query.regular_amount),
        "tips_pay": time_query.tips,
        "comissions": time_query.commissions,
        "income": calculate_income(),
        "concessions" : time_query.concessions,
        "payment_texts" : payment_texts,
        # YEAR INFO
        "year_curr":calculate_year_curr(period.period_type.value, regular_pay(time_query.regular_amount, time_query.regular_time,time_query.salary,time_query.others,time_query.bonus)),
        #RATE
        "regular_rate": time_query.regular_amount,
        "mealt_rate": time_query.meal_amount,
        "over_rate": time_query.over_amount,
        "employer_retained" : time_query.employer_retained,
        # DESCUENTOS INFO
        "secure_social": time_query.secure_social,
        "ss_tips": time_query.social_tips,
        "medicare": time_query.medicare,
        "inability": time_query.inability,
        "choferil": time_query.choferil,
        "egress": calculate_egress(),
        "tax_pr": time_query.tax_pr,
        # TOTAL INFO
        "total": calculate_total()
    }


    # Plantilla HTML
    template_html = """
        <!DOCTYPE html>
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Recibo de Pago</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    font-size: 10px; /* Tamaño de fuente más pequeño */
                    margin: 0;
                    background-color: #fff;
                    color: #000;
                }
                    .cheque {
    border: 2px solid black;
    padding: 20px;
    margin-top: 10px;

}
.titulo-cheque {
    font-weight: bold;
    font-size: 24px;
    text-align: center;
}
                .container {
                    width: 100%;

                    border: 1px solid #000;
                    padding: 12px;
                    box-sizing: border-box;
                }
                .header {
                    margin-bottom: 20px;
                }
                .header p {
                    margin:  0;
                }
                .flex-container {
                    display: flex;
                    justify-content: space-between;
                }
                table{
                    width: 100%;}
                .section {
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 20px;
                }
                .column {
                    width: 33%;
                    padding: 10px;
                    box-sizing: border-box;
                }
                .cheque  .column {
                    width:50%; }
                .totals {
                    text-align: right;
                }
                .totals p {
                    font-size: 1.2em;
                    font-weight: bold;
                }
                .grid-container {
                    display: grid;
                    grid-template-columns: auto auto;
                    column-gap: 20px;
                }
                .grid-container p {
                    margin: 5px 0;
                }
                .grid-container p.amount {
                    text-align: right;
                }
                .middle-column, .year-column {
                    width: 10%;
                    padding: 10px;
                    box-sizing: border-box;
                    margin-left: -30px;
                }
                .middle-column h4, .year-column h4 {
                    text-align: center;
                }
                .year-column p {
                    text-align: right;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">


                    <div class="flex-container">
                        <div class="column">
                        <p>NUMERO DE CHEQUE {{ company }}</p>
                    <p>Fecha: {{ actual_date }}</p>
                            <p>{{ first_name }} {{ last_name }}</p>
                            <p>{{ employer_address }}</p>
                            <p>{{ employer_state  }} {{ employer_address_number }}</p>
                        </div>
                        <div class="column">
                            <p>{{ first_name }} {{ last_name }}</p>
                            <p>NUMERO CHEQUE: {{ company }} {{ actual_date }}</p>
                            <p>MEMO: NÓMINA {{ start_date }} - {{ end_date }}</p>
                        </div>
                    </div>
                </div>
                <div style="width: 100%;display: flex;flex-direction: row;">
                    <div class="column">
                <table >
                    <tr>
                        <th>WAGES</th>
                        <th>CURR</th>
                        <th>YEAR</th>
                    </tr>
                    <tr>
                        <td>REG. PAY:</td>
                        <td>${{ regular_pay }}</td>
                        <td>${{total_regular_pay}}</td>
                    </tr>
                    <tr>
                        <td>VACATIONS:</td>
                        <td>${{ vacation_pay }}</td>
                        <td>${{ total_vacation_pay }}</td>
                    </tr>
                        <tr>
                        <td>SICK PAY:</td>
                        <td>${{ sick_pay }}</td>
                        <td>${{ total_sick_pay }}</td>
                    </tr>
                        <tr>
                        <td>OVER TIME:</td>
                        <td>${{ overtime_pay }}</td>
                        <td>${{ total_over_pay }}</td>
                    </tr>
                        <tr>
                        <td>MEAL TIME:</td>
                        <td>${{ meal_time_pay }}</td>
                        <td>${{ total_meal_pay }}</td>
                    </tr>
                    <tr>
                        <td>HOLIDAY TIME:</td>
                        <td>${{ holiday_time_pay }}</td>
                        <td>${{ total_holiday_pay }}</td>
                    </tr>
                        <tr>
                        <td>COMMI:</td>
                        <td>${{ comissions }}</td>
                        <td>${{ total_commissions }}</td>
                    </tr>
                        <tr>
                        <td>TIPS:</td>
                        <td>${{ tips_pay }}</td>
                        <td>${{ total_tips }}</td>
                    </tr>
                    <tr>
                        <td>CONCESSIONS:</td>
                        <td>${{ concessions }}</td>
                        <td>${{ total_concessions }}</td>
                    </tr>
                        <tr>
                        <td>SALARY:</td>
                        <td>${{ salary }}</td>
                        <td>${{ total_salary }}</td>
                    </tr>
                        <tr>
                        <td>BONUS:</td>
                        <td>${{ bonus }}</td>
                        <td>${{ total_bonus }}</td>
                    </tr>
                        <tr>
                        <td>OTHER 1:</td>
                        <td>${{ others }}</td>
                        <td>${{ total_others }}</td>
                    </tr>
                    <tr>
                        <td>Total:</td>
                        <td>${{ total_col_1 }}</td>
                        <td>${{total_col_1_year}}</td>
                    </tr>
                </table>
                </div>
                <div class="column">
                <table >
                    <tr>
                        <th></th>
                        <th>CURR</th>
                        <th>YEAR</th>
                    </tr>
                    <tr>
                        <td>
Gastos Reembolsados:</td>
                        <td>${{ refund }}</td>
                        <td>${{ total_refund }}</td>
                    </tr>
                    <tr>
                        <td>ASUME:</td>
                        <td>${{ asume }}</td>
                        <td>${{total_asume}}</td>
                    </tr>
                        <tr>
                        <td>DONATIVOS:</td>
                        <td>${{ donation }}</td>
                        <td>${{ total_donation }}</td>
                    </tr>
                        <tr>
                        <td>AFLAC:</td>
                        <td>${{ aflac }}</td>
                        <td>${{ total_aflac }}</td>
                    </tr>

                    


                    
                        {{payment_texts}}
                        <tr>
                        <td>Total:</td>
                        <td>${{ total_col_2 }}</td>
                        <td>${{ total_col_2_year }}</td>
                    </tr>
                        <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>
                        <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>
                        <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>
                    
                        <tr>
                        <td>REG RATE:</td>
                        <td>${{ regular_rate }}</td>
                        <td></td>
                    </tr>
                    <tr>
                        <td>MEALT RATE:</td>
                        <td>${{ mealt_rate }}</td>
                        <td></td>
                    </tr>
                    <tr>
                        <td>OVER RATE:</td>
                        <td>${{ over_rate }}</td>
                        <td></td>
                    </tr>
                    <tr>
                        <td>% RETENCIÓN:</td>
                        <td>${{ employer_retained }} %</td>
                        <td></td>
                    </tr>

                </table>
                </div>
                <div class="column">
                <table >
                    <tr>
                        <th></th>
                        <th>CURR</th>
                        <th>YEAR</th>
                    </tr>
                    <tr>
                        <td>INC TAX:</td>
                        <td>${{ tax_pr }}</td>
                        <td>${{ total_tax_pr }}</td>
                    </tr>

                    <tr>
                        <td>SEGURO SOCIAL:</td>
                        <td>${{ secure_social }}</td>
                        <td>${{total_ss}}</td>
                    </tr>

                        <tr>
                        <td>SS TIPS:</td>
                        <td>${{ ss_tips }}</td>
                        <td>${{ total_social_tips }}</td>
                    </tr>
                        <tr>
                        <td>MEDICARE:</td>
                        <td>${{ medicare }}</td>
                        <td>${{ total_medicare }}</td>
                    </tr>
                        <tr>
                        <td>DISABILITY:</td>
                        <td>${{ inability }}</td>
                        <td>${{ total_inability }}</td>
                    </tr>
                        <tr>
                        <td>CHAUFFEUR W:</td>
                        <td>${{ choferil }}</td>
                        <td>${{ total_choferil }}</td>
                    </tr>
                    
                        <tr>
                        <td>Total:</td>
                        <td>${{ total_col_3 }}</td>
                        <td>${{ total_col_3_year }}</td>
                    </tr>
                        <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>
                        <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>
                        <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>
                        <tr>
                        <td>REG. HOURS:</td>
                        <td>{{ regular_hours }}</td>
                        <td>{{ total_regular_time }}</td>
                    </tr>
                    <tr>
                        <td>VAC HOURS:</td>
                        <td>{{ vacation_hours }}</td>
                        <td>{{ total_vacation_time }}</td>
                    </tr>
                    <tr>
                        <td>MEAL HOURS:</td>
                        <td>{{ meal_hours }}</td>
                        <td>{{ total_meal_time }}</td>
                    </tr>
                        <tr>
                        <td>SICK HOURS:</td>
                        <td>{{ sick_hours }}</td>
                        <td>{{ total_sick_time }}</td>
                    </tr>
                        <tr>
                        <td>OVER. HOURS:</td>
                        <td>{{ over_hours }}</td>
                        <td>{{ total_over_time }}</td>
                    </tr>
                    <tr>
                        <td>HOLIDAY HOURS:</td>
                        <td>{{ holiday_hours }}</td>
                        <td>{{ total_holiday_time }}</td>
                    </tr>
                        
                    
                    
                    
                </table>
                </div>
</div>
<div class="footer" style="  padding-left: 12px;">
                    <p>VAC ACUM: {{vacation_time}} ENF ACUM: {{sick_time}}</p>
                </div>
                <div class="totals">
                    <p>Total: ${{ total }}</p>
                </div>

                

            
            </div>
                    <div class="cheque">
<div>


                    <div style="font-size: 14px;" class="flex-container">
                        <div class="column" style="width: 70%;">



                                                    <p > {{ company }}</p>
                                                    <p style="margin-top: 0px"> {{ physical_address }}</p>

                            <p style="margin-top: 24px;width: 100%;            ">PAY TO ORDER OF: <span style="border-bottom: 1px solid black;padding: 2px 16px 2px 16px;">      {{ first_name }} {{ last_name }}             </p>
                        
                    
                            
                            <p style="margin-top: 24px;">FOR: ________________</p>
                            
                        </div>
                        <div class="column" style="text-align: right;width: 30%;">
                            <p>Fecha: {{ actual_date }}</p>
                            <p   style="margin-top: 48px;">Total: ${{ total }}</p>
                            <p style="margin-top: 32px;">FOR: ________________</p>
                        </div>
                    </div>
                </div>


                    

    """

    template = Template(template_html)
    rendered_html = template.render(info)

    # Generar el PDF usando WeasyPrint
    pdf_file = "voucher_pago.pdf"
    HTML(string=rendered_html).write_pdf(pdf_file)

    return FileResponse(
        pdf_file,
        media_type="application/pdf",
        filename="Talonario_de_Pagos.pdf"
    )

def form_w2pr_pdf_controller(company_id, employer_id, year):
    
    try:
        employers = []
        pdf_files = []
        if employer_id == 0 :
            employers = session.query(Employers.id).filter(Employers.company_id == company_id).all()
        else:
            employers = session.query(Employers.id).filter(Employers.id == employer_id).all()

        for (index, employer) in enumerate(employers, start=1):
            info = queryFormW2pr(employer.id, year)
            if info is None:
                return Response(status_code=status.HTTP_404_NOT_FOUND, content="No data found")

            template = Template(form_w2pr_pdf_generate())
            rendered_html = template.render(info)

            pdf_file = f"./output_files/form_w2pr{index}.pdf"
            HTML(string=rendered_html).write_pdf(pdf_file)
            pdf_files.append(pdf_file)


        doc3 = fitz.open()
        for file in pdf_files:
            doc3.insert_file(file)

        pdf_file = "./output_files/form_w2pr_combined.pdf"
        doc3.save(pdf_file)

        return FileResponse(
            pdf_file,
            media_type="application/pdf",
            filename="Formulario_W2PR.pdf"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()


def form_940_pdf_controller(company_id, year):
    
    pdf = form_940_pdf_generator(company_id, year)
    if pdf is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content="No data found")

    if pdf:
        return FileResponse(
            pdf,
            media_type="application/pdf",
            filename="form_940.pdf"
        )


def form_wages_txt_controller(company_id, year,period):
    
    txt = form_wages_txt_generator(company_id, year,period)

    if txt:
        return FileResponse(
            txt,
            media_type="application/txt",
            filename="form_940.txt"       )

    
def get_w2p_txt_controller(company_id, year,reimbursed,code):
    
    txt = form_w2p_txt_generator(company_id, year,reimbursed,code)

    if txt:
        return FileResponse(
            txt,
            media_type="application/txt",
            filename="form_w2p.txt"       )

def get_w2psse_txt_controller(company_id, year,reimbursed,code):
    
    txt = form_w2psse_txt_generator(company_id, year,reimbursed,code)

    if txt:
        return FileResponse(
            txt,
            media_type="application/txt",
            filename="form_w2p.txt"       )

def form_941_pdf_controller(company_id, year, period):
    
    pdf = form_941_pdf_generator(company_id, year, period)
    if pdf is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content="No data found")

    if pdf:
        return FileResponse(
            pdf,
            media_type="application/pdf",
            filename="form_940.pdf"
        )

    







def form_bonus_pdf_controller(company_id, year, period):

    start = date(year-1, 10, 1)
    end = date(year, 9, calendar.monthrange(year, 9)[1])
    all_times_query = session.query(Time).select_from(Period).join(Time, Period.id == Time.period_id ).join(Employers, Employers.id == Time.employer_id ).filter(Period.period_end >= start,Period.period_end <= end, Employers.company_id == company_id).all()

    

    total_regular_time  = "00:00"
    total_regular_time_seconds = 0

    total_over_time  = "00:00"
    total_over_time_seconds = 0

    total_mealt_time  = "00:00"
    total_mealt_time_seconds = 0

    total_vacation_time  = "00:00"
    total_vacation_time_seconds = 0

    total_sick_time  = "00:00"
    total_sick_time_seconds = 0

    total_holiday_time  = "00:00"
    total_holiday_time_seconds = 0
    for time_entry in all_times_query:
        regular_time = time_entry.regular_time
        over_time = time_entry.over_time
        mealt_time = time_entry.meal_time
        vacation_time = time_entry.vacation_time
        sick_time = time_entry.sick_time
        holiday_time = time_entry.holiday_time



        
        # Convertir la cadena a horas y minutos
        regular_hours, regular_minutes = map(int, regular_time.split(':'))

        # Convertir a segundos
        regular_total_seconds = regular_hours * 3600 + regular_minutes * 60

        # Convertir la cadena a horas y minutos
        over_hours, over_minutes = map(int, over_time.split(':'))

        # Convertir a segundos
        over_total_seconds = over_hours * 3600 + over_minutes * 60

        # Convertir la cadena a horas y minutos
        mealt_hours, mealt_minutes = map(int, mealt_time.split(':'))

        # Convertir a segundos
        mealt_total_seconds = mealt_hours * 3600 + mealt_minutes * 60

        # Convertir la cadena a horas y minutos
        vacation_hours, vacation_minutes = map(int, vacation_time.split(':'))

        # Convertir a segundos
        vacation_total_seconds = vacation_hours * 3600 + vacation_minutes * 60

        # Convertir la cadena a horas y minutos
        sick_hours, sick_minutes = map(int, sick_time.split(':'))

        # Convertir a segundos
        sick_total_seconds = sick_hours * 3600 + sick_minutes * 60

        # Convertir la cadena a horas y minutos
        holiday_hours, holiday_minutes = map(int, holiday_time.split(':'))

        # Convertir a segundos
        holiday_total_seconds = holiday_hours * 3600 + holiday_minutes * 60

        

        # Sumar los segundos al total
        total_regular_time_seconds += regular_total_seconds
        total_mealt_time_seconds += mealt_total_seconds
        total_over_time_seconds += over_total_seconds
        total_sick_time_seconds += sick_total_seconds
        total_vacation_time_seconds += vacation_total_seconds
        total_holiday_time_seconds += holiday_total_seconds


        # Convertir los segundos totales a horas y minutos
        regular_hours, remaining_seconds = divmod(total_regular_time_seconds, 3600)
        regular_minutes, regular_seconds = divmod(remaining_seconds, 60)
        total_regular_time = f"{regular_hours:02d}:{regular_minutes:02d}"
        # Convertir los segundos totales a horas y minutos
        over_hours, remaining_seconds = divmod(total_over_time_seconds, 3600)
        over_minutes, over_seconds = divmod(remaining_seconds, 60)
        total_over_time = f"{over_hours:02d}:{over_minutes:02d}"
        # Convertir los segundos totales a horas y minutos
        sick_hours, remaining_seconds = divmod(total_sick_time_seconds, 3600)
        sick_minutes, sick_seconds = divmod(remaining_seconds, 60)
        total_sick_time = f"{sick_hours:02d}:{sick_minutes:02d}"
        # Convertir los segundos totales a horas y minutos
        mealt_hours, remaining_seconds = divmod(total_mealt_time_seconds, 3600)
        mealt_minutes, mealt_seconds = divmod(remaining_seconds, 60)
        total_mealt_time = f"{mealt_hours:02d}:{mealt_minutes:02d}"
        # Convertir los segundos totales a horas y minutos
        vacation_hours, remaining_seconds = divmod(total_vacation_time_seconds, 3600)
        vacation_minutes, vacation_seconds = divmod(remaining_seconds, 60)
        total_vacation_time = f"{vacation_hours:02d}:{vacation_minutes:02d}"
        # Convertir los segundos totales a horas y minutos
        holiday_hours, remaining_seconds = divmod(total_holiday_time_seconds, 3600)
        holiday_minutes, holiday_seconds = divmod(remaining_seconds, 60)
        total_holiday_time = f"{holiday_hours:02d}:{holiday_minutes:02d}"

        total_hours = regular_hours +over_hours +sick_hours +mealt_hours+holiday_hours
    return total_hours


def form_943_pdf_controller(company_id, year):
    
    pdf = form_943_pdf_generator(company_id, year)
    if pdf is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content="No data found")

    if pdf:
        return FileResponse(
            pdf,
            media_type="application/pdf",
            filename="form_940.pdf"
        )

    


def form_unemployment_pdf_controller(company_id, year, period):
    
    pdf = form_unemployment_pdf_generator(company_id, year, period)
    if pdf is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content="No data found")

    if pdf:
        return FileResponse(
            pdf,
            media_type="application/pdf",
            filename="form_unemployment.pdf"
        )
        

    



def form_choferil_pdf_controller(company_id, year, period):
    try:
        pdf = form_choferil_pdf_generator(company_id, year, period)
        if pdf:
            return FileResponse(
                pdf,
                media_type="application/pdf",
                filename="form_choferil.pdf"
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()

def form_withheld_499_pdf_controller(company_id, year, period):
    try:
        pdf = form_withheld_499_pdf_generator(company_id, year, period)
        if pdf is None:
            return Response(status_code=status.HTTP_404_NOT_FOUND, content="No data found")

        # return pdf
        if pdf:
            return FileResponse(
                pdf,
                media_type="application/pdf",
                filename="form_withheld_499.pdf"
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()


def get_report_bonus_pdf_controller(company_id, year, bonus):
    print("----------bonus-------------")

    print(bonus)
    company = session.query(Companies).filter(Companies.id == company_id).first()
    employees = session.query(Employers).filter(Employers.company_id == company_id).all()
    
    # Calculate quarterly amounts
    quarter_amounts = []
    quarter_starts = [10, 1, 4,7]
    
    for i, start_month in enumerate(quarter_starts):
        
        if (start_month >= 8):
            date_start = date( year - 1, start_month, 1)
        else:
            date_start = date( year, start_month, 1)
        if (start_month >= 8):
            date_end = date( year  -1 , start_month + 2, calendar.monthrange(year, start_month + 2)[1])
        else:
            date_end = date( year , start_month + 2, calendar.monthrange(year, start_month + 2)[1])
        
        quarter_amount = getBonusCompany(company_id, date_start, date_end,bonus)

        if quarter_amount:   
            print("------------------------------------");
            print(quarter_amount);
            for element in quarter_amount:
               
                element_dict = element
                element_dict['period'] = i + 1
                quarter_amounts.append(element_dict)
            
    
    employee_data = []
    total = 0
    total_seconds = 0
    total_hours = ""
    totals_wages = {           
        "totals_1": 0,
        "totals_2": 0,
        "totals_3": 0,
        "totals_4": 0,        
    }
    total_bonus = 0

    
    
    percent = 0
    max_amount = 0
    if bonus.max_employers < len(employees):
        percent = bonus.percent_to_max / 100
        max_amount = bonus.amount_max
    else:
        percent = bonus.percent_to_min / 100
        max_amount = bonus.amount_min
    
    for employee in employees:
        employee_dict = {
            "nombre": employee.first_name,
            "apellido": employee.last_name,
            "number_ss": employee.social_security_number,
            "worked_hour": "",
            "bonus": 0,
            "categoria": "",  # Assuming these fields exist
            "trimestre_1": 0,
            "trimestre_2": 0,
            "trimestre_3": 0,
            "trimestre_4": 0,
            "Total": 0,
        }
        total_worked_seconds = 0  # Initialize a variable for total worked seconds

        # Find matching quarter_amount for this employee
        for quarter_amount in quarter_amounts:
            
            if quarter_amount['employer_id'] == employee.id:
                employee_dict[f"trimestre_{quarter_amount['period']}"] += quarter_amount['wages']
                employee_dict["Total"] += quarter_amount['wages']
                total += quarter_amount['wages']
                totals_wages[f"totals_{quarter_amount['period']}"] += quarter_amount['wages']
                # Update total_worked_seconds
                total_worked_seconds += quarter_amount['total_time']
                
        employee_dict["bonus"] = round(employee_dict["Total"] * percent,2)    
        if employee_dict["bonus"] >=  max_amount:
            employee_dict["bonus"] =  max_amount
        
        # Convert total_worked_seconds to hours and minutes
        hours, remainder = divmod(total_worked_seconds, 3600)
        minutes = int(remainder / 60)
        total_seconds += total_worked_seconds

        if hours < 1350:
            employee_dict["bonus"] = 0


        total_bonus  += employee_dict["bonus"]

        # Update worked_hour with the total sum
        employee_dict["worked_hour"] = f"{hours}:{minutes:02d}"
        employee_data.append(employee_dict)

    # Convert total_worked_seconds to hours and minutes
    total_hours, total_remainder = divmod(total_seconds, 3600)
    total_minutes = int(total_remainder / 60)
    

    total_hours = f"{total_hours}:{total_minutes:02d}"    

    info = {
        "employer_name": company.name,
        "commercial_register": company.commercial_register,
        "data": employee_data,
        "telefono": company.contact_number,
        "total" : total,
        "totals_wages" : totals_wages,
        "total_hours": total_hours,
        "total_bonus": round(total_bonus,2),
    }
    #plantilla html
    template_html = """

        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reporte Planilla CFSE</title>
            <style>
                @page {
                    size: A4 landscape; /* Configura la página en orientación horizontal */
                    margin: 20mm;
                }

                body {
                    font-family: Arial, sans-serif;
                    margin: 20px;
                }

                .header {
                    text-align: center;
                    margin-bottom: 40px;
                }

                .header h1, .header h2 {
                    margin: 0;
                }

                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }

                table, th, td {
                    border: 1px solid black;
                }

                th, td {
                    padding: 8px;
                    text-align: left;
                }

                th {
                    background-color: #f2f2f2;
                    font-size: 10px;
                }

                .total-row {
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <div class="header">
                <h4>{{ employer_name }}</h4>
                <h4>Número de Registro: {{ commercial_register }}</h4>
                <h4>Teléfono: {{ telefono }}</h4>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>NOMBRE</th>
                        <th>APELLIDO</th>
                        <th>NUMERO SS</th>
                        <th>HORAS TRABAJADAS</th>
                        <th>4Q PASADO</th>
                        <th>1Q </th>
                        <th>2Q</th>
                        <th>3Q</th>
                        <th>TOTAL SALARIOS</th>
                        <th>BONO</th>
                    </tr>
                </thead>
                <tbody>
                    {% for employee in data %}
<tr>
    <td>{{ employee.nombre }}</td>
    <td>{{ employee.apellido }}</td>
    <td>{{ employee.number_ss }}</td>
    <td>{{ employee.worked_hour }}</td>
    <td>{{ employee.trimestre_1  }}</td>
    <td>{{ employee.trimestre_2  }}</td>
    <td>{{ employee.trimestre_3  }}</td>
    <td>{{ employee.trimestre_4  }}</td>
    <td>{{ employee.Total }}</td>
    <td>{{ employee.bonus }}</td>
</tr>
{% endfor %}
<tr>
    <td>TOTALES</td>
    <td>---------</td>
    <td>---------</td>
    <td>{{ total_hours }}</td>
    <td>{{ totals_wages.totals_1 }}</td>
    <td>{{ totals_wages.totals_2 }}</td>
    <td>{{ totals_wages.totals_3 }}</td>
    <td>{{ totals_wages.totals_4 }}</td>
    <td>{{ total }}</td>
    <td>{{ total_bonus }}</td>
</tr>
                    
                </tbody>
            </table>
        </body>
        </html>


    """

    template = Template(template_html)
    rendered_html = template.render(info)

    # Generar el PDF usando WeasyPrint
    pdf_file = "pdf_cfse.pdf"
    HTML(string=rendered_html).write_pdf(pdf_file)

    return FileResponse(
        pdf_file,
        media_type="application/pdf",
        filename="pdf_cfse.pdf"
    )

def get_report_cfse_pdf_controller(company_id, year, period):

    company = session.query(Companies).filter(Companies.id == company_id).first()
    employees = session.query(Employers).filter(Employers.company_id == company_id).all()

    # Calculate quarterly amounts
    quarter_amounts = []
    quarter_starts = [7, 10, 1,4]
    
    for i, start_month in enumerate(quarter_starts):
        
        if (start_month >= 7):
            date_start = date( year - 1, start_month, 1)
        else:
            date_start = date( year, start_month, 1)
        if (start_month  >= 7):
            date_end = date( year -1 , start_month + 2, calendar.monthrange(year-1, start_month + 2)[1])
        else:
            date_end = date( year , start_month + 2, calendar.monthrange(year, start_month + 2)[1])
        
        quarter_amount = getAmountCSFECompany(company_id, date_start, date_end)

        if quarter_amount:   
            for element in quarter_amount:
                element_dict = element._asdict()  # Convert SQLAlchemy result to dictionary
                element_dict['period'] = i + 1
                quarter_amounts.append(element_dict)
            
    
    employee_data = []
    

    for employee in employees:
        employee_dict = {
            "nombre": employee.first_name,
            "apellido": employee.last_name,
            "categoria": "",  # Assuming these fields exist
            "trimestre_1": 0,
            "trimestre_2": 0,
            "trimestre_3": 0,
            "trimestre_4": 0,
            "Total": 0,
        }
        
        # Find matching quarter_amount for this employee
        for quarter_amount in quarter_amounts:
            
            if quarter_amount['employer_id'] == employee.id:
                employee_dict[f"trimestre_{quarter_amount['period']}"] += quarter_amount['wages']
                employee_dict["Total"] += quarter_amount['wages']
                

        employee_data.append(employee_dict)

        

    info = {
        "employer_name": company.name,
        "commercial_register": company.commercial_register,
        "data": employee_data,
        "telefono": company.contact_number,
    }
    #plantilla html
    template_html = """

        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reporte Planilla CFSE</title>
            <style>
                @page {
                    size: A4 landscape; /* Configura la página en orientación horizontal */
                    margin: 20mm;
                }

                body {
                    font-family: Arial, sans-serif;
                    margin: 20px;
                }

                .header {
                    text-align: center;
                    margin-bottom: 40px;
                }

                .header h1, .header h2 {
                    margin: 0;
                }

                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }

                table, th, td {
                    border: 1px solid black;
                }

                th, td {
                    padding: 8px;
                    text-align: left;
                }

                th {
                    background-color: #f2f2f2;
                    font-size: 10px;
                }

                .total-row {
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <div class="header">
                <h4>{{ employer_name }}</h4>
                <h4>Número de Registro: {{ commercial_register }}</h4>
                <h4>Teléfono: {{ telefono }}</h4>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>Nombre</th>
                        <th>Apellido</th>
                        <th>Categoría</th>
                        <th>Tercer Trimestre</th>
                        <th>Cuarto Trimestre</th>
                        <th>Primer Trimestre</th>
                        <th>Segundo Trimestre</th>
                        <th>Total</th>
                    </tr>
                </thead>
                <tbody>
                    {% for employee in data %}
<tr>
    <td>{{ employee.nombre }}</td>
    <td>{{ employee.apellido }}</td>
    <td>{{ employee.categoria }}</td>
    <td>{{ employee.trimestre_1  }}</td>
    <td>{{ employee.trimestre_2  }}</td>
    <td>{{ employee.trimestre_3  }}</td>
    <td>{{ employee.trimestre_4  }}</td>
    <td>{{ employee.Total }}</td>
</tr>
{% endfor %}
                    
                </tbody>
            </table>
        </body>
        </html>


    """

    template = Template(template_html)
    rendered_html = template.render(info)

    # Generar el PDF usando WeasyPrint
    pdf_file = "pdf_cfse.pdf"
    HTML(string=rendered_html).write_pdf(pdf_file)

    return FileResponse(
        pdf_file,
        media_type="application/pdf",
        filename="pdf_cfse.pdf"
    )

    
        
        
        

def all_counterfoil_controller(company_id, period_id ):
    
    # calculo del overtime_pay
    def convertir_horas_decimales(hh_mm_str):
        hours, minutes = map(int, hh_mm_str.split(':'))
        return hours + minutes / 60.0

    def regular_pay(regular_amount , regular_time, salary, others, bonus):
        time_hours = convertir_horas_decimales(regular_time)
        return regular_amount * time_hours + salary + others +bonus


    def calculate_payment(payment_type, regular_amount):
        payment_hours = convertir_horas_decimales(payment_type)
        payment_pay = payment_hours * regular_amount
        return Decimal(payment_pay).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


    def calculate_year_curr(period_type, regular_pay):
        if period_type == "monthly":
            return regular_pay * 12
        elif period_type == "biweekly":
            return regular_pay * 24
        elif period_type == "weekly":
            return regular_pay * 52

    def calculate_income():
        regu_pay = regular_pay(time_query.regular_amount, time_query.regular_time,time_query.salary,time_query.others,time_query.bonus)
        overtime_pay = calculate_payment(time_query.over_time, time_query.over_amount)
        meal_time_pay= calculate_payment(time_query.meal_time, time_query.meal_amount)
        holiday_time_pay = calculate_payment(time_query.holiday_time, time_query.regular_amount)
        sick_pay = calculate_payment(time_query.sick_time, time_query.regular_amount)
        vacation_pay = calculate_payment(time_query.vacation_time, time_query.regular_amount)
        tips_pay = time_query.tips
        commission_pay = time_query.commissions
        concessions = time_query.concessions
        return float(regu_pay)+ float(overtime_pay) + float(meal_time_pay) + float(holiday_time_pay) + float(sick_pay) + float(vacation_pay) + float(tips_pay) + float(commission_pay) + float(concessions) + float(time_query.refund)

    def calculate_egress():
        secure_social = time_query.secure_social
        ss_tips = time_query.social_tips
        medicare = time_query.medicare
        inability = time_query.inability
        choferil = time_query.choferil
        tax_pr = time_query.tax_pr

        aflac = time_query.aflac

        return float(secure_social) + float(ss_tips) + float(medicare) + float(inability) + float(choferil) + float(tax_pr)  + float(aflac) + float(time_query.asume) + float(time_query.donation)

    def calculate_payments():
        amount = 0
        for payment in payment_query:
            if payment.Time.period_id == period_id:
                if payment.Payments.type_taxe == 1 and payment.Payments.amount > 0:
                    amount -= payment.Payments.amount
                else:
                    amount += payment.Payments.amount

        return amount

    def calculate_total():
        income = calculate_income()
        egress = calculate_egress()
        adicional_amount = calculate_payments()

        return round(income - egress + adicional_amount, 2)

    # Función para convertir una cadena de tiempo a minutos
    def time_to_minutes(time_str):
        
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes
    
    # Obtener la información de la empresa
    company = session.query(Companies).filter(Companies.id == company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Compañoa no encontrada"
        )

    # Obtener la información del empleado
    employer = session.query(Employers).filter(Employers.company_id == company_id).first()
    if not employer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empleado no encontrado"
        )


    # Obtener la información del periodo
    period = session.query(Period).filter(Period.id == period_id).first()
    if not period:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Periodo no encontrado"
        )        

    time_period_query = session.query(Period).select_from(Period).filter(Period.id == period_id).first()
    year = time_period_query.period_end.year
    month = time_period_query.period_end.month
   
    all_time_query_sums = session.query(Time.employer_id.label("employer_id"),
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
                    func.sum(Time.tax_pr).label("total_tax_pr")).select_from(Period).join(Time, Period.id == Time.period_id 
                    ).join(Employers, Employers.id == Time.employer_id).filter(Period.year == year,Period.period_end <= time_period_query.period_end, Employers.company_id == company_id
                    ).group_by(Time.employer_id).all()

    
    pdf_files = []
    index = 0 
    for all_time_query in all_time_query_sums:
        index += 1
        employer_id = all_time_query.employer_id
       
        
        
        all_times_query = session.query(Time).select_from(Period).join(Time, Period.id == Time.period_id and Time.employer_id == employer_id).filter(Period.year == year,Time.employer_id == employer_id,Period.period_end <= period.period_end).all()

        employer = session.query(Employers).filter_by(id = employer_id ).first()

        total_regular_time  = "00:00"
        total_regular_time_seconds = 0

        total_over_time  = "00:00"
        total_over_time_seconds = 0

        total_mealt_time  = "00:00"
        total_mealt_time_seconds = 0

        total_vacation_time  = "00:00"
        total_vacation_time_seconds = 0

        total_sick_time  = "00:00"
        total_sick_time_seconds = 0

        total_holiday_time  = "00:00"
        total_holiday_time_seconds = 0
        for time_entry in all_times_query:
            regular_time = time_entry.regular_time
            over_time = time_entry.over_time
            mealt_time = time_entry.meal_time
            vacation_time = time_entry.vacation_time
            sick_time = time_entry.sick_time
            holiday_time = time_entry.holiday_time



            
            # Convertir la cadena a horas y minutos
            regular_hours, regular_minutes = map(int, regular_time.split(':'))

            # Convertir a segundos
            regular_total_seconds = regular_hours * 3600 + regular_minutes * 60

            # Convertir la cadena a horas y minutos
            over_hours, over_minutes = map(int, over_time.split(':'))

            # Convertir a segundos
            over_total_seconds = over_hours * 3600 + over_minutes * 60

            # Convertir la cadena a horas y minutos
            mealt_hours, mealt_minutes = map(int, mealt_time.split(':'))

            # Convertir a segundos
            mealt_total_seconds = mealt_hours * 3600 + mealt_minutes * 60

            # Convertir la cadena a horas y minutos
            vacation_hours, vacation_minutes = map(int, vacation_time.split(':'))

            # Convertir a segundos
            vacation_total_seconds = vacation_hours * 3600 + vacation_minutes * 60

            # Convertir la cadena a horas y minutos
            sick_hours, sick_minutes = map(int, sick_time.split(':'))

            # Convertir a segundos
            sick_total_seconds = sick_hours * 3600 + sick_minutes * 60

            # Convertir la cadena a horas y minutos
            holiday_hours, holiday_minutes = map(int, holiday_time.split(':'))

            # Convertir a segundos
            holiday_total_seconds = holiday_hours * 3600 + holiday_minutes * 60

            

            # Sumar los segundos al total
            total_regular_time_seconds += regular_total_seconds
            total_mealt_time_seconds += mealt_total_seconds
            total_over_time_seconds += over_total_seconds
            total_sick_time_seconds += sick_total_seconds
            total_vacation_time_seconds += vacation_total_seconds
            total_holiday_time_seconds += holiday_total_seconds


            # Convertir los segundos totales a horas y minutos
            regular_hours, remaining_seconds = divmod(total_regular_time_seconds, 3600)
            regular_minutes, regular_seconds = divmod(remaining_seconds, 60)
            total_regular_time = f"{regular_hours:02d}:{regular_minutes:02d}"
            # Convertir los segundos totales a horas y minutos
            over_hours, remaining_seconds = divmod(total_over_time_seconds, 3600)
            over_minutes, over_seconds = divmod(remaining_seconds, 60)
            total_over_time = f"{over_hours:02d}:{over_minutes:02d}"
            # Convertir los segundos totales a horas y minutos
            sick_hours, remaining_seconds = divmod(total_sick_time_seconds, 3600)
            sick_minutes, sick_seconds = divmod(remaining_seconds, 60)
            total_sick_time = f"{sick_hours:02d}:{sick_minutes:02d}"
            # Convertir los segundos totales a horas y minutos
            mealt_hours, remaining_seconds = divmod(total_mealt_time_seconds, 3600)
            mealt_minutes, mealt_seconds = divmod(remaining_seconds, 60)
            total_mealt_time = f"{mealt_hours:02d}:{mealt_minutes:02d}"
            # Convertir los segundos totales a horas y minutos
            vacation_hours, remaining_seconds = divmod(total_vacation_time_seconds, 3600)
            vacation_minutes, vacation_seconds = divmod(remaining_seconds, 60)
            total_vacation_time = f"{vacation_hours:02d}:{vacation_minutes:02d}"
            # Convertir los segundos totales a horas y minutos
            holiday_hours, remaining_seconds = divmod(total_holiday_time_seconds, 3600)
            holiday_minutes, holiday_seconds = divmod(remaining_seconds, 60)
            total_holiday_time = f"{holiday_hours:02d}:{holiday_minutes:02d}"


        payment_query = session.query(Payments,Time).select_from(Period).join(Time, Period.id == Time.period_id ).join(Payments, Payments.time_id == Time.id).filter(Payments.is_active == True,Payments.is_active == True,Period.year == year,Period.period_start <= period.period_start,Time.employer_id == employer_id).all()
        payment_texts = ""
        # Crear lista de textos de pagos
        total_payment_amount = 0
        payment_amount = 0
        total_amount_by_tax_id = defaultdict(int)  # Dictionary to store total per tax_id

        # Calculate total amount by tax_id
        for payment in payment_query:
            total_amount_by_tax_id[payment.Payments.taxe_id] += payment.Payments.amount

        for payment in payment_query:
            total_payment_amount += payment.Payments.amount
            if payment.Time.period_id == period_id:
                amount = payment.Payments.amount;
                if (payment.Payments.amount < 0):
                    amount = payment.Payments.amount * -1
                total_for_current_tax_id = total_amount_by_tax_id.get(payment.Payments.taxe_id, 0)

                payment_texts += f" <tr><td>{payment.Payments.name}:</td><td>${amount}</td><td>${total_for_current_tax_id}</td></tr>"


        time_query = session.query(Time).filter(Time.period_id == period_id, Time.employer_id == employer_id).first()
        vacation_time_query = session.query(
        func.sum(VacationTimes.vacation_hours).label("vacation_hours"),
        func.sum(VacationTimes.sicks_hours).label("sicks_hours")
        ).select_from(VacationTimes).filter(     
            VacationTimes.employer_id == employer_id,        
            cast(VacationTimes.month, Integer) < month,
            cast(VacationTimes.year, Integer) <= year
        ).group_by(VacationTimes.year).all()

        vacation_acum = 0
        sicks_acum = 0
        if vacation_time_query is not None and len(vacation_time_query) > 0:
            vacation_acum = vacation_time_query[0].vacation_hours
            sicks_acum = vacation_time_query[0].sicks_hours        

        payment_amount = calculate_payments()
        if (payment_amount < 0 ):
            payment_amount = payment_amount * -1
        
       
        print("---------------------time_query---------------")
        print(time_query)
        if (time_query is not None):
            info = {
            # EMPLOYERS INFO
            "first_name": employer.first_name,
            "salary": time_query.salary,
            "others": time_query.others,
            "vacation_time": minutes_to_time(( vacation_acum* 60)+time_to_minutes(employer.vacation_time)- time_to_minutes(total_vacation_time)),
            "sick_time": minutes_to_time((sicks_acum * 60)+time_to_minutes(employer.sick_time)- time_to_minutes(total_sick_time)),
            "others": time_query.others,
            "total_ss":round(all_time_query.total_ss, 2) ,
            "total_tax_pr":round(all_time_query.total_tax_pr, 2) ,
            "total_medicare":round(all_time_query.total_medicare, 2) ,
            "total_refund":round(all_time_query.total_refund, 2) ,
            "total_bonus":round(all_time_query.total_bonus, 2) ,
            "total_commissions" : round(all_time_query.total_commissions, 2) ,
            "total_tips" : round(all_time_query.total_tips, 2) ,
            "total_choferil" : round(all_time_query.total_choferil, 2) ,
            "total_inability" : round(all_time_query.total_inability, 2) ,
            "total_others" : round(all_time_query.total_others, 2) ,
            "total_asume" : round(all_time_query.total_asume, 2) ,
            "total_aflac" : round(all_time_query.total_aflac, 2) ,
            "total_donation" : round(all_time_query.total_donation, 2) ,
            "total_concessions" : round(all_time_query.total_concessions, 2) ,
            "total_social_tips" : round(all_time_query.total_social_tips, 2) ,
            "total_regular_pay": round(all_time_query.total_regular_pay, 2) ,
            "total_over_pay": round(all_time_query.total_over_pay, 2) ,
            "total_meal_pay": round(all_time_query.total_meal_pay, 2) ,
            "total_holyday_pay": round(all_time_query.total_holyday_pay, 2) ,
            "total_sick_pay": round(all_time_query.total_sick_pay, 2) ,
            "total_vacation_pay": round(all_time_query.total_vacation_pay, 2) ,
            "total_salary" : round(all_time_query.total_salary, 2) ,
            "total_regular_time" : total_regular_time ,
            "total_over_time" : total_over_time ,
            "total_meal_time" : total_mealt_time ,
            "holiday_time_pay" : time_query.holyday_pay,
            "total_holiday_pay" : all_time_query.total_holyday_pay ,

            "total_holiday_time" : total_holiday_time ,
            "total_sick_time" : total_sick_time ,
            "total_vacation_time" : total_vacation_time ,
            "total_col_1" : round(time_query.regular_pay+time_query.over_pay+time_query.meal_pay+time_query.holyday_pay+time_query.sick_pay+time_query.vacation_pay+ time_query.tips+ time_query.commissions+ time_query.concessions, 2) ,
            "total_col_1_year" : round(# The above code seems to be a comment in a Python script. The
            # comment is indicating that the code below it is related to a
            # query that is relevant for all time.
            all_time_query.total_regular_pay+all_time_query.total_over_pay+all_time_query.total_meal_pay+all_time_query.total_holyday_pay+all_time_query.total_sick_pay+all_time_query.total_vacation_pay+ all_time_query.total_tips+ all_time_query.total_commissions+ all_time_query.total_concessions, 2) ,
            
            "total_col_2" : round(time_query.asume+time_query.donation+payment_amount+time_query.aflac-time_query.refund, 2) ,
            "total_col_2_year" : round(all_time_query.total_asume+all_time_query.total_donation+total_payment_amount+all_time_query.total_aflac-all_time_query.total_refund, 2) ,

            "total_col_3" : round(time_query.tax_pr+time_query.secure_social+time_query.choferil+time_query.inability+time_query.medicare+time_query.social_tips, 2) ,
            "total_col_3_year" : round(all_time_query.total_tax_pr+all_time_query.total_ss+all_time_query.total_choferil+all_time_query.total_inability+all_time_query.total_medicare+all_time_query.total_social_tips, 2) ,
            

            "asume" : time_query.asume,

            "bonus": time_query.bonus,
            "aflac": time_query.aflac,

            "refund": time_query.refund,
            "donation": time_query.donation,
            "last_name": employer.last_name,
            "employer_address": employer.address,
            "employer_state": employer.address_state,
            "employer_address_number": employer.address_number,
            "employer_phone": employer.phone_number,
            "social_security_number": employer.social_security_number,
            #PERIOD INFO
            "actual_date": datetime.now().strftime("%d-%m-%Y"),
            "start_date": period.period_start,
            "end_date": period.period_end,
            "period_type": period.period_type.value,
            # COMPANY INFO
            "company": company.name,
            "physical_address": company.physical_address,
            # TIME INFO
            "regular_hours": time_query.regular_time,
            "over_hours": time_query.over_time,
            "meal_hours": time_query.meal_time,
            "holiday_hours": time_query.holiday_time,
            "sick_hours": time_query.sick_time,


            "vacation_hours": time_query.vacation_time,
            # PAY INFO
            "regular_pay": regular_pay(time_query.regular_amount, time_query.regular_time,time_query.salary,time_query.others,time_query.bonus),
            "overtime_pay": calculate_payment(time_query.over_time, time_query.over_amount),
            "meal_time_pay": calculate_payment(time_query.meal_time, time_query.meal_amount),
            "sick_pay": calculate_payment(time_query.sick_time, time_query.regular_amount),
            "vacation_pay": calculate_payment(time_query.vacation_time, time_query.regular_amount),
            "tips_pay": time_query.tips,
            "comissions": time_query.commissions,
            "income": calculate_income(),
            "concessions" : time_query.concessions,
            "payment_texts" : payment_texts,
            # YEAR INFO
            "year_curr":calculate_year_curr(period.period_type.value, regular_pay(time_query.regular_amount, time_query.regular_time,time_query.salary,time_query.others,time_query.bonus)),
            #RATE
            "regular_rate": time_query.regular_amount,
            "mealt_rate": time_query.meal_amount,
            "over_rate": time_query.over_amount,
            "employer_retained" : time_query.employer_retained,
            # DESCUENTOS INFO
            "secure_social": time_query.secure_social,
            "ss_tips": time_query.social_tips,
            "medicare": time_query.medicare,
            "inability": time_query.inability,
            "choferil": time_query.choferil,
            "egress": calculate_egress(),
            "tax_pr": time_query.tax_pr,
            # TOTAL INFO
            "total": calculate_total()
        }

            

            template = Template(voucherTemplate())
            rendered_html = template.render(info)


            pdf_file = f"./output_files/voucher_pago_{index}.pdf"
            HTML(string=rendered_html).write_pdf(pdf_file)
            pdf_files.append(pdf_file)


    doc3 = fitz.open()
    
    for file in pdf_files:
        doc3.insert_file(file)

    pdf_file = "./output_files/voucher_pago.pdf"
    doc3.save(pdf_file)


    return FileResponse(
        pdf_file,
        media_type="application/pdf",
        filename="Talonario_de_Pagos.pdf"
    )
     
        
        
def voucherTemplate():
    # Plantilla HTML
    template_html = """
            <!DOCTYPE html>
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Recibo de Pago</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    font-size: 10px; /* Tamaño de fuente más pequeño */
                    margin: 0;
                    background-color: #fff;
                    color: #000;
                }
                    .cheque {
    border: 2px solid black;
    padding: 20px;
    margin-top: 10px;

}
.titulo-cheque {
    font-weight: bold;
    font-size: 24px;
    text-align: center;
}
                .container {
                    width: 100%;

                    border: 1px solid #000;
                    padding: 12px;
                    box-sizing: border-box;
                }
                .header {
                    margin-bottom: 20px;
                }
                .header p {
                    margin:  0;
                }
                .flex-container {
                    display: flex;
                    justify-content: space-between;
                }
                table{
                    width: 100%;}
                .section {
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 20px;
                }
                .column {
                    width: 33%;
                    padding: 10px;
                    box-sizing: border-box;
                }
                .cheque  .column {
                    width:50%; }
                .totals {
                    text-align: right;
                }
                .totals p {
                    font-size: 1.2em;
                    font-weight: bold;
                }
                .grid-container {
                    display: grid;
                    grid-template-columns: auto auto;
                    column-gap: 20px;
                }
                .grid-container p {
                    margin: 5px 0;
                }
                .grid-container p.amount {
                    text-align: right;
                }
                .middle-column, .year-column {
                    width: 10%;
                    padding: 10px;
                    box-sizing: border-box;
                    margin-left: -30px;
                }
                .middle-column h4, .year-column h4 {
                    text-align: center;
                }
                .year-column p {
                    text-align: right;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">


                    <div class="flex-container">
                        <div class="column">
                        <p>NUMERO DE CHEQUE {{ company }}</p>
                    <p>Fecha: {{ actual_date }}</p>
                            <p>{{ first_name }} {{ last_name }}</p>
                            <p>{{ employer_address }}</p>
                            <p>{{ employer_state  }} {{ employer_address_number }}</p>
                        </div>
                        <div class="column">
                            <p>{{ first_name }} {{ last_name }}</p>
                            <p>NUMERO CHEQUE: {{ company }} {{ actual_date }}</p>
                            <p>MEMO: NÓMINA {{ start_date }} - {{ end_date }}</p>
                        </div>
                    </div>
                </div>
                <div style="width: 100%;display: flex;flex-direction: row;">
                    <div class="column">
                <table >
                    <tr>
                        <th>WAGES</th>
                        <th>CURR</th>
                        <th>YEAR</th>
                    </tr>
                    <tr>
                        <td>REG. PAY:</td>
                        <td>${{ regular_pay }}</td>
                        <td>${{total_regular_pay}}</td>
                    </tr>
                    <tr>
                        <td>VACATIONS:</td>
                        <td>${{ vacation_pay }}</td>
                        <td>${{ total_vacation_pay }}</td>
                    </tr>
                        <tr>
                        <td>SICK PAY:</td>
                        <td>${{ sick_pay }}</td>
                        <td>${{ total_sick_pay }}</td>
                    </tr>
                        <tr>
                        <td>OVER TIME:</td>
                        <td>${{ overtime_pay }}</td>
                        <td>${{ total_over_pay }}</td>
                    </tr>
                        <tr>
                        <td>MEAL TIME:</td>
                        <td>${{ meal_time_pay }}</td>
                        <td>${{ total_meal_pay }}</td>
                    </tr>
                    <tr>
                        <td>HOLIDAY TIME:</td>
                        <td>${{ holiday_time_pay }}</td>
                        <td>${{ total_holiday_pay }}</td>
                    </tr>
                        <tr>
                        <td>COMMI:</td>
                        <td>${{ comissions }}</td>
                        <td>${{ total_commissions }}</td>
                    </tr>
                        <tr>
                        <td>TIPS:</td>
                        <td>${{ tips_pay }}</td>
                        <td>${{ total_tips }}</td>
                    </tr>
                    <tr>
                        <td>CONCESSIONS:</td>
                        <td>${{ concessions }}</td>
                        <td>${{ total_concessions }}</td>
                    </tr>
                        <tr>
                        <td>SALARY:</td>
                        <td>${{ salary }}</td>
                        <td>${{ total_salary }}</td>
                    </tr>
                        <tr>
                        <td>BONUS:</td>
                        <td>${{ bonus }}</td>
                        <td>${{ total_bonus }}</td>
                    </tr>
                        <tr>
                        <td>OTHER 1:</td>
                        <td>${{ others }}</td>
                        <td>${{ total_others }}</td>
                    </tr>
                    <tr>
                        <td>Total:</td>
                        <td>${{ total_col_1 }}</td>
                        <td>${{total_col_1_year}}</td>
                    </tr>
                </table>
                </div>
                <div class="column">
                <table >
                    <tr>
                        <th></th>
                        <th>CURR</th>
                        <th>YEAR</th>
                    </tr>
                    <tr>
                        <td>
Gastos Reembolsados:</td>
                        <td>${{ refund }}</td>
                        <td>${{ total_refund }}</td>
                    </tr>
                    <tr>
                        <td>ASUME:</td>
                        <td>${{ asume }}</td>
                        <td>${{total_asume}}</td>
                    </tr>
                        <tr>
                        <td>DONATIVOS:</td>
                        <td>${{ donation }}</td>
                        <td>${{ total_donation }}</td>
                    </tr>
                        <tr>
                        <td>AFLAC:</td>
                        <td>${{ aflac }}</td>
                        <td>${{ total_aflac }}</td>
                    </tr>

                    


                    
                        {{payment_texts}}
                        <tr>
                        <td>Total:</td>
                        <td>${{ total_col_2 }}</td>
                        <td>${{ total_col_2_year }}</td>
                    </tr>
                        <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>
                        <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>
                        <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>
                    
                        <tr>
                        <td>REG RATE:</td>
                        <td>${{ regular_rate }}</td>
                        <td></td>
                    </tr>
                    <tr>
                        <td>MEALT RATE:</td>
                        <td>${{ mealt_rate }}</td>
                        <td></td>
                    </tr>
                    <tr>
                        <td>OVER RATE:</td>
                        <td>${{ over_rate }}</td>
                        <td></td>
                    </tr>
                    <tr>
                        <td>% RETENCIÓN:</td>
                        <td>${{ employer_retained }} %</td>
                        <td></td>
                    </tr>

                </table>
                </div>
                <div class="column">
                <table >
                    <tr>
                        <th></th>
                        <th>CURR</th>
                        <th>YEAR</th>
                    </tr>
                    <tr>
                        <td>INC TAX:</td>
                        <td>${{ tax_pr }}</td>
                        <td>${{ total_tax_pr }}</td>
                    </tr>

                    <tr>
                        <td>SEGURO SOCIAL:</td>
                        <td>${{ secure_social }}</td>
                        <td>${{total_ss}}</td>
                    </tr>

                        <tr>
                        <td>SS TIPS:</td>
                        <td>${{ ss_tips }}</td>
                        <td>${{ total_social_tips }}</td>
                    </tr>
                        <tr>
                        <td>MEDICARE:</td>
                        <td>${{ medicare }}</td>
                        <td>${{ total_medicare }}</td>
                    </tr>
                        <tr>
                        <td>DISABILITY:</td>
                        <td>${{ inability }}</td>
                        <td>${{ total_inability }}</td>
                    </tr>
                        <tr>
                        <td>CHAUFFEUR W:</td>
                        <td>${{ choferil }}</td>
                        <td>${{ total_choferil }}</td>
                    </tr>
                    
                        <tr>
                        <td>Total:</td>
                        <td>${{ total_col_3 }}</td>
                        <td>${{ total_col_3_year }}</td>
                    </tr>
                        <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>
                        <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>
                        <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>
                        <tr>
                        <td>REG. HOURS:</td>
                        <td>{{ regular_hours }}</td>
                        <td>{{ total_regular_time }}</td>
                    </tr>
                    <tr>
                        <td>VAC HOURS:</td>
                        <td>{{ vacation_hours }}</td>
                        <td>{{ total_vacation_time }}</td>
                    </tr>
                    <tr>
                        <td>MEAL HOURS:</td>
                        <td>{{ meal_hours }}</td>
                        <td>{{ total_meal_time }}</td>
                    </tr>
                        <tr>
                        <td>SICK HOURS:</td>
                        <td>{{ sick_hours }}</td>
                        <td>{{ total_sick_time }}</td>
                    </tr>
                        <tr>
                        <td>OVER. HOURS:</td>
                        <td>{{ over_hours }}</td>
                        <td>{{ total_over_time }}</td>
                    </tr>
                    <tr>
                        <td>HOLIDAY HOURS:</td>
                        <td>{{ holiday_hours }}</td>
                        <td>{{ total_holiday_time }}</td>
                    </tr>
                        
                    
                    
                    
                </table>
                </div>
</div>
<div class="footer" style="  padding-left: 12px;">
                    <p>VAC ACUM: {{vacation_time}} ENF ACUM: {{sick_time}}</p>
                </div>
                <div class="totals">
                    <p>Total: ${{ total }}</p>
                </div>

                

            
            </div>
                    <div class="cheque">
<div>


                    <div style="font-size: 14px;" class="flex-container">
                        <div class="column" style="width: 70%;">



                                                    <p > {{ company }}</p>
                                                    <p style="margin-top: 0px"> {{ physical_address }}</p>

                            <p style="margin-top: 24px;width: 100%;            ">PAY TO ORDER OF: <span style="border-bottom: 1px solid black;padding: 2px 16px 2px 16px;">      {{ first_name }} {{ last_name }}             </p>
                        
                    
                            
                            <p style="margin-top: 24px;">FOR: ________________</p>
                            
                        </div>
                        <div class="column" style="text-align: right;width: 30%;">
                            <p>Fecha: {{ actual_date }}</p>
                            <p   style="margin-top: 48px;">Total: ${{ total }}</p>
                            <p style="margin-top: 32px;">FOR: ________________</p>
                        </div>
                    </div>
                </div>




        """
    return template_html