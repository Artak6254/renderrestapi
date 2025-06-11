from io import BytesIO
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.core.mail import EmailMessage
from email.utils import formataddr


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    if not pdf.err:
        return result
    return None


def generate_ticket_pdf(passenger):
    context = {
        "name": passenger.full_name,
        "email": passenger.email,
        "ticket_id": passenger.ticket_id.id,
        "departure_seat": passenger.departure_seat_id.seat_number if passenger.departure_seat_id else None,
        "return_seat": passenger.return_seat_id.seat_number if passenger.return_seat_id else None,
    }
    return render_to_pdf('index.html', context)


def send_ticket_email(passenger):
    pdf = generate_ticket_pdf(passenger)
    # if pdf:
    #     email = EmailMessage(
    #         subject="Ձեր ավիատոմսը",
    #         body=f"Բարև {passenger.full_name}, կից կգտնեք Ձեր տոմսը։",
    #         from_email=formataddr(("NovAir", "youremail@gmail.com")),
    #         to=[passenger.email],
    #     )
    #     email.attach(f"ticket_{passenger.full_name}.pdf", pdf.getvalue(), "application/pdf")
    #     email.send()
