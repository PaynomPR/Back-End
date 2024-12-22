from pathlib import Path
import datetime
from models.queries.queryUtils import roundedAmount,  getEmployer, getAmountVariosByCompany ,getCompany

from database.config import session
from models.queries.queryUtils import getCompany, getEmployees, getAmountVariosByCompany
from utils.country import COUNTRY
from utils.time_func import getPeriodTime , getAgeEmployer

def form_w2psse_txt_generator(company_id, year,resbmited = "1",resbmited_code = ""):
    rute = Path(__file__).parent.absolute()
    document_dir = rute.parent / 'output_files'
    output_file_name = 'form_w2p.txt'

    # Create the full path to the output file
    output_file_path = document_dir / output_file_name

    # Create the output directory if it doesn't exist
    document_dir.mkdir(parents=True, exist_ok=True)  

    # Get company and employees
    data  = getCompany(company_id)
    company = data['company']
    account = data['account']
    
    
  


    # Calculate total amount
    amount_varios_number = getAmountVariosByCompany(company_id,year)
  
   

    # Open the file in write mode and write your desired content
    with open(output_file_path, 'w') as file:
        file.write(RAtxt(account,resbmited,resbmited_code)+"\n")
        file.write(REtxt(year,company)+"\n")

        count = 0
        acum_total_20 = 0
        acum_total_21 = 0
        acum_total_22 = 0
        acum_total_23 = 0
        acum_total_24 = 0

        acum_total_7 = 0
        acum_total_8 = 0
        acum_total_9 = 0
        acum_total_10 = 0
        acum_total_11 = 0
        acum_total_13 = 0
        acum_total_14 = 0
        acum_total_16 = 0
        acum_total_6 = 0
        for data in amount_varios_number:
            
            count = count + 1
            # Date of birth (format: YYYY-MM-DD)
            birthday = str(data.Employers.birthday).split('-') if data.Employers.birthday is not None else '1000-01-01'.split('-')
            age = getAgeEmployer(birthday)
            total_7 = 0
            total_wages = 0
            # Rounding amount to 2 decimal places
            rounded_amount_medicares = roundedAmount(data.medicares if data.medicares is not None else 0)
            rounded_amount_aflac = roundedAmount(data.aflac if data.aflac is not None else 0)
            rounded_amount_commissions = roundedAmount(data.commissions if data.commissions is not None else 0)
            rounded_amount_bonus = roundedAmount(data.bonus if data.bonus is not None else 0)
            rounded_amount_wages = roundedAmount(data.wages if data.wages is not None else 0 ) 
            rounded_amount_wages_26 = roundedAmount(data.wages if data.wages is not None else 0) if age <= 26 else 0.00
            rounded_amount_concessions = roundedAmount(data.concessions if data.concessions is not None else 0)
            rounded_amount_tips = roundedAmount(data.tips if data.tips is not None else 0)
            rounded_amount_donation = roundedAmount(data.donation if data.donation is not None else 0)
            
            total_wages= rounded_amount_wages
            if age <= 26:
                if (rounded_amount_wages> 40000):
                    total_wages = rounded_amount_wages-40000 
                    total_7 = 40000
                else:
                    total_wages = 0
                    total_7=rounded_amount_wages
            
            
            rounded_amount_11 = roundedAmount(rounded_amount_commissions +     total_wages  + rounded_amount_concessions + rounded_amount_tips) 
            rounded_amount_refunds = roundedAmount(data.refunds if data.refunds is not None else 0)
            rounded_amount_secures_social = roundedAmount(data.secure_social if data.secure_social is not None else 0)
            rounded_amount_social_tips = roundedAmount(data.social_tips if data.social_tips is not None else 0)
            rounded_amount_taxes_pr = roundedAmount(data.taxes_pr if data.taxes_pr is not None else 0)

            # Address Company
            physicalAddressCompany = company.physical_address if company.physical_address is not None else ''
            statePhysicalAddressCompany = company.state_physical_address if company.state_physical_address is not None else ''
            countryPhysicalAddressCompany = company.country_physical_address if company.country_physical_address is not None else ''

            n_control = company.w2_first_control
            total_20 = roundedAmount(roundedAmount(total_7)+ roundedAmount(rounded_amount_11)-roundedAmount(rounded_amount_tips))
            print("----------------total_20------------------")
            print(total_20)
            acum_total_20 += roundedAmount(total_20)
            total_21 = roundedAmount(roundedAmount(rounded_amount_secures_social)+roundedAmount(rounded_amount_social_tips))

            acum_total_21 += roundedAmount(total_21)
            total_22 = roundedAmount(roundedAmount(rounded_amount_wages_26)+roundedAmount(rounded_amount_11))

            acum_total_22 += roundedAmount(total_22) 
            total_23 = roundedAmount(rounded_amount_medicares)
            acum_total_23 += roundedAmount(total_23)
            total_24 = roundedAmount(rounded_amount_tips)
            acum_total_24 += roundedAmount(total_24)
            total_16 = total_7
            acum_total_16 += roundedAmount(total_16)
            total_7 = total_wages
            acum_total_7 += roundedAmount(total_7)
            total_8 = roundedAmount(rounded_amount_commissions)
            acum_total_8 += roundedAmount(total_8)
            total_9 = roundedAmount(rounded_amount_concessions)
            acum_total_9 += roundedAmount(total_9)
            total_10 = roundedAmount(rounded_amount_tips)
            acum_total_10 += roundedAmount(total_10)
            total_11 = roundedAmount(rounded_amount_11)
            acum_total_11 += roundedAmount(total_11)
            total_13 = roundedAmount(rounded_amount_taxes_pr)
            acum_total_13 += roundedAmount(total_13)
            total_14 = roundedAmount(rounded_amount_taxes_pr)
            acum_total_14 += roundedAmount(total_14)

            total_6 = roundedAmount(rounded_amount_donation)
            acum_total_6 += roundedAmount(total_6)
            total_19 = roundedAmount(rounded_amount_aflac)
            
            total_12 = roundedAmount(rounded_amount_refunds)
           
            file.write(RWtxt(data.Employers,total_20,total_21,total_22,total_23,total_24)+"\n")
            file.write(ROtxt(data.Employers,total_7,total_8,total_9,total_10,total_11,total_13,total_14)+"\n")
            file.write(RStxt(data.Employers,company,total_6,total_19,total_16,total_12,data.Employers.birthday)+"\n")
        file.write(RTtxt(count,acum_total_20,acum_total_21,acum_total_22,acum_total_23,acum_total_24)+"\n")
        file.write(RUtxt(count,acum_total_7,acum_total_8,acum_total_9,acum_total_10,acum_total_11,acum_total_13,acum_total_14)+"\n")  
        file.write(RVtxt(count,company,acum_total_16,acum_total_6)+"\n")        
        file.write(RFtxt(count)+"\n") 
            

    return output_file_path

def add_to_right(texto, longitud_total,character):
  """Agrega espacios en blanco a la derecha de un texto hasta alcanzar una longitud dada.

  Args:
    texto: El texto original.
    longitud_total: La longitud total deseada, incluyendo los espacios.

  Returns:
    El texto con los espacios agregados a la derecha.
  """

  return texto.ljust(longitud_total).replace(" ",character)
def RAtxt(ac,resbmited,resbmited_code):
    text = ""
    if (resbmited_code == ""):
        resbmited_code = add_to_right(text,6," ")
    if (resbmited > 0):
        resbmited = resbmited-1
    
    return "RA"+ac.employer_insurance_number.replace("-", "")[:9]+ac.identidad_ssa[:8]+add_to_right(text,4," ")+add_to_right(text,5," ")+str(resbmited)+str(resbmited_code)[:6]+"99"+ac.company.ljust(57)+ac.physical_address[:22][:22].ljust(22)+ac.address[:22][:22].ljust(22)+COUNTRY[int(ac.physical_country)][:22].ljust(22)+ac.physical_state+ac.physical_zip_code+add_to_right(text,4," ")+add_to_right(text,5," ")+add_to_right(text,23," ")+add_to_right(text,15," ")+add_to_right(text,2," ")+ac.company.ljust(57)+ac.physical_address[:22].ljust(22)+ac.address[:22].ljust(22)+COUNTRY[int(ac.physical_country)-1][:22].ljust(22)+ac.physical_state+ac.physical_zip_code+add_to_right(text,4," ")+add_to_right(text,5," ")+add_to_right(text,23," ")+add_to_right(text,15," ")+add_to_right(text,2," ")+(ac.name+" "+ac.first_last_name).ljust(27)+ac.phone.replace("-","").ljust(15)+add_to_right(text,5," ")+add_to_right(text,3," ")+ac.email.ljust(40)+add_to_right(text,3," ")+add_to_right(text,10," ")+add_to_right(text,1," ")+"A"+add_to_right(text,12," ")


def REtxt(year,company):
    text = ""
    payer = " "
    if (company.payer == "1"):
        payer = "R"
    if (company.payer == "2"):
        payer = "A"
    if (company.payer == "3"):
        payer = "F"
    if (company.payer == "4"):
        payer = "H"
    return "RE"+str(year)+add_to_right(text,1," ")+company.number_patronal.replace("-","")[:9].ljust(9)+add_to_right(text,9," ")+"0"+add_to_right(text,4," ")+add_to_right(text,9," ")+company.name.replace("&","y").ljust(57)+company.physical_address[:22].ljust(22)+company.postal_address[:22].ljust(22)+COUNTRY[int(company.country_physical_address)-1][:22].ljust(22)+company.state_physical_address.ljust(2)+company.zipcode_physical_address.ljust(5)+add_to_right(text,4," ")+add_to_right(text,5," ")+add_to_right(text,23," ")+add_to_right(text,15," ")+add_to_right(text,2," ")+payer+"P"+"0"+company.contact.ljust(27)+company.contact_number.replace("-","").ljust(15)+add_to_right(text,5," ")+add_to_right(text,10," ")+company.email.ljust(40)+add_to_right(text,194," ")

def RWtxt(employer,total_20,total_21,total_22,total_23,total_24):
    total_20 = round(total_20 * 100)
    total_20 = f"{total_20:011d}"
    total_21 = round(total_21 * 100)
    total_21 = f"{total_21:011d}"
    total_22 = round(total_22 * 100)
    total_22 = f"{total_22:011d}"
    total_23 = round(total_23 * 100)
    total_23 = f"{total_23:011d}"
    total_24 = round(total_24 * 100)
    total_24 = f"{total_24:011d}"
    

    text = ""    
    return "RW"+employer.social_security_number.replace("-","")[:9]+employer.first_name.ljust(15)+employer.middle_name.ljust(15)+(employer.last_name+" "+employer.mother_last_name).ljust(20)+add_to_right(text,4," ")+employer.address[:22].ljust(22)+employer.address[:22].ljust(22)+COUNTRY[int(employer.address_country)-1][:22].ljust(22)+employer.address_state.ljust(2)+employer.address_number.ljust(5)+add_to_right(text,4," ")+add_to_right(text,5," ")+add_to_right(text,23," ")+add_to_right(text,15," ")+add_to_right(text,2," ")+add_to_right(text,22,"0")+total_20+total_21+total_22+total_23+total_24+add_to_right(text,11," ")+add_to_right(text,66,"0")+add_to_right(text,11," ")+add_to_right(text,44,"0")+add_to_right(text,11," ")+add_to_right(text,77,"0")+add_to_right(text,1," ")+"0"+add_to_right(text,1," ")+"00"+add_to_right(text,23," ")

def ROtxt(employer,total_7,total_8,total_9,total_10,total_11,total_13,total_14):
    total_7 = round(total_7 * 100)
    total_7 = f"{total_7:011d}"    
    total_8 = round(total_8 * 100)
    total_8 = f"{total_8:011d}" 
    total_9 = round(total_9 * 100)
    total_9 = f"{total_9:011d}"
    total_10 = round(total_10 * 100)
    total_10 = f"{total_10:011d}" 
    total_11 = round(total_11 * 100)
    total_11 = f"{total_11:011d}"  
    total_13 = round(total_13 * 100)
    total_13 = f"{total_13:011d}" 
    
    text = ""    
    return "RO"+add_to_right(text,9," ")+add_to_right(text,11,"0")+add_to_right(text,11,"0")+add_to_right(text,66,"0")+add_to_right(text,11," ")+add_to_right(text,44,"0")+add_to_right(text,120," ")+total_7+total_8+total_9+total_10+total_11+total_13+add_to_right(text,11,"0")+add_to_right(text,11," ")+add_to_right(text,22,"0")+add_to_right(text,128," ")

def RStxt(employer,company,total_6,total_19,total_16,total_12,birthday):
    total_6 = round(total_6 * 100)
    total_6 = f"{total_6:011d}" 
    total_19 = round(total_19 * 100)
    total_19 = f"{total_19:011d}" 
    total_12 = round(total_12 * 100)
    total_12 = f"{total_12:011d}" 
    text = ""  
    code = "  "
    if (total_16 > 0):
        code = "E"
    total_16 = round(total_16 * 100)
    total_16 = f"{total_16:011d}" 
      
    return "RS"+add_to_right(text,2,"0")+add_to_right(text,5,"0")+employer.social_security_number.replace("-","")[:9]+employer.first_name.ljust(15)+employer.middle_name.ljust(15)+(employer.last_name+" "+employer.mother_last_name).ljust(20)+add_to_right(text,4," ")+employer.address[:22].ljust(22)+employer.address[:22].ljust(22)+COUNTRY[int(employer.address_country)-1][:22].ljust(22)+employer.address_state.ljust(2)+employer.address_number.ljust(5)+add_to_right(text,9," ")+add_to_right(text,23," ")+add_to_right(text,15," ")+add_to_right(text,2," ")+add_to_right(text,2," ")+add_to_right(text,6,"0")+add_to_right(text,40,"0")+add_to_right(text,5," ")+add_to_right(text,20,"0")+add_to_right(text,6," ")+add_to_right(text,64,"0")+add_to_right(text,75," ")+add_to_right(text,75," ")+add_to_right(text,25," ")

def RTtxt(count,acum_total_20,acum_total_21,acum_total_22,acum_total_23,acum_total_24):
    text = ""  
    count = f"{count:07d}" 
    acum_total_20 = round(acum_total_20 * 100)
    acum_total_20 = f"{acum_total_20:015d}"

    acum_total_21 = round(acum_total_21 * 100)
    acum_total_21 = f"{acum_total_21:015d}"

    acum_total_22 = round(acum_total_22 * 100)
    acum_total_22 = f"{acum_total_22:015d}"

    acum_total_23 = round(acum_total_23 * 100)
    acum_total_23 = f"{acum_total_23:015d}"

    acum_total_24 = round(acum_total_24 * 100)
    acum_total_24 = f"{acum_total_24:015d}"
      
    print("----------------acum_total_20------------------")
    print(acum_total_20)
    return "RT"+count+add_to_right(text,30,"0")+acum_total_20+acum_total_21+acum_total_22+acum_total_23+acum_total_24+add_to_right(text,15," ")+add_to_right(text,15,"0")+add_to_right(text,75,"0")+add_to_right(text,15," ")+add_to_right(text,180,"0")+add_to_right(text,98," ")

def RUtxt(count,acum_total_7,acum_total_8,acum_total_9,acum_total_10,acum_total_11,acum_total_13,acum_total_14):
    text = ""  
    count = f"{count:07d}" 
    acum_total_7 = round(acum_total_7 * 100)
    acum_total_7 = f"{acum_total_7:015d}"
    acum_total_8 = round(acum_total_8 * 100)
    acum_total_8 = f"{acum_total_8:015d}"
    acum_total_9 = round(acum_total_9 * 100)
    acum_total_9 = f"{acum_total_9:015d}"
    acum_total_10 = round(acum_total_10 * 100)
    acum_total_10 = f"{acum_total_10:015d}"
    acum_total_11 = round(acum_total_11 * 100)
    acum_total_11 = f"{acum_total_11:015d}"
    acum_total_13 = round(acum_total_13 * 100)
    acum_total_13 = f"{acum_total_13:015d}"
    acum_total_14 = round(acum_total_14 * 100)
    acum_total_14 = f"{acum_total_14:015d}"
      
    return "RU"+count+add_to_right(text,15,"0")+add_to_right(text,15,"0")+add_to_right(text,90,"0")+add_to_right(text,15," ")+add_to_right(text,60,"0")+add_to_right(text,150," ")+acum_total_7+acum_total_8+acum_total_9+acum_total_10+acum_total_11+acum_total_13+add_to_right(text,45,"0")+add_to_right(text,23," ")


def RVtxt(count,company,acum_total_16,acum_total_6):
    text = ""  
    count = f"{count:07d}" 
    acum_total_16 = round(acum_total_16 * 100)
    acum_total_16 = f"{acum_total_16:015d}"

    acum_total_6 = round(acum_total_6 * 100)
    acum_total_6 = f"{acum_total_6:015d}"
      
    return "RV"+add_to_right(text,510," ")

def RFtxt(count):
    text = ""  
    count = f"{count:09d}" 
    
      
    return "RF"+add_to_right(text,5," ")+count+add_to_right(text,496," ")