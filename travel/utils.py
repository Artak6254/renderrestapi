# travel/utils.py

from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import render_to_string

def generate_flight_ticket_pdf(passenger):
    html = render_to_string("pdf_templates/ticket_template.html", {"passenger": passenger})
    result = BytesIO()
    pisa_status = pisa.CreatePDF(src=html, dest=result)
    
    if pisa_status.err:
        return None
    return result.getvalue()
