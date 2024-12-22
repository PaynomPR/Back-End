from models.companies import Companies
from models.employers import Employers
from models.periods import Period
from models.time import Time
from database.config import session
from random import randint
from models.accountant import Accountant
from sqlalchemy import func, and_ , distinct
from datetime import date
from utils.time_func import getPeriodTime, getAgeEmployer
import calendar
from sqlalchemy import func, cast, Integer
from sqlalchemy import extract

def addZeroNumber(value):
    return f'{value}0' if len(value) == 1 else value

def getRandomIrs():
    return f'{randint(10000, 99999)}'

def addDecimal(number):
  array = str(number).split('.') if number != 0 else '0.0'.split('.')
  if len(array) == 1:
    array.append('00')
  else:
    array[1] = addZeroNumber(array[1])

  return array


def getTotalAmountAndExemptAmount(company_id, date_period):
    result = session.query(
      func.sum(Time.regular_pay + Time.over_pay + Time.vacation_pay + Time.meal_pay + Time.sick_pay + Time.holyday_pay  + Time.commissions + Time.concessions ).label('total'), Employers.id, Employers.birthday
      ).join(Employers, Employers.id == Time.employer_id
      ).join(Period, Period.id == Time.period_id).filter(     
        Employers.company_id == company_id,
        Period.period_end >= date_period['start'],
        Period.period_end <= date_period['end']
    ).group_by(Employers.id).all()

    total = 0
    exempt_amount = 0
    count = 0
    not_exempt_amount = 0
    for payment in result:
      count = count +1
      total += payment[0]
      if payment[2] is not None:
        birthday = str(payment[2]).split('-') if payment[2] is not None else '0000-00-00'.split('-')
        print("---------------------")
        print(payment[2])
        age = getAgeEmployer(birthday)
        if age < 26:
          exempt_amount += payment[0]
        else:
          not_exempt_amount  += payment[0]
           


    return {
      'count' : count,
      'total': not_exempt_amount,
      'exempt': exempt_amount
    }


def getTotalAmount(company_id, date_period):
    result = session.query(
      func.sum(Time.regular_pay + Time.over_pay + Time.vacation_pay + Time.meal_pay + Time.sick_pay + Time.holyday_pay)
      ).join(Employers, Employers.id == Time.employer_id
      ).join(Period, Period.id == Time.period_id).filter(     
        Employers.company_id == company_id,
        Period.period_start >= date_period['start'],
        Period.period_end <= date_period['end']
      
    ).scalar()

    return result if result is not None else 0

def getTotalAmountAndWeeks(company_id, year, periodo):
    period = getPeriodTime(periodo, year)
    diferent = period['end'] - period['start']
    weeks = diferent.days // 7

    result = session.query(
      func.sum(Time.regular_pay + Time.over_pay + Time.vacation_pay + Time.meal_pay + Time.sick_pay + Time.holyday_pay)
      ).join(Employers, Employers.id == Time.employer_id
      ).join(Period, Period.id == Time.period_id).filter(     
        Employers.company_id == company_id,
        Period.period_start >= period['start'],
        Period.period_end <= period['end']
      ).scalar()

    return {
      'total_amount': result if result is not None else 0,
      'weeks': weeks
    }

def getAmountVariosByCompany(company_id, year, period = None):
    date_start = date(year, 1, 1)
    date_end = date(year, 12, 31)

    result = session.query(
      func.sum(Time.regular_pay + Time.over_pay + Time.vacation_pay + Time.meal_pay + Time.sick_pay + Time.holyday_pay).label('wages'),
      func.sum(Time.commissions).label('commissions'),
      func.sum(Time.concessions).label('concessions'),
      func.sum(Time.tips).label('tips'),
      Employers,
      func.sum(Time.donation).label('donation'),
      func.sum(Time.refund).label('refunds'),
      func.sum(Time.aflac).label('aflac'),
      func.sum(Time.medicare).label('medicares'),
      func.sum(Time.bonus).label('bonus'),
      func.sum(Time.social_tips).label('social_tips'),
      func.sum(Time.secure_social).label('secure_social'),
      func.sum(Time.tax_pr).label('taxes_pr')
      ).join(Period, Period.id == Time.period_id
      ).join(Employers, Employers.id == Time.employer_id
      ).filter(
          Employers.company_id == company_id,
          Period.period_start >= date_start,
          Period.period_end <= date_end
      ).group_by(Employers.id).all()

    return result

def getAmountVarios(employer_id, year, period = None):
    date_start = date(year, 1, 1)
    date_end = date(year, 12, 31)

    result = session.query(
      func.sum(Time.regular_pay + Time.over_pay + Time.vacation_pay + Time.meal_pay + Time.sick_pay + Time.holyday_pay).label('wages'),
      func.sum(Time.commissions).label('commissions'),
      func.sum(Time.concessions).label('concessions'),
      func.sum(Time.tips).label('tips'),
      func.sum(Time.donation).label('donation'),
      func.sum(Time.refund).label('refunds'),
      func.sum(Time.aflac).label('aflac'),
      func.sum(Time.medicare).label('medicares'),
      func.sum(Time.bonus).label('bonus'),
      func.sum(Time.social_tips).label('social_tips'),
      func.sum(Time.secure_social).label('secure_social'),
      func.sum(Time.tax_pr).label('taxes_pr')
      ).join(Period, Period.id == Time.period_id
      ).join(Employers, Employers.id == Time.employer_id
      ).filter(
          Employers.id == employer_id,
          Period.period_start >= date_start,
          Period.period_end <= date_end
      ).all()

    return result[0]

def getAmountByTrimestre(company_id, year):
    quarter_amounts = {'1': 0, '2': 0, '3': 0, '4': 0}
    quarter_starts = [1, 4, 7, 10]

    for i, start_month in enumerate(quarter_starts):
        date_start = date(year, start_month, 1)
        # Calculate end date based on the actual number of days in the month
        date_end = date(year, start_month + 2, calendar.monthrange(year, start_month + 2)[1])
        quarter_amount = getAmountByCompany(company_id, date_start, date_end)

        if quarter_amount:
            quarter_amounts[str(i + 1)] = quarter_amount[0].wages
        else:
            quarter_amounts[str(i + 1)] = 0

    return quarter_amounts


def getAmountByMonth(company_id, year,month): 
    date_start = date(year, month, 1)
    date_end = date(year, month, calendar.monthrange(year, month )[1]) 
    
    quarter_amount = getAmountByCompany(company_id, date_start, date_end)
    if quarter_amount:
      return quarter_amount
    else:
      return 0

def getAmountVariosCompany(company_id, year, period = None):
    date_start = date(year, 1, 1)
    date_end = date(year, 12, 31)

    if period is not None:
      period = getPeriodTime(period, year)
      date_start = period['start']
      date_end = period['end']

    result = session.query(
       
      func.sum(Time.regular_pay + Time.over_pay + Time.vacation_pay + Time.meal_pay + Time.sick_pay + Time.holyday_pay).label('wages'),
      func.sum(Time.regular_pay).label('regular_pay'),
      func.sum( Time.over_pay ).label('over_pay'),
      func.sum( Time.vacation_pay ).label('vacation_pay'),
      func.sum( Time.meal_pay ).label('meal_pay'),
      func.sum( Time.sick_pay ).label('sick_pay'),
      func.sum(Time.holyday_pay).label('holyday_pay'),
      func.sum(Time.commissions).label('commissions'),
      func.sum(Time.concessions).label('concessions'),
      func.sum(Time.tips).label('tips'),
      func.sum(Time.donation).label('donation'),
      func.sum(Time.refund).label('refunds'),
      func.sum(Time.medicare).label('medicares'),
      func.sum(Time.bonus).label('bonus'),
      func.sum(Time.social_tips).label('social_tips'),
      func.sum(Time.secure_social).label('secure_social'),
      func.sum(Time.tax_pr).label('taxes_pr')
      ).select_from(Period).join(Time, Period.id == Time.period_id ).join(Employers, Time.employer_id == Employers.id).filter( Employers.company_id == company_id,  Period.period_end >= date_start ,Period.period_end <= date_end ).all()
      
    return result[0]



def getAmountVariosCompanyByMouth(company_id, year):
    date_start = date(year, 1, 1)
    date_end = date(year, 12, 31)
    result = session.query(
  
        extract('year', Period.period_end).label('year'),
    extract('month', Period.period_end).label('month'),
    func.sum(Time.regular_pay + Time.over_pay + Time.vacation_pay + Time.meal_pay + Time.sick_pay + Time.holyday_pay + Time.commissions + Time.concessions+ Time.tips).label('wages'),
    func.sum(Time.regular_pay).label('regular_pay'),
    func.sum(Time.over_pay).label('over_pay'),
    func.sum(Time.vacation_pay).label('vacation_pay'),
    func.sum(Time.meal_pay).label('meal_pay'),
    func.sum(Time.sick_pay).label('sick_pay'),
    func.sum(Time.holyday_pay).label('holyday_pay'),
    func.sum(Time.commissions).label('commissions'),
    func.sum(Time.concessions).label('concessions'),
    func.sum(Time.tips).label('tips'),
    func.sum(Time.donation).label('donation'),
    func.sum(Time.refund).label('refunds'),
    func.sum(Time.medicare).label('medicares'),
    func.sum(Time.bonus).label('bonus'),
    func.sum(Time.social_tips).label('social_tips'),
    func.sum(Time.secure_social).label('secure_social'),
    func.sum(Time.tax_pr).label('taxes_pr')
    ).select_from(Period) \
    .join(Time, Period.id == Time.period_id) \
    .join(Employers, Time.employer_id == Employers.id) \
    .filter(Employers.company_id == company_id, Period.period_end >= date_start, Period.period_end <= date_end) \
    .group_by(extract('year', Period.period_end), extract('month', Period.period_end)) \
.order_by(extract('year', Period.period_end), extract('month', Period.period_end)) \
    .all()
    return result

   
def convert_to_seconds(time_string):
    """Convierte una cadena de tiempo en formato HH:MM a segundos."""
    hours, minutes = map(int, time_string.split(':'))
    return hours * 3600 + minutes * 60

    
def getBonusCompany(company_id, date_start, date_end,bonus):
    from collections import defaultdict

    # ... (tu código existente)

    # Obtener todos los registros sin agrupar
    all_times_query = session.query(Time,Employers).select_from(Period).join(Time, Period.id == Time.period_id).join(Employers, Employers.id == Time.employer_id).filter(Period.period_end >= date_start, Period.period_end <= date_end, Employers.company_id == company_id).all()

    # Crear un diccionario para almacenar los totales por empleado
    employee_totals = defaultdict(lambda: {
        'total_time': 0,      
        'wages': 0,
       
        # ... (otros campos)
    })

    # Iterar sobre los registros y acumular los totales
    for time_entry in all_times_query:
        employer_id = time_entry.Time.employer_id
        employee_totals[employer_id]['employer_id'] = employer_id
        employee_totals[employer_id]['name'] = time_entry.Employers.first_name
        employee_totals[employer_id]['last_name'] = time_entry.Employers.last_name

        if bonus.reg:
          employee_totals[employer_id]['total_time'] += convert_to_seconds(time_entry.Time.regular_time)
          employee_totals[employer_id]['total_time'] += time_entry.Time.hours_worked_salary * 3600
        if bonus.over:
          employee_totals[employer_id]['total_time'] += convert_to_seconds(time_entry.Time.over_time)
        if bonus.vacations:
          employee_totals[employer_id]['total_time'] += convert_to_seconds(time_entry.Time.vacation_time)
        if bonus.sick:
          employee_totals[employer_id]['total_time'] += convert_to_seconds(time_entry.Time.sick_time)
           



        employee_totals[employer_id]['wages'] += time_entry.Time.regular_pay + time_entry.Time.over_pay + time_entry.Time.vacation_pay + time_entry.Time.meal_pay + time_entry.Time.sick_pay + time_entry.Time.holyday_pay + time_entry.Time.commissions + time_entry.Time.concessions + time_entry.Time.tips
        # ... (sumar otros campos)
   

    # Return the employee totals as a list of dictionaries
    return list(employee_totals.values())
   
def getAmountCSFECompany(company_id, date_start, date_end ):
    result = session.query(
      
      func.sum(Time.regular_pay + Time.over_pay + Time.vacation_pay + Time.meal_pay + Time.sick_pay + Time.holyday_pay+ Time.commissions +Time.concessions+Time.tips).label('wages'),
     
     Time.employer_id.label('employer_id'),
      func.sum(Time.regular_pay).label('regular_pay'),
      func.sum( Time.over_pay ).label('over_pay'),
      func.sum( Time.vacation_pay ).label('vacation_pay'),
      func.sum( Time.meal_pay ).label('meal_pay'),
      func.sum( Time.sick_pay ).label('sick_pay'),
      func.sum(Time.holyday_pay).label('holyday_pay'),
      func.sum(Time.commissions).label('commissions'),
      func.sum(Time.concessions).label('concessions'),
      func.sum(Time.tips).label('tips'),
      func.sum(Time.donation).label('donation'),
      func.sum(Time.refund).label('refunds'),
      
      func.sum(Time.medicare).label('medicares'),
      func.sum(Time.bonus).label('bonus'),
      func.sum(Time.social_tips).label('social_tips'),
      func.sum(Time.secure_social).label('secure_social'),
      func.sum(Time.tax_pr).label('taxes_pr')
      ).select_from(Period).join(Time, Period.id == Time.period_id ).join(Employers, Time.employer_id == Employers.id).filter( Employers.company_id == company_id,  Period.period_end >= date_start , Period.period_end <= date_end ).group_by(Time.employer_id).all()
    
    return result or []  # Return an empty list if result is None


def getAmountByCompany(company_id, date_start, date_end ):
    result = session.query(
     
      func.sum(Time.regular_pay + Time.over_pay + Time.vacation_pay + Time.meal_pay + Time.sick_pay + Time.holyday_pay+ Time.commissions +Time.concessions+Time.tips).label('wages'),
      Employers.company_id,
    
      func.sum(Time.regular_pay).label('regular_pay'),
      func.sum( Time.over_pay ).label('over_pay'),
      func.sum( Time.vacation_pay ).label('vacation_pay'),
      func.sum( Time.meal_pay ).label('meal_pay'),
      func.sum( Time.sick_pay ).label('sick_pay'),
      func.sum(Time.holyday_pay).label('holyday_pay'),
      func.sum(Time.commissions).label('commissions'),
      func.sum(Time.concessions).label('concessions'),
      func.sum(Time.tips).label('tips'),
      func.sum(Time.donation).label('donation'),
      func.sum(Time.refund).label('refunds'),
      
      func.sum(Time.medicare).label('medicares'),
      func.sum(Time.bonus).label('bonus'),
      func.sum(Time.social_tips).label('social_tips'),
      func.sum(Time.secure_social).label('secure_social'),
      func.sum(Time.tax_pr).label('taxes_pr')
      ).select_from(Period).join(Time, Period.id == Time.period_id ).join(Employers, Time.employer_id == Employers.id).filter( Employers.company_id == company_id,  Period.period_end >= date_start , Period.period_end <= date_end ).group_by(Employers.company_id).all()
    
    return result or []  # Return an empty list if result is None
def getAmountGroupEmployerWages(company_id, start , end ):
    
    result = session.query(
      
      func.sum(Time.regular_pay + Time.over_pay + Time.vacation_pay + Time.meal_pay + Time.sick_pay + Time.holyday_pay+ Time.commissions +Time.concessions+Time.tips).label('wages'),
      Employers.id,
     Employers,
      func.sum(Time.regular_pay).label('regular_pay'),
      func.sum( Time.over_pay ).label('over_pay'),
      func.sum( Time.vacation_pay ).label('vacation_pay'),
      func.sum( Time.meal_pay ).label('meal_pay'),
      func.sum( Time.sick_pay ).label('sick_pay'),
      func.sum(Time.holyday_pay).label('holyday_pay'),
      func.sum(Time.commissions).label('commissions'),
      func.sum(Time.concessions).label('concessions'),
      func.sum(Time.tips).label('tips'),
      func.sum(Time.donation).label('donation'),
      func.sum(Time.refund).label('refunds'),
      
      func.sum(Time.medicare).label('medicares'),
      func.sum(Time.bonus).label('bonus'),
      func.sum(Time.social_tips).label('social_tips'),
      func.sum(Time.secure_social).label('secure_social'),
      func.sum(Time.tax_pr).label('taxes_pr')
      ).select_from(Period).join(Time, Period.id == Time.period_id ).join(Employers, Time.employer_id == Employers.id).filter( Employers.company_id == company_id,  Period.period_end >= start , Period.period_end <= end ).group_by(Employers.id).all()
    
    return result or []  # Return an empty list if result is None
def getAmountGroupEmployer(company_id, year , month ):
    date_start = date(year, month, 1)
    date_end = date(year, month, calendar.monthrange(year, month )[1])
    result = session.query(
      
      func.sum(Time.regular_pay + Time.over_pay + Time.vacation_pay + Time.meal_pay + Time.sick_pay + Time.holyday_pay+ Time.commissions +Time.concessions+Time.tips).label('wages'),
      Employers.id,
    
      func.sum(Time.regular_pay).label('regular_pay'),
      func.sum( Time.over_pay ).label('over_pay'),
      func.sum( Time.vacation_pay ).label('vacation_pay'),
      func.sum( Time.meal_pay ).label('meal_pay'),
      func.sum( Time.sick_pay ).label('sick_pay'),
      func.sum(Time.holyday_pay).label('holyday_pay'),
      func.sum(Time.commissions).label('commissions'),
      func.sum(Time.concessions).label('concessions'),
      func.sum(Time.tips).label('tips'),
      func.sum(Time.donation).label('donation'),
      func.sum(Time.refund).label('refunds'),
      
      func.sum(Time.medicare).label('medicares'),
      func.sum(Time.bonus).label('bonus'),
      func.sum(Time.social_tips).label('social_tips'),
      func.sum(Time.secure_social).label('secure_social'),
      func.sum(Time.tax_pr).label('taxes_pr')
      ).select_from(Period).join(Time, Period.id == Time.period_id ).join(Employers, Time.employer_id == Employers.id).filter( Employers.company_id == company_id,  Period.period_end >= date_start , Period.period_end <= date_end ).group_by(Employers.id).all()
    
    return result or []  # Return an empty list if result is None
       

def getByEmployerAmountCompany(company_id, year, period = None):
    date_start = date(year, 1, 1)
    date_end = date(year, 12, 31)

    if period is not None:
      period = getPeriodTime(period, year)
      date_start = period['start']
      date_end = period['end']

    result = session.query(
      func.sum(Time.regular_pay + Time.over_pay + Time.vacation_pay + Time.meal_pay + Time.sick_pay + Time.holyday_pay+ Time.tips).label('wages'),
      func.sum(Time.regular_pay).label('regular_pay'),
      func.sum( Time.over_pay ).label('over_pay'),
      func.sum( Time.vacation_pay ).label('vacation_pay'),
      func.sum( Time.meal_pay ).label('meal_pay'),
      func.sum( Time.sick_pay ).label('sick_pay'),
      func.sum(Time.holyday_pay).label('holyday_pay'),
      func.sum(Time.commissions).label('commissions'),
      func.sum(Time.concessions).label('concessions'),
      func.sum(Time.tips).label('tips'),
      func.sum(Time.donation).label('donation'),
      func.sum(Time.refund).label('refunds'),
      func.sum(Time.medicare).label('medicares'),
      func.sum(Time.bonus).label('bonus'),
      func.sum(Time.social_tips).label('social_tips'),
      func.sum(Time.secure_social).label('secure_social'),
      func.sum(Time.tax_pr).label('taxes_pr')
      ).select_from(Period).join(Time, Period.id == Time.period_id ).join(Employers, Time.employer_id == Employers.id).filter( Employers.company_id == company_id,  Period.year == year ).group_by(Time.employer_id).all()
      
    return result


def getAmountVariosCompanyGroupByMonth(company_id, year, period = None):
    date_start = date(year, 1, 1)
    date_end = date(year, 12, 31)

    if period is not None:
      period = getPeriodTime(period, year)
      date_start = period['start']
      date_end = period['end']
    
    result = session.query(
      func.sum(Time.regular_pay + Time.over_pay + Time.vacation_pay + Time.meal_pay + Time.sick_pay + Time.holyday_pay).label('wages'),
      func.sum(Time.commissions).label('commissions'),
      func.sum(Time.concessions).label('concessions'),
      func.sum(Time.tips).label('tips'),
      func.sum(Time.donation).label('donation'),
      func.sum(Time.refund).label('refunds'),
      func.sum(Time.medicare).label('medicares'),
      func.sum(Time.bonus).label('bonus'),
      func.sum(Time.social_tips).label('social_tips'),
      func.sum(Time.secure_social).label('secure_social'),
      func.sum(Time.tax_pr).label('taxes_pr'),
      func.date_trunc('month', Period.period_end).label('month'),
      ).join(Employers, Time.employer_id == Employers.id
      ).join(Period, Period.id == Time.period_id 
      
      ).filter( Employers.company_id == company_id, Period.period_end >= date_start, Period.period_end <= date_end 
      ).group_by(func.date_trunc('month', Period.period_end)) \
  .having(func.date_trunc('month', Period.period_end) <= date_end) \
  .order_by(func.date_trunc('month', Period.period_end)).all()

    return result

def getEmployers7000(company_id, date_period):
    arrayTotal = session.query(
      func.sum(Time.regular_pay + Time.over_pay + Time.vacation_pay + Time.meal_pay + Time.sick_pay + Time.holyday_pay + Time.commissions + Time.concessions + Time.bonus).label('total')
      ).join(Employers, Time.employer_id == Employers.id
      ).join(Period, Period.id == Time.period_id ).filter(
        Employers.company_id == company_id,
        Period.period_start >= date_period['start'],
        Period.period_end <= date_period['end']      
    ).group_by(Time.employer_id).all()
    result = 0
    for value in arrayTotal:
        max_7000 = (value.total - 7000) if value.total > 7000 else value.total
        result += max_7000

    return result
def getEmployersAmountToDate(company_id,year, month):
    date_start = date(year, 1, 1)
    date_end = date(year, month, calendar.monthrange(year, month)[1])
    arrayTotal = session.query(
      func.sum(Time.regular_pay + Time.over_pay + Time.vacation_pay + Time.meal_pay + Time.sick_pay + Time.holyday_pay  + Time.commissions + Time.concessions+ Time.tips).label('total'),
      Employers.id,
      Employers.first_name,
      Employers.last_name,
      Employers.licence,
      Employers.social_security_number,
      func.count(Time.period_id).label('total_weeks'),
      ).select_from(Period).join(Time, Period.id == Time.period_id ).join(Employers, Time.employer_id == Employers.id
      ).filter(
        Employers.company_id == company_id,
        Period.period_end >= date_start,
        Period.period_end <= date_end
        
    ).group_by(Employers.id).all()

    return arrayTotal
def getEmployersAmount(company_id, date_period):
    arrayTotal = session.query(
      func.sum(Time.regular_pay + Time.over_pay + Time.vacation_pay + Time.meal_pay + Time.sick_pay + Time.holyday_pay  + Time.commissions + Time.concessions+ Time.tips).label('total'),
      Employers.id,
      Employers.first_name,
      Employers.last_name,
      Employers.licence,
      Employers.social_security_number,
      func.count(Time.period_id).label('total_weeks'),
      ).select_from(Period).join(Time, Period.id == Time.period_id ).join(Employers, Time.employer_id == Employers.id
      ).filter(
        Employers.company_id == company_id,
        Period.period_end >= date_period['start'],
        Period.period_end <= date_period['end']
        
    ).group_by(Employers.id).all()

    return arrayTotal

def getEmployersChoferilAmount(company_id, date_period):
    arrayTotal = session.query(
      func.sum(Time.regular_pay + Time.over_pay + Time.vacation_pay + Time.meal_pay + Time.sick_pay + Time.holyday_pay  + Time.commissions + Time.concessions).label('total'),
      Employers.id,
      Employers.first_name,
      Employers.last_name,
      Employers.licence,
      Employers.social_security_number,
      func.count(distinct(Time.period_id)).label('total_weeks'),
      ).select_from(Period).join(Time, Period.id == Time.period_id ).join(Employers, Time.employer_id == Employers.id
      ).filter(
         Employers.choferil == "SI",
        Employers.company_id == company_id,
        Period.period_end >= date_period['start'],
        Period.period_end <= date_period['end']
        
    ).group_by(Employers.id).all()

    return arrayTotal
def roundedAmount(amount, decimal = 2):
    return round(amount, decimal)

def getCompany(company_id):
    company = session.query(Companies).filter(Companies.id == company_id).first()
    account = session.query(Accountant).filter(Companies.id == company.id).first()
    return {
      'company': company,
      'account': account
    }

def getEmployees(company_id):
    employers = session.query(Employers).filter(Employers.company_id == company_id).all()
    return employers



def getEmployer(employer_id):
    employer = session.query(Employers).filter(Employers.id == employer_id).first()
    company = session.query(Companies).filter(Companies.id == employer.company_id).first()
    return {
      'employer': employer,
      'company': company
    }