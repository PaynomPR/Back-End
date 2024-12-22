from pathlib import Path
import fitz  # PyMuPDF
from models.companies import Companies
from database.config import session
from models.queries.queryForm941 import queryForm941



def form_941_pdf_generator(company_id, year, period):
    rute = Path(__file__).parent.absolute()
    document_dir = rute.parent / 'output_files'
    source_file_name = 'template/f941_plantilla.pdf'
    output_file_name = 'form_941.pdf'

    data_entry_data = queryForm941(company_id, year, period)
    if len(data_entry_data) > 0:
        with fitz.open(document_dir / source_file_name) as doc:
            for page_number in range(len(doc)):
                page = doc[page_number]
                for field in page.widgets():                    
                    if field.field_name in data_entry_data:
                        field.field_value = data_entry_data[field.field_name]
                        field.update()
                    



            doc.save(document_dir / output_file_name, incremental=False, encryption=fitz.PDF_ENCRYPT_KEEP)

        return document_dir / output_file_name
    else:
        return None
