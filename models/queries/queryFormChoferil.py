from models.queries.queryUtils import getCompany, getEmployersChoferilAmount, roundedAmount
from utils.time_func import getPeriodTime
from datetime import datetime, date
from utils.country import COUNTRY
def queryFormChoferil (company_id, year, periodo):

    company = getCompany(company_id)['company']

    date_period = getPeriodTime(periodo, year)
    dateToday = datetime.now()

    employees = getEmployersChoferilAmount(company.id, date_period)
    # Address Company
    postalAddressCompany = company.postal_address if company.postal_address is not None else ''
    statePostalAddressCompany = company.state_postal_addess if company.state_postal_addess is not None else ''
    countryPostalAddressCompany = COUNTRY[int(company.country_postal_address)-1] if COUNTRY[int(company.country_postal_address)-1] is not None else ''
    zipcodePostalAddressCompany = company.zipcode_postal_address if company.zipcode_postal_address is not None else ''
    index = 1
    totalAmount = 0
    totalWeeks = 0
    arrayEmployees = []
    for value in employees:
        data = {
            f'text_social_employee_{index}': value.social_security_number if value.social_security_number is not None else '',
            f'text_name_{index}': f'{value.first_name} {value.last_name}',
            f'text_license_number_{index}': value.licence if value.licence is not None else '',
            f'text_total_weeks_{index}': str(value.total_weeks) if value.total_weeks is not None else '',
        }

        totalWeeks += value.total_weeks
        arrayEmployees.append(data)
        totalAmount += roundedAmount(value.total)
        index += 1

    data = {
        'text_date_end': company.choferil_number+" "+str(date_period['end']),
        'text_total_weeks_paid': str(totalWeeks),
        'text_total_tax_due': str(float(totalWeeks) * float(company.driver_rate)),
        'text_payment_ampunt': '0',
        'text_position': '--',
        'company_info': company.name +"\n" + postalAddressCompany +", " + statePostalAddressCompany +", " + countryPostalAddressCompany + " " +zipcodePostalAddressCompany if company.name is not None else '',
        'text_phone': company.phone_number if company.phone_number is not None else '',
        'text_date': f'{dateToday.year}-{dateToday.month}-{dateToday.day}'
    }

    for employee in arrayEmployees:
        data.update(employee)

    return data