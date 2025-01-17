from models.queries.queryUtils import getCompany, getEmployers7000, getEmployees, getAmountVariosCompany, roundedAmount, getAmountVariosCompanyGroupByMonth, getTotalAmountAndExemptAmount
from utils.time_func import getPeriodTime
from utils.country import COUNTRY
from datetime import datetime
def queryForm499(company_id, year, period):
    
    # Data Active
    # Get company and employees
    data  = getCompany(company_id)
    company = data['company']
    account = data['account']
    date_period = getPeriodTime(period, year)

    amountVariosExempt = getTotalAmountAndExemptAmount(company.id, date_period)
    employers = getEmployees(company.id)
    amountVarios = getAmountVariosCompany(company.id, year, period)
    amountVariosByMonth = getAmountVariosCompanyGroupByMonth(company.id, year, period)

    # Address Company
    postalAddressCompany = company.postal_address if company.postal_address is not None else ''
    statePostalAddressCompany = company.state_postal_addess if company.state_postal_addess is not None else ''
    countryPostalAddressCompany = COUNTRY[int(company.country_postal_address)-1] if COUNTRY[int(company.country_postal_address)-1] is not None else ''
    zipcodePostalAddressCompany = company.zipcode_postal_address if company.zipcode_postal_address is not None else ''

    physicalAddressCompany = company.physical_address if company.physical_address is not None else ''
    statePhysicalAddressCompany = company.state_physical_address if company.state_physical_address is not None else ''
    countryPhysicalAddressCompany = COUNTRY[int(company.country_physical_address)-1] if COUNTRY[int(company.country_physical_address)-1] is not None else ''
    zipcodePhysicalAddressCompany = company.zipcode_physical_address if company.zipcode_physical_address is not None else ''

    # Calculate
    rounded_amount_tips = roundedAmount(amountVarios.tips)
    total_salary_compensation = roundedAmount(amountVariosExempt['total'])
    total_retentions = roundedAmount(amountVarios.taxes_pr)
    date_period_end = date_period['end']
    meses_espanol = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
    7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}
    # Obtener el día y el mes en números
    dia = date_period_end.day
    mes = date_period_end.month

    # Obtener el nombre del mes en español
    nombre_mes = meses_espanol[mes]
    # Formatear la fecha
    fecha_formateada = f"{dia}  {nombre_mes}  {date_period_end.year}"
    # Part 3 Page 2 calculation
    month_total_liabilities = []
    for index, amount in enumerate(amountVariosByMonth):
        print("-----------------month-------------------")
        print(amount.month)
        index += 1
        total = roundedAmount(amount.taxes_pr)
        mitad = total / 2
        dataTmp = {
            'total': str(total),
        }
        if total_retentions <= 2500:
            dataTmp['text_month_3_day_28'] = str(total)
            dataTmp['text_month_3_liability'] = str(total)
        elif total_retentions >= 2500 and total_retentions <= 100000:
            dataTmp[f'text_month_{index}_day_28'] = str(total)
            dataTmp[f'text_month_{index}_liability'] = str(total)
        else:
            dataTmp[f'text_month_{index}_day_14'] = str(mitad)
            dataTmp[f'text_month_{index}_day_28'] = str(mitad)
            dataTmp[f'text_month_{index}_liability'] = str(total)

        month_total_liabilities.append(dataTmp)

    # Data for PDF
    data = {
        'date_end' : fecha_formateada,
        'firma_contador' : account.company,
        'text_code_naics' : company.industrial_code,
        'text_name_company': company.name if company.name is not None else '', # company name
        'text_ein': company.number_patronal if company.number_patronal is not None else '', # company ein
        'text_name_contact' : company.contact if company.contact is not None else '', # contact name
        'text_phone_company': str(company.phone_number) if company.phone_number is not None else '', # company phone number
        'personal_contact_number': str(company.contact_number) if company.contact_number is not None else '', # personal contact number
       
        'textarea_address_business':   company.name +"\n" + physicalAddressCompany  +", " +statePhysicalAddressCompany+", " + countryPhysicalAddressCompany +", " + zipcodePhysicalAddressCompany, # address company
'textarea_address_company': company.name +"\n" + postalAddressCompany +", " + statePostalAddressCompany +", " + countryPostalAddressCompany + " " +zipcodePostalAddressCompany if company.name is not None else '',
        'accountent_name' : account.name + " " + account.first_last_name ,
        'account_number' : account.identidad_efile ,

        'date' : datetime.now().strftime("%d-%m-%Y"),
        'address' : account.address ,
        'text_month_1_day_28':month_total_liabilities[0]['total'] if len(month_total_liabilities) > 0 else '0',
        'text_month_2_day_28':month_total_liabilities[1]['total'] if len(month_total_liabilities) > 1 else '0',

 
        'text_total_employees': str(amountVariosExempt['count']), # total number of employees
        'text_total_exempt': str(amountVariosExempt['exempt']), # total exempt
        'text_total_compensation_withholding': str(total_salary_compensation), # total salary compensation
        'text_total_tips_withholding': str(rounded_amount_tips), # total tip compensation
        'text_total_withholding': str(total_retentions), # total retentions
        'text_total_quarter_liability': str(total_retentions), # total retentions
        'text_first_month_liability': month_total_liabilities[0]['total'] if len(month_total_liabilities) > 0 else '0',
        'text_second_month_liability': month_total_liabilities[1]['total'] if len(month_total_liabilities) > 1 else '0',
        'text_third_month_liability': month_total_liabilities[2]['total'] if len(month_total_liabilities) > 2 else '0',
        'text_total_liability_quarter': str(total_retentions), # total retentions
    }

    for value in month_total_liabilities:
        data.update(value)


    return data
    



