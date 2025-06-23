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

def generate_ticket_pdf(archive_data: dict):
    passengers = archive_data.get("passengers_data", [])

    context = {
        "name": archive_data.get("fullname"),
        "passport_serial": archive_data.get("passport_serial"),
        "phone": passengers[0].get("phone", "") if passengers else "",
        "ticket_number": archive_data.get("ticket_number"),
        "departure_seat": passengers[0].get("departure_seat", "") if passengers else "",
        "return_seat": passengers[0].get("return_seat", "") if passengers else "",
        "flight_from": archive_data.get("flight_from"),
        "flight_to": archive_data.get("flight_to"),
        "flight_departure_date": archive_data.get("flight_departure_date"),
        "flight_return_date": archive_data.get("flight_return_date"),
        "departure_time": archive_data.get("departure_time"),
        "arrival_time": archive_data.get("arrival_time"),
        "bort_number": archive_data.get("bort_number"),
        "adult_count": sum(1 for p in passengers if p.get('passenger_type') == 'adult'),
        "child_count": sum(1 for p in passengers if p.get('passenger_type') == 'child'),
        "baby_count": sum(1 for p in passengers if p.get('passenger_type') == 'baby'),
        "total_price": archive_data.get("total_price"),
    }
    return render_to_pdf('index.html', context)

def send_ticket_email(archive_data: dict):
    pdf = generate_ticket_pdf(archive_data)
    if pdf:
        email = EmailMessage(
            subject="Ձեր ավիատոմսը",
            body=f"Բարև {archive_data.get('fullname')}, կից կգտնեք Ձեր տոմսը։",
            from_email=formataddr(("NovAir", "youremail@gmail.com")),
            to=[archive_data.get("passengers_data", [{}])[0].get("email")],
        )
        email.attach(f"ticket_{archive_data.get('fullname')}.pdf", pdf.getvalue(), "application/pdf")
        email.send()
