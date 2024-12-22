from pathlib import Path
import fitz  # PyMuPDF
from models.companies import Companies
from database.config import session
from models.queries.queryForm940 import queryForm940



def form_940_pdf_generator(company_id, year):
    
    rute = Path(__file__).parent.absolute()
    document_dir = rute.parent / 'output_files'
    source_file_name = 'template/f940sp.pdf'
    output_file_name = 'complete.pdf'

    data_entry_data = queryForm940(company_id, year)

    with fitz.open(document_dir / source_file_name) as doc:
        for page_number in range(len(doc)):
            page = doc[page_number]
            for field in page.widgets():
                if field.field_type == fitz.PDF_WIDGET_TYPE_TEXT:
                    if field.field_name == 'topmostSubform[0]Page1[0]EntityArea[0]f1_1[0]':
                        field.field_value = data_entry_data['ein_first_part']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]EntityArea[0]f1_2[0]':
                        field.field_value = data_entry_data['ein_second_part']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]EntityArea[0]f1_3[0]':
                        field.field_value = data_entry_data['legal_name']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]EntityArea[0]f1_4[0]':
                        field.field_value = data_entry_data['comercial_name']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]EntityArea[0]f1_5[0]':
                        field.field_value = data_entry_data['address']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]EntityArea[0]f1_6[0]':
                        field.field_value = data_entry_data['city']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]EntityArea[0]f1_7[0]':
                        field.field_value = data_entry_data['state']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]EntityArea[0]f1_8[0]':
                        field.field_value = data_entry_data['zip']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]EntityArea[0]f1_9[0]':
                        field.field_value = data_entry_data['foering_country_name']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]EntityArea[0]f1_10[0]':
                        field.field_value = data_entry_data['province_name']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]EntityArea[0]f1_11[0]':
                        field.field_value = data_entry_data['postal_code']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]f1_12[0]':
                        field.field_value = data_entry_data['abreviation_state_1']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]f1_13[0]':
                        field.field_value = data_entry_data['abreviation_state_2']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]f1_14[0]':
                        field.field_value = data_entry_data['total_payments_for_all_employees_1']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]f1_15[0]':
                        field.field_value = data_entry_data['total_payments_for_all_employees_2']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]f1_16[0]':
                        field.field_value = data_entry_data['Futa_tax_1']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]f1_17[0]':
                        field.field_value = data_entry_data['Futa_tax_2']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]f1_18[0]':
                        field.field_value = data_entry_data['payments_exceeded_7000_1']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]f1_19[0]':
                        field.field_value = data_entry_data['payments_exceeded_7000_2']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]f1_20[0]':
                        field.field_value = data_entry_data['total_payments_1']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]f1_21[0]':
                        field.field_value = data_entry_data['total_payments_2']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]f1_22[0]':
                        field.field_value = data_entry_data['total_futa_salary_1']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]f1_23[0]':
                        field.field_value = data_entry_data['total_futa_salary_2']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]f1_24[0]':
                        field.field_value = data_entry_data['futa_tax_before_adjustment_1']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]f1_25[0]':
                        field.field_value = data_entry_data['futa_tax_before_adjustment_2']
                        field.update()
                    ## part 3
                    elif field.field_name == 'topmostSubform[0]Page1[0]f1_26[0]':
                        field.field_value = data_entry_data['futa_field_9_1']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]f1_27[0]':
                        field.field_value = data_entry_data['futa_field_9_2']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]f1_28[0]':
                        field.field_value = data_entry_data['futa_field_10_1']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]f1_29[0]':
                        field.field_value = data_entry_data['futa_field_10_2']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]f1_30[0]':
                        field.field_value = data_entry_data['futa_field_11_1']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]f1_31[0]':
                        field.field_value = data_entry_data['futa_field_11_2']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]f1_32[0]':
                        field.field_value = data_entry_data['total_futa_after_adjustment_1']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]f1_33[0]':
                        field.field_value = data_entry_data['total_futa_after_adjustment_2']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]f1_34[0]':
                        field.field_value = data_entry_data['futa_deposit_per_year_1']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]f1_35[0]':
                        field.field_value = data_entry_data['futa_deposit_per_year_2']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]f1_36[0]':
                        field.field_value = data_entry_data['futa_due_balance_1']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]f1_37[0]':
                        field.field_value = data_entry_data['futa_due_balance_1']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]f1_38[0]':
                        field.field_value = data_entry_data['futa_ovepayments_1']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page1[0]f1_39[0]':
                        field.field_value = data_entry_data['futa_ovepayments_2']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page2[0]NameReadOrder[0]f1_3[0]':
                        field.field_value = data_entry_data['legal_name']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page2[0]EIN_Number[0]f1_1[0]':
                        field.field_value = data_entry_data['ein_first_part']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page2[0]EIN_Number[0]f1_2[0]':
                        field.field_value = data_entry_data['ein_second_part']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page2[0]f2_1[0]':
                        field.field_value = data_entry_data['futa_trimest_1_1']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page2[0]f2_2[0]':
                        field.field_value = data_entry_data['futa_trimest_1_2']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page2[0]f2_3[0]':
                        field.field_value = data_entry_data['futa_trimest_2_1']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page2[0]f2_4[0]':
                        field.field_value = data_entry_data['futa_trimest_2_2']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page2[0]f2_5[0]':
                        field.field_value = data_entry_data['futa_trimest_3_1']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page2[0]f2_6[0]':
                        field.field_value = data_entry_data['futa_trimest_3_2']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page2[0]f2_7[0]':
                        field.field_value = data_entry_data['futa_trimest_4_1']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page2[0]f2_8[0]':
                        field.field_value = data_entry_data['futa_trimest_4_2']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page2[0]f2_9[0]':
                        field.field_value = data_entry_data['total_tax_obligation_1']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page2[0]f2_10[0]':
                        field.field_value = data_entry_data['total_tax_obligation_2']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page2[0]f2_11[0]':
                        field.field_value = data_entry_data['autorizated_person']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page2[0]f2_12[0]':
                        field.field_value = data_entry_data['authorized_person_phone']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page2[0]f2_13[0]':
                        field.field_value = data_entry_data['personal_number_id_1']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page2[0]f2_14[0]':
                        field.field_value = data_entry_data['personal_number_id_2']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page2[0]f2_15[0]':
                        field.field_value = data_entry_data['personal_number_id_3']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page2[0]f2_16[0]':
                        field.field_value = data_entry_data['personal_number_id_4']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page2[0]f2_17[0]':
                        field.field_value = data_entry_data['personal_number_id_5']
                        field.update()


                    elif field.field_name == 'topmostSubform[0]Page2[0]f2_27[0]':
                        field.field_value = data_entry_data['accountant_city']
                        field.update()

                    elif field.field_name == 'topmostSubform[0]Page2[0]f2_28[0]':
                        field.field_value = data_entry_data['accountant_state']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page2[0]f2_25[0]':
                        field.field_value = data_entry_data['accountant_addres']
                        field.update()
                    elif field.field_name == 'date_1':
                        field.field_value = data_entry_data['date_1']
                        field.update()
                    elif field.field_name == 'date_2':
                        field.field_value = data_entry_data['date_2']
                        field.update()
    
                    elif field.field_name == 'topmostSubform[0]Page2[0]f2_22[0]':
                        field.field_value = data_entry_data['accountant_ptin']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page2[0]f2_24[0]':
                        field.field_value = data_entry_data['accountant_ein']
                        field.update()

                    elif field.field_name == 'topmostSubform[0]Page2[0]f2_26[0]':
                        field.field_value = data_entry_data['accountant_phone']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page2[0]f2_29[0]':
                        field.field_value = data_entry_data['accountant_postal']
                        field.update()
                        

                        
                    elif field.field_name == 'topmostSubform[0]Page2[0]f2_18[0]':
                        field.field_value = data_entry_data['employer_personal_name']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page2[0]f2_21[0]':
                        field.field_value = data_entry_data['accountant_personal_name']
                        field.update()

                        
                    elif field.field_name == 'topmostSubform[0]Page2[0]f2_19[0]':
                        field.field_value = data_entry_data['employer_position']
                        field.update()
                    elif field.field_name == 'topmostSubform[0]Page2[0]f2_20[0]':
                        field.field_value = data_entry_data['employer_diurn_number']
                        field.update()


        doc.save(document_dir / output_file_name, incremental=False, encryption=fitz.PDF_ENCRYPT_KEEP)

    return document_dir / output_file_name
    