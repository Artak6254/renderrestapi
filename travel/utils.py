from io import BytesIO
from django.template.loader import get_template
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

def generate_ticket_pdf(archive):
    passengers = archive.passengers_data

    context = {
        "name": archive.fullname,
        "passport_serial": archive.passport_serial,
        "phone": passengers[0].get("phone", ""),
        "ticket_number": archive.ticket_number,
        "departure_seat": passengers[0].get("departure_seat", ""),
        "return_seat": passengers[0].get("return_seat", ""),
        "flight_from": archive.flight_from,
        "flight_to": archive.flight_to,
        "flight_departure_date": archive.flight_departure_date,
        "flight_return_date": archive.flight_return_date,
        "departure_time": archive.departure_time,
        "arrival_time": archive.arrival_time,
        "bort_number": archive.bort_number,
        "adult_count": sum(1 for p in passengers if p['passenger_type'] == 'adult'),
        "child_count": sum(1 for p in passengers if p['passenger_type'] == 'child'),
        "baby_count": sum(1 for p in passengers if p['passenger_type'] == 'baby'),
        "total_price": archive.total_price,
    }
    return render_to_pdf('index.html', context)

def send_ticket_email(archive):
    pdf = generate_ticket_pdf(archive)
    if pdf:
        email = EmailMessage(
            subject="Ձեր ավիատոմսը",
            body=f"Բարև {archive.fullname}, կից կգտնեք Ձեր տոմսը։",
            from_email=formataddr(("NovAir", "youremail@gmail.com")),
            to=[archive.passengers_data[0].get("email")],
        )
        email.attach(f"ticket_{archive.fullname}.pdf", pdf.getvalue(), "application/pdf")
        email.send()
