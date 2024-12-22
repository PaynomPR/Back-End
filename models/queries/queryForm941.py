from models.queries.queryUtils import getCompany, getEmployees,getAmountByMonth, getAmountVariosCompany, addDecimal,roundedAmount, getRandomIrs
from utils.country import COUNTRY
from utils.time_func import getPeriodTime
def queryForm941(company_id, year, period):


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
    month = date_start.month
    

    # Calculate total amount
    amount_varios_number = getAmountVariosCompany(company_id, year, period)
    amount_by_month_1 =  getAmountByMonth(company_id, year,month)[0]
    amount_by_month_2 =  getAmountByMonth(company_id, year,month+1)[0]
    amount_by_month_3 =  getAmountByMonth(company_id, year,month+2)[0]

    amount_by_month_1_number = roundedAmount(amount_by_month_1.social_tips + amount_by_month_1.secure_social + amount_by_month_1.medicares)*2
    amount_by_month_1_decimal = addDecimal(amount_by_month_1_number)

    amount_by_month_2_number = roundedAmount(amount_by_month_2.social_tips + amount_by_month_2.secure_social+ amount_by_month_2.medicares)*2
    amount_by_month_2_decimal = addDecimal(amount_by_month_2_number)

    amount_by_month_3_number = roundedAmount(amount_by_month_3.social_tips + amount_by_month_3.secure_social+ amount_by_month_3.medicares)*2
    amount_by_month_3_decimal = addDecimal(amount_by_month_3_number)

    amount_by_month_total_number = amount_by_month_1_number +amount_by_month_2_number  +amount_by_month_3_number
    amount_by_month_total_decimal = addDecimal(amount_by_month_total_number)

    # Calculate column 1
    total_wages = amount_varios_number.wages + amount_varios_number.commissions + amount_varios_number.concessions 
    salary_security_social = addDecimal(roundedAmount(total_wages))
    tips_security_social = addDecimal(roundedAmount(amount_varios_number.tips))
    salary_tips_security_social = addDecimal(roundedAmount(total_wages + amount_varios_number.tips))
    # Calculate column 2
    salary_security_social_x_0124_number = roundedAmount(total_wages * 0.124)
    salary_security_social_x_0124 = addDecimal(salary_security_social_x_0124_number)
    tips_security_social_x_0124_number = roundedAmount(amount_varios_number.tips * 0.124)
    tips_security_social_x_0124 = addDecimal(tips_security_social_x_0124_number)
    salary_tips_security_social_x_0029_number = roundedAmount((total_wages + amount_varios_number.tips) * 0.029)
    salary_tips_security_social_x_0029 = addDecimal((salary_tips_security_social_x_0029_number))
    # Calculate total Line 5e
    total_5e_number = roundedAmount(salary_security_social_x_0124_number + tips_security_social_x_0124_number + salary_tips_security_social_x_0029_number)
    total_5e = addDecimal(total_5e_number)
    # Calculate total Line 6
    total_6_number = roundedAmount(total_5e_number + 0)
    total_6 = addDecimal(total_6_number)
    # Calculate total Line 10
    total_10_number = roundedAmount(total_6_number + 0)
    total_10 = addDecimal(total_10_number)

    # Personal number id
    personal_number_id = getRandomIrs()


    data = {
        ## Page 1
        ## Header fields
        f'topmostSubform[0]Page1[0]c1_1[{period-1}]': True,
        'topmostSubform[0]Page3[0]f3_32[0]':account.company,            
        'topmostSubform[0]Page1[0]EntityArea[0]f1_1[0]': ein_part_1[0], # identification ein part 1
        'topmostSubform[0]Page1[0]EntityArea[0]f1_1[0]1': ein_part_1[1], # identification ein part 1

        'topmostSubform[0]Page1[0]EntityArea[0]f1_2[0]': ein_part_2[0], # identification ein part 2
        'topmostSubform[0]Page1[0]EntityArea[0]f1_2[0]1': ein_part_2[1], # identification ein part 2
        'topmostSubform[0]Page1[0]EntityArea[0]f1_2[0]2': ein_part_2[2], # identification ein part 2
        'topmostSubform[0]Page1[0]EntityArea[0]f1_2[0]3': ein_part_2[3], # identification ein part 2
        'topmostSubform[0]Page1[0]EntityArea[0]f1_2[0]4': ein_part_2[4], # identification ein part 2
        'topmostSubform[0]Page1[0]EntityArea[0]f1_2[0]5': ein_part_2[5], # identification ein part 2
        'topmostSubform[0]Page1[0]EntityArea[0]f1_2[0]6': ein_part_2[6], # identification ein part 2


        
        'topmostSubform[0]Page1[0]EntityArea[0]f1_3[0]': company.name, # Name company
        'topmostSubform[0]Page1[0]EntityArea[0]f1_4[0]': '', # Commercial name company
        'topmostSubform[0]Page1[0]EntityArea[0]f1_5[0]': company.postal_address, # Address company
        'topmostSubform[0]Page1[0]EntityArea[0]f1_6[0]':  COUNTRY[int(company.country_postal_address)-1],
        'topmostSubform[0]Page1[0]EntityArea[0]f1_7[0]': company.state_postal_addess, # State company
        'topmostSubform[0]Page1[0]EntityArea[0]f1_8[0]': company.zipcode_postal_address, # ZipCode company
        'topmostSubform[0]Page1[0]EntityArea[0]f1_9[0]': '', # Name country foreign
        'topmostSubform[0]Page1[0]EntityArea[0]f1_10[0]': '', # Provincia foreign
        'topmostSubform[0]Page1[0]EntityArea[0]f1_11[0]': '', # Zip code foreign
        ## Part 1
        'topmostSubform[0]Page1[0]f1_12[0]': str(len(employers)), # Total of employees
        ### Column 1
        'topmostSubform[0]Page1[0]f1_13[0]': salary_security_social[0], # Salary security social part 1 - Line 5a
        'topmostSubform[0]Page1[0]f1_14[0]': salary_security_social[1], # Salary security social part 2 - Line 5a
        'topmostSubform[0]Page1[0]f1_17[0]': '0', # Qualified sick leave wages part 1 - Line 5a (I)
        'topmostSubform[0]Page1[0]f1_18[0]': '00', # Qualified sick leave wages part 2 - Line 5a (I)
        'topmostSubform[0]Page1[0]f1_21[0]': '0', # Qualified family leave wages part 1 - Line 5a (II)
        'topmostSubform[0]Page1[0]f1_22[0]': '00', # Qualified family leave wages part 2 - Line 5a (II)
        'topmostSubform[0]Page1[0]f1_25[0]': tips_security_social[0], # Tips subject to social security tax part 1 - Line 5b
        'topmostSubform[0]Page1[0]f1_26[0]': tips_security_social[1], # Tips subject to social security tax part 2 - Line 5b
        'topmostSubform[0]Page1[0]f1_29[0]': salary_tips_security_social[0], # Wages and tips subject to medicare tax part 1 - line 5c
        'topmostSubform[0]Page1[0]f1_30[0]': salary_tips_security_social[1], # Wages and tips subject to medicare tax part 2 - line 5c
        'topmostSubform[0]Page1[0]f1_33[0]': '0', # Wages and tips subject to additional medicare tax withholding part 1 - line 5d
        'topmostSubform[0]Page1[0]f1_34[0]': '00', # Wages and tips subject to additional medicare tax withholding part 2 - line 5d
        ### Column 2
        'topmostSubform[0]Page1[0]f1_15[0]': salary_security_social_x_0124[0], # Salary security social * 0.124 part 1
        'topmostSubform[0]Page1[0]f1_16[0]': salary_security_social_x_0124[1], # Salary security social * 0.124 part 2
        'topmostSubform[0]Page1[0]f1_19[0]': '0', # Qualified sick leave wages * 0.062 part 1 - Line 5a (I)
        'topmostSubform[0]Page1[0]f1_20[0]': '00', # Qualified sick leave wages * 0.062 part 2 - Line 5a (I)
        'topmostSubform[0]Page1[0]f1_23[0]': '0', # Qualified family leave wages * 0.062 part 1 - Line 5a (II)
        'topmostSubform[0]Page1[0]f1_24[0]': '00', # Qualified family leave wages * 0.062 part 2 - Line 5a (II)
        'topmostSubform[0]Page1[0]f1_27[0]': tips_security_social_x_0124[0], # Tips subject to social security tax * 0.124 part 1 - Line 5b
        'topmostSubform[0]Page1[0]f1_28[0]': tips_security_social_x_0124[1], # Tips subject to social security tax * 0.124 part 2 - Line 5b
        'topmostSubform[0]Page1[0]f1_31[0]': salary_tips_security_social_x_0029[0], # Wages and tips subject to medicare tax * 0.029 part 1 - Line 5c
        'topmostSubform[0]Page1[0]f1_32[0]': salary_tips_security_social_x_0029[1], # Wages and tips subject to medicare tax * 0.029 part 2 - Line 5c
        'topmostSubform[0]Page1[0]f1_35[0]': '0', # Wages and tips subject to additional medicare tax withholding * 0.009 part 1 - Line 5d
        'topmostSubform[0]Page1[0]f1_36[0]': '00', # Wages and tips subject to additional medicare tax withholding * 0.009 part 2 - Line 5d
        ### Continue Part 1
        'topmostSubform[0]Page1[0]f1_37[0]': total_5e[0], # comment part 1 - Line 5e
        'topmostSubform[0]Page1[0]f1_38[0]': total_5e[1], # comment part 2 - Line 5e
        'topmostSubform[0]Page1[0]f1_39[0]': '0', # comment part 1 - Line 5f
        'topmostSubform[0]Page1[0]f1_40[0]': '00', # comment part 2 - Line 5f
        'topmostSubform[0]Page1[0]f1_41[0]': total_6[0], # comment part 1 - Line 6
        'topmostSubform[0]Page1[0]f1_42[0]': total_6[1], # comment part 2 - Line 6
        'topmostSubform[0]Page1[0]f1_43[0]': '0', # comment part 1 - Line 7
        'topmostSubform[0]Page1[0]f1_44[0]': '00', # comment part 2 - Line 7
        'topmostSubform[0]Page1[0]f1_45[0]': '0', # comment part 1 - Line 8
        'topmostSubform[0]Page1[0]f1_46[0]': '00', # comment part 2 - Line 8
        'topmostSubform[0]Page1[0]f1_47[0]': '0', # comment part 1 - Line 9
        'topmostSubform[0]Page1[0]f1_48[0]': '00', # comment part 2 - Line 9
        'topmostSubform[0]Page1[0]f1_49[0]': total_10[0], # comment part 1 - Line 10
        'topmostSubform[0]Page1[0]f1_50[0]': total_10[1], # comment part 2 - Line 10
        'topmostSubform[0]Page1[0]f1_51[0]': '0', # comment part 1 - Line 11a
        'topmostSubform[0]Page1[0]f1_52[0]': '00', # comment part 2 - Line 11a
        'topmostSubform[0]Page1[0]f1_53[0]': '0', # comment part 1 - Line 11b
        'topmostSubform[0]Page1[0]f1_54[0]': '00', # comment part 2 - Line 11b
        'topmostSubform[0]Page1[0]f1_55[0]': '0', # comment part 1 - Line 11c
        'topmostSubform[0]Page1[0]f1_56[0]': '00', # comment part 2 - Line 11c
        ## Page 2
        ### Part 1
        'topmostSubform[0]Page2[0]Name_ReadOrder[0]f1_3[0]': company.name, # name company
        'topmostSubform[0]Page2[0]EIN_Number[0]f1_1[0]': ein_part_1, # identification ein part 1
        'topmostSubform[0]Page2[0]EIN_Number[0]f1_2[0]': ein_part_2, # identification ein part 2
        'topmostSubform[0]Page2[0]f2_3[0]': '0', # part 1 - Line 11d
        'topmostSubform[0]Page2[0]f2_4[0]': '00', # part 2 - Line 11d
        'topmostSubform[0]Page2[0]f2_5[0]': '0', # part 1 - Line 11e
        'topmostSubform[0]Page2[0]f2_6[0]': '00', # part 2 - Line 11e
        'topmostSubform[0]Page2[0]f2_7[0]': '0.00', # part complete - Line 11f
        'topmostSubform[0]Page2[0]f2_8[0]': '0', # part 1 - Line 11g
        'topmostSubform[0]Page2[0]f2_9[0]': '00', # part 2 - Line 11g
        'topmostSubform[0]Page2[0]f2_10[0]': '0', # part 1 - Line 12
        'topmostSubform[0]Page2[0]f2_11[0]': '00', # part 2 - Line 12
        'topmostSubform[0]Page2[0]f2_12[0]': '0', # part 1 - Line 13a
        'topmostSubform[0]Page2[0]f2_13[0]': '00', # part 2 - Line 13a
        'topmostSubform[0]Page2[0]f2_14[0]': '0', # part 1 - Line 13b
        'topmostSubform[0]Page2[0]f2_15[0]': '00', # part 2 - Line 13b
        'topmostSubform[0]Page2[0]f2_16[0]': '0', # part 1 - Line 13c
        'topmostSubform[0]Page2[0]f2_17[0]': '00', # part 2 - Line 13c
        'topmostSubform[0]Page2[0]f2_18[0]': '0', # part 1 - Line 13d
        'topmostSubform[0]Page2[0]f2_19[0]': '00', # part 2 - Line 13d
        'topmostSubform[0]Page2[0]f2_20[0]': '0', # part 1 - Line 13e
        'topmostSubform[0]Page2[0]f2_21[0]': '00', # part 2 - Line 13e
        'topmostSubform[0]Page2[0]f2_22[0]': '0', # part 1 - Line 13f
        'topmostSubform[0]Page2[0]f2_23[0]': '00', # part 2 - Line 13f
        'topmostSubform[0]Page2[0]f2_24[0]': '0', # part 1 - Line 13g
        'topmostSubform[0]Page2[0]f2_25[0]': '00', # part 2 - Line 13g
        'topmostSubform[0]Page2[0]f2_26[0]': '0', # part 1 - Line 13h
        'topmostSubform[0]Page2[0]f2_27[0]': '00', # part 2 - Line 13h
        'topmostSubform[0]Page2[0]f2_28[0]': '0', # part 1 - Line 13i
        'topmostSubform[0]Page2[0]f2_29[0]': '00', # part 2 - Line 13i
        'topmostSubform[0]Page2[0]f2_30[0]': '0', # part 1 - Line 14
        'topmostSubform[0]Page2[0]f2_31[0]': '00', # part 2 - Line 14
        'topmostSubform[0]Page2[0]f2_32[0]': '0', # part 1 - Line 15
        'topmostSubform[0]Page2[0]f2_33[0]': '00', # part 2 - Line 15
        ### Part 2
        'topmostSubform[0]Page2[0]f2_34[0]': str(amount_by_month_1_decimal[0]), # mes 1 part 1 - Line 16
        'topmostSubform[0]Page2[0]f2_35[0]': str(amount_by_month_1_decimal[1]), # mes 1 part 2 - Line 16
        'topmostSubform[0]Page2[0]f2_36[0]': str(amount_by_month_2_decimal[0]), # mes 2 part 1 - Line 16
        'topmostSubform[0]Page2[0]f2_37[0]': str(amount_by_month_2_decimal[1]), # mes 2 part 2 - Line 16
        'topmostSubform[0]Page2[0]f2_38[0]': str(amount_by_month_3_decimal[0]), # mes 3 part 1 - Line 16
        'topmostSubform[0]Page2[0]f2_39[0]': str(amount_by_month_3_decimal[1]), # mes 3 part 2 - Line 16
        'topmostSubform[0]Page2[0]f2_40[0]': str(amount_by_month_total_decimal[0]), # total mes part 1 - Line 16
        'topmostSubform[0]Page2[0]f2_41[0]': str(amount_by_month_total_decimal[1]), # total mes part 2 - Line 16
       
        ### Part 3
        'topmostSubform[0]Page3[0]Name_ReadOrder[0]f1_3[0]': company.name, # name company
        'topmostSubform[0]Page3[0]EIN_Number[0]f1_1[0]': ein_part_1, # identification ein part 1
        'topmostSubform[0]Page3[0]EIN_Number[0]f1_2[0]': ein_part_2, # identification ein part 2
        'topmostSubform[0]Page3[0]Ciudad_ReadOrder[0]f3_36[0]': COUNTRY[int(account.country)-1],
   
    'topmostSubform[0]Page3[0]f3_31[0]': account.identidad_ssa,
    'topmostSubform[0]Page3[0]f3_33[0]': account.employer_insurance_number,
  
    'accountant_addres' : account.address,
   
    'accountant_personal_name': f'{account.name} {account.first_last_name}',
        'topmostSubform[0]Page3[0]f3_3[0]': '01012024', # date - Line 17
        'topmostSubform[0]Page3[0]f3_4[0]': '0', # part 1 - Line 19
        'topmostSubform[0]Page3[0]f3_5[0]': '00', # part 2 - Line 19
        'topmostSubform[0]Page3[0]f3_6[0]': '0', # part 1 - Line 20
        'topmostSubform[0]Page3[0]f3_7[0]': '00', # part 2 - Line 20
        'topmostSubform[0]Page3[0]f3_8[0]': '0', # part 1 - Line 21
        'topmostSubform[0]Page3[0]f3_9[0]': '00', # part 2 - Line 21
        'topmostSubform[0]Page3[0]f3_10[0]': '0', # part 1 - Line 22
        'topmostSubform[0]Page3[0]f3_11[0]': '00', # part 2 - Line 22
        'topmostSubform[0]Page3[0]f3_12[0]': '0', # part 1 - Line 23
        'topmostSubform[0]Page3[0]f3_13[0]': '00', # part 2 - Line 23
        'topmostSubform[0]Page3[0]f3_14[0]': '0', # part 1 - Line 24
        'topmostSubform[0]Page3[0]f3_15[0]': '00', # part 2 - Line 24
        'topmostSubform[0]Page3[0]f3_16[0]': '0', # part 1 - Line 25
        'topmostSubform[0]Page3[0]f3_17[0]': '00', # part 2 - Line 25
        'topmostSubform[0]Page3[0]f3_18[0]': '0', # part 1 - Line 26
        'topmostSubform[0]Page3[0]f3_19[0]': '00', # part 2 - Line 26
        'topmostSubform[0]Page3[0]f3_20[0]': '0', # part 1 - Line 27
        'topmostSubform[0]Page3[0]f3_21[0]': '00', # part 2 - Line 27
        'topmostSubform[0]Page3[0]f3_22[0]': '0', # part 1 - Line 28
        'topmostSubform[0]Page3[0]f3_23[0]': '00', # part 2 - Line 28
        ### Part 4
        'topmostSubform[0]Page3[0]f3_27[0]' : company.contact,
        'topmostSubform[0]Page3[0]f3_28[0]': "Gerente",
        'topmostSubform[0]Page3[0]f3_24[0]': account.name + " "+ account.first_last_name, # name personal
        'topmostSubform[0]Page3[0]f3_25[0]':  account.phone, # phone personal
        'topmostSubform[0]Page3[0]f3_26[0]': personal_number_id, # pin irs
        'topmostSubform[0]Page3[0]f3_30[0]' : account.name + " "+ account.first_last_name,
        'topmostSubform[0]Page3[0]Direccion_ReadOrder[0]f3_34[0]' : account.address,
        'topmostSubform[0]Page3[0]Ciudad_ReadOrder[0]f3_36[0]' : COUNTRY[int(account.country)-1],
        'topmostSubform[0]Page3[0]f3_38[0]' :  account.zip_code,
        'topmostSubform[0]Page3[0]f3_35[0]' :  account.phone,
        'topmostSubform[0]Page3[0]Ciudad_ReadOrder[0]f3_37[0]' : account.state,


    }
    return data


