from pathlib import Path
import fitz  # PyMuPDF
from models.companies import Companies
from database.config import session
from models.queries.queryForm943 import queryForm943



def form_943_pdf_generator(company_id, year):
    rute = Path(__file__).parent.absolute()
    document_dir = rute.parent / 'output_files'
    source_file_name = 'template/f943.pdf'
    output_file_name = 'form_943.pdf'

    data_entry_data = queryForm943(company_id, year)
    if len(data_entry_data) > 0:
        with fitz.open(document_dir / source_file_name) as doc:
            for page_number in range(len(doc)):
                page = doc[page_number]
                for field in page.widgets():
                   

                    if field.field_type == fitz.PDF_WIDGET_TYPE_TEXT:
                        print("----------------field------------------")
                        print(field.field_name)
                        if field.field_name in data_entry_data:
                            field.field_value = data_entry_data[field.field_name]
                            print("----------------field.field_name------------------")
                            print(field.field_name)
                            field.update()



            doc.save(document_dir / output_file_name, incremental=False, encryption=fitz.PDF_ENCRYPT_KEEP)

        return document_dir / output_file_name
    else:
        return None
