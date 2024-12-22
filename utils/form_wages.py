from pathlib import Path
import datetime

from database.config import session
from models.queries.queryUtils import getCompany, getEmployees, getAmountGroupEmployerWages, addDecimal,roundedAmount, getRandomIrs
from utils.country import COUNTRY
from utils.time_func import getPeriodTime

def form_wages_txt_generator(company_id, year,period):
    rute = Path(__file__).parent.absolute()
    document_dir = rute.parent / 'output_files'
    output_file_name = 'form_wages.txt'

    # Create the full path to the output file
    output_file_path = document_dir / output_file_name

    # Create the output directory if it doesn't exist
    document_dir.mkdir(parents=True, exist_ok=True)  


    # Get company and employees
    data  = getCompany(company_id)
    company = data['company']
    account = data['account']
    employers = getEmployees(company.id)

    # get Ein
    ein = company.number_patronal.split('-')
    ein_part_1 = ein[0] if (len(ein) >= 1) else ''
    ein_part_2 = ein[1] if (len(ein) >= 2) else ''

    date_period = getPeriodTime(period, year)
    date_start = date_period['start']
    date_end = date_period['end']


    # Calculate total amount
    amount_varios_number = getAmountGroupEmployerWages(company_id, date_start, date_end)
  
    now = datetime.datetime.now()

    today = datetime.date.today().strftime("%y%m%d").zfill(6)
    year = datetime.date.today().year
    last_two_digits = year % 100
    formato_hora = now.strftime("%H:%M:%S")

    # Open the file in write mode and write your desired content
    with open(output_file_path, 'w') as file:
        for data in amount_varios_number:
            
            try:
                # Redondear a dos decimales y multiplicar por 100 para convertir a entero
                salario_redondeado = int(data.wages * 100)
                
                # Limitar el valor máximo a 999999999 (equivalente a 9999999.99)
                salario_redondeado = min(salario_redondeado, 9999999)

                # Formatear como cadena con relleno de ceros a la izquierda
                salario_formateado = f"{salario_redondeado:07d}"
                if data.Employers.type == 1:
                    employer_type = "N"
                else:
                    employer_type = "S"
                if (data.Employers.middle_name != ""):
                    employer_initial = data.Employers.middle_name[0]
                else: 
                    employer_initial = " "
                file.write(data.Employers.social_security_number.replace("-", "")+" W4"+data.Employers.last_name[:4]+"12345678$WCA"+today+formato_hora.replace(":", "")+str(last_two_digits)+str(period)+"2"+salario_formateado+company.desem.replace("-", "")[:9]+"    "+"00000000"+"  "+"1000000"+today+"00000004"+data.Employers.first_name.ljust(16)+employer_initial+data.Employers.last_name.upper().ljust(16)+data.Employers.mother_last_name.upper().ljust(16)+employer_type+"     \n")
            except Exception as e:
                print(f"Error processing data for {data.Employers.social_security_number}: {str(e)}")
                # Consider logging the error for further analysis

    return output_file_path