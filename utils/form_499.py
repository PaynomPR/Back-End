from pathlib import Path
import fitz  # PyMuPDF
from models.queries.queryForm499 import queryForm499


def form_withheld_499_pdf_generator(company_id, year, period):

    
    rute = Path(__file__).parent.absolute()
    document_dir = rute.parent / 'output_files'
    source_file_name = 'template/plantilla_form_499.pdf'
    output_file_name = 'form_499.pdf'

    
    data_entry = queryForm499(company_id, year, period)
    

    try:
        # Open the source PDF
        doc = fitz.open(document_dir / source_file_name)
    except Exception as e:
        print(f"Failed to open document: {e}")
        return None

    try:
        for page_number in range(len(doc)):
            page = doc[page_number]
            for field in page.widgets():
                if field.field_type == fitz.PDF_WIDGET_TYPE_TEXT:
                    if field.field_name in data_entry:
                        value = data_entry[field.field_name]
                        # Check if the value is a float (decimal) and format it
                        if isinstance(value, float):
                            field.field_value = f"{value:.2f}"
                        else:
                            field.field_value = str(value) # Ensure non-float values are strings
                        field.update()
        doc.save(document_dir / output_file_name, incremental=False, encryption=fitz.PDF_ENCRYPT_KEEP)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        doc.close()

    return document_dir / output_file_name
    
