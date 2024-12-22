import jinja2
import pdfkit
import pathlib
import platform

# Asegúrate de que el binario wkhtmltopdf esté en la siguiente ruta
dir_path = pathlib.Path().resolve()
wkhtmltopdf_path = (
f"{dir_path}/utils/pdfkit/binary/windows/wkhtmltopdf.exe"
if "windows" in platform.system().lower()
else f"{dir_path}/utils/pdfkit/binary/linux/wkhtmltopdf/local/bin/wkhtmltopdf"
)

def create_pdf(html_path, info, filename="output"):
    template_name = html_path.split("\\")[-1]
    template_path = html_path.replace(template_name, "")

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_path))
    template = env.get_template(template_name)
    html = template.render(info)

    options = {
    "page-size": "Letter",
    "orientation": "portrait",
    "margin-top": "0.16in",
    "margin-right": "0.1in",
    "margin-bottom": "0.16in",
    "margin-left": "0.1in",
    "encoding": "UTF-8",
    "dpi": 300,
    "no-outline": True,
    "enable-local-file-access": True,
    "images": True,
    "enable-javascript": True,
    }

    output_path = f"{dir_path}/utils/pdfkit/output/{filename}.pdf"
    css = f"{dir_path}/utils/pdfkit/assets/css/{html_path.split('/')[-1].split('.')[0]}.css"

    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

    pdfkit.from_string(
    html, output_path, css=css, options=options, configuration=config
    )

    return output_path