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
    employees = data_entry['employees']
        
    
    
    # Split employees into groups of 24
    employee_groups = [employees[i:i+24] for i in range(0, len(employees), 24)]
    
    # Generate individual PDFs with employee lists (up to 24 per PDF)
    for i, employee_group in enumerate(employee_groups):
        output_file_name = document_dir / (output_file_name_prefix + str(i+1) + '.pdf')
      
        
        # Open the source PDF
        doc = fitz.open(document_dir / source_file_name)

        # Update form fields with data
        for page_number in range(len(doc)):
            page = doc[page_number]
            for field in page.widgets():
                if field.field_type == fitz.PDF_WIDGET_TYPE_TEXT:
                    if field.field_name in data_entry:
                        field.field_value = data_entry[field.field_name]
                        field.update()

        # Save the individual PDF
        doc.save(output_file_name, incremental=False, encryption=fitz.PDF_ENCRYPT_KEEP)
        doc.close()

        

    # Combine individual PDFs into a single PDF (optional)
    def combine_pdfs(pdf_list, output_file_name):
        
        combined_doc = fitz.open()

        for pdf_path in pdf_list:
            print("-----------------pdf_path-----------------"+pdf_path)
            combined_doc.insert_pdf(fitz.open(pdf_path))

        combined_doc.save(output_file_name)
        combined_doc.close()

    pdf_list = []

    # Loop through files in the directory
    for filename in os.listdir(document_dir):
        if filename.startswith(output_file_name_prefix):
            # Convert PosixPath to string and append to pdf_list
            pdf_path = (document_dir / filename).as_posix()  # Use .as_str() to get string
            pdf_list.append(pdf_path)

    print("-----------------pdf_list-----------------")
    print(pdf_list)  # Print the list of PDF paths as strings
    combined_pdf_path = document_dir / 'unemployment_combined.pdf'
    part1 = document_dir / 'unemployment_part_1.pdf'

    combine_pdfs(pdf_list, combined_pdf_path)
   
    return part1
 