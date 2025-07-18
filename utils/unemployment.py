from pathlib import Path
import fitz  # PyMuPDF

from database.config import session
from models.queries.queryFormUnemployment import queryFormUnemployment
import os

""" def form_unemployment_pdf_generator(company_id, year, period):

    
    rute = Path(__file__).parent.absolute()
    document_dir = rute.parent / 'output_files'
    source_file_name = 'template/plantilla_unemployees_tmp.pdf'
    # source_file_name_2 = 'template/planilla_form_unemployees_part_2.pdf'
    output_file_name = 'unemployment.pdf'

    data_entry = []

    
    data_entry = queryFormUnemployment(company_id, year, period)
    employees = data_entry['employees']

    


    
    doc = fitz.open(document_dir / source_file_name)
    

    
    for page_number in range(len(doc)):
        page = doc[page_number]
        for field in page.widgets():
            if field.field_type == fitz.PDF_WIDGET_TYPE_TEXT:
                if field.field_name in data_entry:
                    field.field_value = data_entry[field.field_name]
                    field.update()

    doc.save(document_dir / output_file_name, incremental=False, encryption=fitz.PDF_ENCRYPT_KEEP)

        
    
    doc.close()


    return document_dir / output_file_name """
    

def form_unemployment_pdf_generator(company_id, year, period):
    
    # Directory paths
    rute = Path(__file__).parent.absolute()
    document_dir = rute.parent / 'output_files'
    source_file_name = 'template/plantilla_unemployees_tmp.pdf'
    output_file_name_prefix = 'unemployment_part_'  # Prefix for individual PDFs

    data_entry = []

    
    # Retrieve employee data
    data_entry = queryFormUnemployment(company_id, year, period)
    employees = data_entry.get('employees', []) # Use .get to handle cases where 'employees' might be missing
        
    
    
    # Split employees into groups of 24
    employee_groups = [employees[i:i+24] for i in range(0, len(employees), 24)]
    
    # Generate individual PDFs with employee lists (up to 24 per PDF)
    for i, employee_group in enumerate(employee_groups):
        output_file_name = document_dir / (output_file_name_prefix + str(i+1) + '.pdf')

        # Open the source PDF
        doc = fitz.open(document_dir / source_file_name)
        # Update form fields with general data (company_id, year, period, etc.)
        for page_number in range(len(doc)):
            page = doc[page_number]
            for field in page.widgets():
                if field.field_type == fitz.PDF_WIDGET_TYPE_TEXT:
                    if field.field_name in data_entry:
                        field.field_value = str(data_entry[field.field_name]) # Ensure value is string
                        field.update()
        for emp_idx, employee in enumerate(employee_group):
            # Assuming your template has fields like 'employee_name_0', 'employee_id_0', 'employee_name_1', etc.
            # Adjust field names based on your actual template
            try:
                page_to_fill = doc[0] # Assuming employee data is filled on the first page of the template

                # Example: Fill employee name and ID fields
                # Replace 'employee_name_' and 'employee_id_' with your actual field prefixes
                name_field = page_to_fill.first_widget(f"employee_name_{emp_idx}")
                id_field = page_to_fill.first_widget(f"employee_id_{emp_idx}")
                if name_field and 'name' in employee: # Assuming employee dict has a 'name' key
                    name_field.field_value = str(employee['name'])
                    name_field.update()
                if id_field and 'id' in employee: # Assuming employee dict has an 'id' key
                    id_field.field_value = str(employee['id'])
                    id_field.update()
                # Update other employee-specific fields here
            except Exception as e:
                print(f"Error filling employee fields for employee {emp_idx}: {e}")
        # --- END OF IMPORTANT ADDITION ---

        # Save the individual PDF
        doc.save(output_file_name, incremental=False, encryption=fitz.PDF_ENCRYPT_KEEP)
        doc.close()

        

     # Combine individual PDFs into a single PDF
    def combine_pdfs(pdf_list, output_file_name):
        combined_doc = fitz.open()
        for pdf_path in pdf_list:
            # print("-----------------pdf_path-----------------"+pdf_path) # Debug print
            try:
                combined_doc.insert_pdf(fitz.open(pdf_path))
            except Exception as e:
                print(f"Error inserting {pdf_path}: {e}")
        combined_doc.save(output_file_name)
        combined_doc.close()

    pdf_list = []

    # Loop through files in the directory
    for filename in os.listdir(document_dir):
        if filename.startswith(output_file_name_prefix) and filename.endswith('.pdf'): # Ensure it's a PDF
            # Convert PosixPath to string and append to pdf_list
            pdf_path = (document_dir / filename).as_posix()
            pdf_list.append(pdf_path)

    # print("-----------------pdf_list-----------------") # Debug print
    # print(pdf_list) # Debug print
    combined_pdf_path = document_dir / 'unemployment_combined.pdf'

    combine_pdfs(pdf_list, combined_pdf_path)
   
    return combined_pdf_path
 