from models.queries.queryUtils import getCompany, getEmployees, getAmountVariosCompany, addDecimal,roundedAmount, getRandomIrs , getAmountVariosCompanyByMouth
import json
from datetime import datetime


def queryForm943(company_id, year):

    
    # Get company and employees
    data  = getCompany(company_id)
    company = data['company']
    account = data['account']
    employers = getEmployees(company.id)
    

    # get Ein
    ein = company.number_patronal.split('-')
    ein_part_1 = ein[0] if (len(ein) >= 1) else ''
    ein_part_2 = ein[1] if (len(ein) >= 2) else ''

    # Calculate total amount
    amount_varios_number = getAmountVariosCompany(company_id, year)
    amount_varios_number_mouth = getAmountVariosCompanyByMouth(company_id, year)
    monthly_wages = {str(month): 0 for month in range(1, 13)}  # Initialize with zeros
    total_monthly_wages = 0

    for row in amount_varios_number_mouth:  # Populate with actual data
        month = row.month
        monthly_wages[str(month)] = roundedAmount(row.wages * (15.30 /100)) if row.wages is not None else 0
        total_monthly_wages +=   roundedAmount(monthly_wages[str(month)])
    total_monthly_wages = roundedAmount(total_monthly_wages)
    monthly_wages_json = json.dumps(monthly_wages)  # Convert to JSON string
    
      
    

    # Calculate total
    total_wages_no_tips = amount_varios_number.wages + amount_varios_number.commissions + amount_varios_number.concessions+ amount_varios_number.tips
    total_wages_no_tips_number = addDecimal(roundedAmount(total_wages_no_tips))  
    total_wages = amount_varios_number.wages + amount_varios_number.commissions + amount_varios_number.concessions  + amount_varios_number.tips
    salary_security_social = addDecimal(roundedAmount(total_wages))
    tax_medicares = addDecimal(roundedAmount(amount_varios_number.medicares))
    # Calculate * 0.124 + 0.029
    salary_security_social_x_0124_number = roundedAmount(total_wages * 0.124)
    salary_security_social_x_0124 = addDecimal(salary_security_social_x_0124_number)
    tax_medicares_x_0029_number = roundedAmount(total_wages_no_tips * 0.029)
    tax_medicares_x_0029 = addDecimal(tax_medicares_x_0029_number)

    # Calculate total 9
    total_9_number = roundedAmount(salary_security_social_x_0124_number + tax_medicares_x_0029_number)
    total_9 = addDecimal(total_9_number)



    data = {
        ## Page 1
        ## Header fields
        'topmostSubform[0]Page1[0]NameAddress_ReadOrder[0]f1_2[0]': ein_part_1, # identification ein part 1
        'topmostSubform[0]Page1[0]NameAddress_ReadOrder[0]f1_3[0]': ein_part_2, # identification ein part 2
        'topmostSubform[0]Page1[0]NameAddress_ReadOrder[0]f1_1[0]': company.name, # Name company
        'topmostSubform[0]Page1[0]NameAddress_ReadOrder[0]f1_4[0]': '', # Commercial name company
        'topmostSubform[0]Page1[0]NameAddress_ReadOrder[0]f1_5[0]': company.physical_address, # Address company
        'topmostSubform[0]Page1[0]NameAddress_ReadOrder[0]f1_6[0]': f'{company.state_physical_address}, {company.zipcode_physical_address}', # State and ZipCode company
        ## Part 1
        "topmostSubform[0]Page2[0]Table_A-E[0]A[0]Tax[0]f2_25[0]" : str(monthly_wages["1"]),
        "topmostSubform[0]Page2[0]Table_A-E[0]B[0]Tax[0]f2_27[0]" : str(monthly_wages["2"]),
        "topmostSubform[0]Page2[0]Table_A-E[0]C[0]Tax[0]f2_29[0]" : str(monthly_wages["3"]),
        "topmostSubform[0]Page2[0]Table_A-E[0]D[0]Tax[0]f2_31[0]" : str(monthly_wages["4"]),
        "topmostSubform[0]Page2[0]Table_A-E[0]E[0]Tax[0]f2_33[0]" : str(monthly_wages["5"]),
        "topmostSubform[0]Page2[0]Table_F-J[0]F[0]Tax[0]f2_35[0]" : str(monthly_wages["6"]),
        "topmostSubform[0]Page2[0]Table_F-J[0]G[0]Tax[0]f2_37[0]" : str(monthly_wages["7"]),
        "topmostSubform[0]Page2[0]Table_F-J[0]H[0]Tax[0]f2_39[0]" : str(monthly_wages["8"]),
        "topmostSubform[0]Page2[0]Table_F-J[0]I[0]Tax[0]f2_41[0]" : str(monthly_wages["9"]),
        "topmostSubform[0]Page2[0]Table_F-J[0]J[0]Tax[0]f2_43[0]" : str(monthly_wages["10"]),
        "topmostSubform[0]Page2[0]Table_K-M[0]K[0]Tax[0]f2_45[0]" : str(monthly_wages["11"]),

        "topmostSubform[0]Page2[0]Table_K-M[0]L[0]Tax[0]f2_47[0]" : str(monthly_wages["12"]),
        "topmostSubform[0]Page2[0]Table_K-M[0]M[0]Tax[0]f2_49[0]":str(total_monthly_wages),
        "date": datetime.now().strftime("%d-%m-%Y"),
        "date_2": datetime.now().strftime("%d-%m-%Y"),
         ## part 6
    'preparer_first_name': account.name+ ""+ account.first_last_name,
    'authorized_person_phone': account.phone,
    
   
   
    'accountant_ptin': account.identidad_ssa,
    'accountant_ein': account.employer_insurance_number,
    'preparer_phone' :account.phone,
    'preparer_address' : account.address + " " + account.zip_code,
   
    'preparer_name': f'{account.name} {account.first_last_name}',
    'employer_personal_name' : f'{company.contact}' ,
    
    'employer_diurn_number': account.phone,

        'topmostSubform[0]Page1[0]f1_7[0]': str(len(employers)), # Total of employees - Line 1
        'topmostSubform[0]Page1[0]f1_8[0]': salary_security_social[0], # Salary security social part 1 - Line 2
        'topmostSubform[0]Page1[0]f1_9[0]': salary_security_social[1], # Salary security social part 2 - Line 2
        'topmostSubform[0]Page1[0]f1_10[0]': '0', # Qualified sick leave wages part 1 - Line 2a
        'topmostSubform[0]Page1[0]f1_11[0]': '00', # Qualified sick leave wages part 2 - Line 2a
        'topmostSubform[0]Page1[0]f1_12[0]': '0', # Qualified family leave wages part 1 - Line 2b
        'topmostSubform[0]Page1[0]f1_13[0]': '00', # Qualified family leave wages part 2 - Line 2b
        'topmostSubform[0]Page1[0]f1_14[0]': salary_security_social_x_0124[0], # Salary security social * 0.124 part 1 - line 3
        'topmostSubform[0]Page1[0]f1_15[0]': salary_security_social_x_0124[1], # Salary security social * 0.124 part 2 - line 3
        'topmostSubform[0]Page1[0]f1_16[0]': '0', # Qualified sick leave wages * 0.062 part 1 - Line 3a
        'topmostSubform[0]Page1[0]f1_17[0]': '00', # Qualified sick leave wages * 0.062 part 2 - Line 3a
        'topmostSubform[0]Page1[0]f1_18[0]': '0', # Qualified family leave wages * 0.062 part 1 - Line 3b
        'topmostSubform[0]Page1[0]f1_19[0]': '00', # Qualified family leave wages * 0.062 part 2 - Line 3b
        'topmostSubform[0]Page1[0]f1_20[0]': str(total_wages_no_tips_number[0]), # tax medicares part 1 - Line 4
        'topmostSubform[0]Page1[0]f1_21[0]': str(total_wages_no_tips_number[1]), # tax medicares part 2 - Line 4
        'topmostSubform[0]Page1[0]f1_22[0]': tax_medicares_x_0029[0], # tax medicares x 0.029 part 1 - Line 5
        'topmostSubform[0]Page1[0]f1_23[0]': tax_medicares_x_0029[1], # tax medicares x 0.029 part 2 - Line 5
        'topmostSubform[0]Page1[0]f1_24[0]': '0', # tax medicares additional part 1 - Line 6
        'topmostSubform[0]Page1[0]f1_25[0]': '00', # tax medicares additional part 2 - Line 6
        'topmostSubform[0]Page1[0]f1_26[0]': '0', # tax medicares additional x 0.009 part 1 - Line 7
        'topmostSubform[0]Page1[0]f1_27[0]': '00', # tax medicares additional x 0.009 part 2 - Line 7
        'topmostSubform[0]Page1[0]f1_28[0]': '0', # federal income tax withheld part - Line 8
        'topmostSubform[0]Page1[0]f1_29[0]': '00', # federal income tax withheld part - Line 8
        'topmostSubform[0]Page1[0]f1_30[0]': total_9[0], # total taxes before adjustment part 1 - Line 9
        'topmostSubform[0]Page1[0]f1_31[0]': total_9[1], # total taxes before adjustment part 2 - Line 9

    }
    return data
    

