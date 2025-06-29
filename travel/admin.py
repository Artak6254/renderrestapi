from django.contrib import admin
from .forms import PassengersAdminForm 
from django.contrib.sites.models import Site
from .permissions import IsAdminOrOwner
import datetime
import csv
from django_admin_search.admin import AdvancedSearchAdmin
from django.http import HttpResponseRedirect
from django.urls import reverse,path
from django.template import loader
from django.http import HttpResponse
from rangefilter.filters import DateRangeFilter
from django.contrib.staticfiles.storage import staticfiles_storage
from django.templatetags.static import static
# from .views import archive_sold_ticket_data
from django.utils.html import format_html
from django.utils.safestring import mark_safe
import json
from .forms import BookingTicketsSearchForm
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.db.models import JSONField
from django.forms import Textarea

from .models import (
    Logo, Navbars, SubnavbarsList, HomePageIntro, HomepageBookingSearch, 
    CalendarFieldList, PassangerFieldList, HomePageWhyChooseUs, ReasonsList, 
    HomePageFaq, HomePageQuestion, Footer, FooterLinks, FooterSocial,
    LanguageList, Tickets,Flights, FlightSeats, Passengers,PassangersCount,
    AirTransContact,InfoForTransferContact,
    ImportantInfo,TopHeadingAirTrans,TopHeadingBaggage,BaggageRowBox,
    TopHeadingCertificate,CertificateDescr,CertificatesImages,TopHeadingContact,
    ContactImages,ContactInfo,SeatChoiceDescription,
    TopHeadingSeatChoice,SeatChoicePrice,ListAirContact,BookingTickets,
    SectionHeadingAirTrans,HandLuggage, Baggage,PathCertificate,Paragraphs,Image,
    TopHeadingPath,Contact,Social,SupportText,ListTransferInfo,ListImportantInfo,FlightSchedule,
    
    BookingResultsPageLabel ,BookingNavigation, OrderSummary, BookingClientInfoPageLabel,
    BookingPaymentPageLabel,SoldFlightArchive,AboutUsTopHeading,AboutUsDescr,ContactIntro,
    TopContact,ContactNewInfo,ContactMap
)


admin.site.unregister(Site) 
admin.site.site_header = 'NOVAIR'
admin.site.site_title = 'NOVAIR'
admin.site.index_title = 'Welcome to NOVAIR Admin Panel'






@admin.register(BookingTickets)
class BookTicketsAdmin(admin.ModelAdmin):
    change_list_template = "admin/travel/bookingtickets/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        return urls
    
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False  # Optional՝ չթույլատրել ջնջել նույնպես





@admin.register(SoldFlightArchive)
class SoldFlightArchiveAdmin(admin.ModelAdmin):
    actions = ['export_ticket_data_as_xml']

    list_display = (
        'flight_from', 'flight_to', 'flight_departure_date', 'flight_return_date',
        'departure_time', 'arrival_time', 'total_price', 'total_passengers',
    )
    
    
    date_hierarchy = 'flight_departure_date'
    list_filter = (
        ('flight_departure_date', DateRangeFilter),
        ('flight_return_date', DateRangeFilter),
    )
    formfield_overrides = {
        JSONField: {'widget': Textarea(attrs={'rows': 10, 'cols': 100})}
    }

    fieldsets = (
        ('✈️ Flight Info', {
            'fields': (
                'flight_from', 'flight_to',
                'flight_departure_date', 'flight_return_date',
                'departure_time', 'arrival_time',
            )
        }),
        ('💵 Pricing Info', {
            'fields': (
                'total_price', 'total_passengers',
            )
        }),
        ('🎫 Ticket Info', {
            'fields': (
                'ticket_data',  # ✅ JSONField խմբագրելի
                'display_ticket_table',  # ✅ Աղյուսակով ցուցադրում
            )
        }),
        ('💺 Seat Info', {
            'fields': (
                'seats',  # ✅ JSONField խմբագրելի
                'display_seat_table',
            )
        }),
        ('👥 Passenger Info', {
            'fields': (
                'passengers_data',  # ✅ JSONField խմբագրելի
                'display_passenger_table',
            )
        }),
        ('❌ Չեղարկման Գործողություն', {
            'fields': (
                'display_cancel_buttons',
            )
        }),
    )

    readonly_fields = (
        'display_passenger_table',
        'display_ticket_table',
        'display_seat_table',
        'display_cancel_buttons',
    )

    exclude = ()

    @admin.action(description="📤 Export Tickets as XML")
    def export_ticket_data_as_xml(self, request, queryset):
        from xml.etree.ElementTree import Element, SubElement, tostring
        from xml.dom import minidom

        root = Element("SoldFlightArchives")

        for archive in queryset:
            archive_elem = SubElement(root, "SoldFlightArchive")
            SubElement(archive_elem, "FlightFrom").text = archive.flight_from
            SubElement(archive_elem, "FlightTo").text = archive.flight_to
            SubElement(archive_elem, "DepartureDate").text = archive.flight_departure_date.strftime('%Y-%m-%d') if archive.flight_departure_date else ''
            SubElement(archive_elem, "ReturnDate").text = archive.flight_return_date.strftime('%Y-%m-%d') if archive.flight_return_date else ''
            SubElement(archive_elem, "DepartureTime").text = archive.departure_time
            SubElement(archive_elem, "ArrivalTime").text = archive.arrival_time
            SubElement(archive_elem, "TotalPrice").text = str(archive.total_price)

            tickets_elem = SubElement(archive_elem, "Tickets")
            for t in archive.ticket_data or []:
                ticket_elem = SubElement(tickets_elem, "Ticket")
                SubElement(ticket_elem, "TicketID").text = str(t.get("ticket_id", ""))
                SubElement(ticket_elem, "TicketNumber").text = t.get("ticket_number", "")
                SubElement(ticket_elem, "TicketType").text = t.get("ticket_type", "")
                SubElement(ticket_elem, "Price").text = str(t.get("price", ""))
                SubElement(ticket_elem, "TicketIsSold").text = str(t.get("ticket_is_sold", ""))

        # Pretty print the XML
        rough_string = tostring(root, encoding='utf-8')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ")

        response = HttpResponse(pretty_xml, content_type='application/xml')
        response['Content-Disposition'] = 'attachment; filename="tickets_export.xml"'
        return response

    def display_passenger_table(self, obj):
        rows = ""
        for p in obj.passengers_data or []:
            rows += f"""
                <tr>
                    <td>{p.get("name", "")}</td>
                    <td>{p.get("surname", "")}</td>
                    <td>{p.get("passport_serial", "")}</td>
                    <td>{p.get("passport_validity_period", "")}</td>
                    <td>{p.get("title", "")}</td>
                    <td>{p.get("date_of_birth", "")}</td>
                    <td>{p.get("citizenship", "")}</td>
                    <td>{p.get("phone", "")}</td>
                    <td>{p.get("email", "")}</td>
                    <td>{p.get("passenger_type", "")}</td>
                    <td>{p.get("price", "")}</td>
                </tr>
            """
        return mark_safe(f"""
        <table style="width:100%; border-collapse: collapse;" border="1">
            <tr>
                <th>Name</th><th>Surname</th><th>Passport</th><th>Passport Validate</th>
                <th>Title</th><th>Date of Birth</th><th>Citizenship</th>
                <th>Phone</th><th>Email</th><th>Passenger Type</th><th>Price</th>
            </tr>{rows}
        </table>
        """)

    def display_ticket_table(self, obj):
        rows = ""
        for t in obj.ticket_data or []:
            rows += f"""
                <tr>
                    <td>{t.get("ticket_id", "")}</td>
                    <td>{t.get("ticket_number", "")}</td>
                    <td>{t.get("ticket_type", "")}</td>
                    <td>{t.get("price", "")}</td>
                    <td>{t.get("ticket_is_sold", "")}</td>
                </tr>
            """
        return mark_safe(f"""
        <table style="width:100%; border-collapse: collapse;" border="1">
            <tr>
                <th>Ticket ID</th><th>Number</th><th>Type</th><th>Price</th><th>Sold</th>
            </tr>{rows}
        </table>
        """)

    def display_seat_table(self, obj):
        rows = ""
        for s in obj.seats or []:
            rows += f"""
                <tr>
                    <td>{s.get("seat_id", "")}</td>
                    <td>{s.get("seat_number", "")}</td>
                    <td>{s.get("seat_type", "")}</td>
                    <td>{s.get("flight_id", "")}</td>
                </tr>
            """
        return mark_safe(f"""
        <table style="width:100%; border-collapse: collapse;" border="1">
            <tr>
                <th>Seat ID</th><th>Number</th><th>Type</th><th>Flight ID</th>
            </tr>{rows}
        </table>
        """)

    
    def display_seat_table(self, obj):
        rows = ""
        for s in obj.seats or []:
            rows += f"""
                <tr>
                    <td>{s.get("seat_id", "")}</td>
                    <td>{s.get("seat_number", "")}</td>
                    <td>{s.get("seat_type", "")}</td>
                    <td>{s.get("is_taken", "")}</td>
                    <td>{s.get("flight_id", "")}</td>
                </tr>
            """
        return mark_safe(f"""
            <table style="width:100%; border-collapse: collapse;" border="1">
                <tr>
                    <th>Seat ID</th><th>Number</th><th>Type</th><th>Is Taken</th><th>Flight ID</th>
                </tr>{rows}
            </table>
        """)
    
    def display_cancel_buttons(self, obj):
        if not obj.ticket_data:
            return "-"

        buttons = ""
        for ticket in obj.ticket_data:
            ticket_id = ticket.get("ticket_id")
            ticket_number = ticket.get("ticket_number", "Unknown")

            if ticket_id:
                buttons += f"""
                    <button 
                       onclick="cancelTicket('{ticket_id}', '{ticket_number}', event)" 
                        style="
                            background-color:#dc3545; color:white; border:none; 
                            padding:6px 12px; border-radius:5px; cursor:pointer; margin-bottom: 5px;
                        ">
                        Չեղարկել {ticket_number}
                    </button>
                """

        buttons += """
        <script>
        // Get CSRF token from cookie
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        const csrftoken = getCookie('csrftoken');

        function cancelTicket(ticketId, ticketNumber, event) {
            if (!confirm('Չեղարկե՞լ տոմս ' + ticketNumber + '։')) return;

            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
            const btn = event.target;

            fetch('/api/cancel_ticket/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({ ticket_id: ticketId }),
                credentials: 'include'
            })
            .then(response => {
                if (!response.ok) {
                    return response.text().then(text => { throw new Error(text) });
                }
                return response.json();
            })
            .then(data => {
                alert(data.message || "Տոմսը չեղարկվեց։");
                btn.innerText = "Չեղարկված ✅";
                btn.disabled = true;
                btn.style.backgroundColor = "#6c757d";
                btn.style.cursor = "not-allowed";
            })
            .catch(error => {
                console.error("Սերվերի սխալ:", error);
                alert("Չեղարկման սխալ։");
            });
        }

        </script>
        """

        return mark_safe(buttons)

    def has_add_permission(self, request):
        return False




@admin.register(Tickets)
class TicketsAdmin(admin.ModelAdmin):
    list_display = ("ticket_number", "flight_id", "is_sold", "is_active")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)





admin.site.register(FlightSchedule)
admin.site.register(Logo)
admin.site.register(HomePageIntro)
admin.site.register(LanguageList)

admin.site.register(FlightSeats)
admin.site.register(PassangersCount)


admin.site.register(AirTransContact)
admin.site.register(InfoForTransferContact)
admin.site.register(ImportantInfo)
admin.site.register(TopHeadingAirTrans)
admin.site.register(TopHeadingBaggage)
admin.site.register(BaggageRowBox)

admin.site.register(HandLuggage)
admin.site.register(TopHeadingCertificate)
admin.site.register(CertificateDescr)
admin.site.register(CertificatesImages)
admin.site.register(PathCertificate)
admin.site.register(TopHeadingContact)
admin.site.register(ContactImages)
admin.site.register(ContactInfo)
admin.site.register(SeatChoiceDescription)
admin.site.register(TopHeadingSeatChoice)
admin.site.register(SeatChoicePrice)
admin.site.register(ListAirContact)
admin.site.register(SectionHeadingAirTrans)

admin.site.register(Baggage)
admin.site.register(Paragraphs)
admin.site.register(Image)

admin.site.register(TopHeadingPath)
admin.site.register(Contact)
admin.site.register(Social)
admin.site.register(SupportText)


admin.site.register(ListTransferInfo)
admin.site.register(ListImportantInfo)


admin.site.register(BookingResultsPageLabel)
admin.site.register(BookingNavigation)
admin.site.register(OrderSummary)
admin.site.register(BookingClientInfoPageLabel)

admin.site.register(BookingPaymentPageLabel)



admin.site.register(AboutUsTopHeading)
admin.site.register(AboutUsDescr)
admin.site.register(ContactIntro)
admin.site.register(TopContact)
admin.site.register(ContactNewInfo)
admin.site.register(ContactMap)




@admin.register(Passengers)
class PassengersAdmin(admin.ModelAdmin):
    form = PassengersAdminForm
    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        import datetime

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="passengers_data.csv"'
        response.write('\ufeff')  # Excel-ի համար UTF-8 BOM

        writer = csv.writer(response, delimiter=';')

        column_headers = [
            'Full Name',
            'Title',
            'Passport Number',
            'Birth Date',
            'Citizenship',
            'Email',
            'Phone',
            'Departure Baggage',
            'Return Baggage',
        ]
        field_names = [
            'full_name',
            'title',
            'passport_serial',
            'date_of_birth',
            'citizenship',
            'email',
            'phone',
            'departure_baggage_weight',
            'return_baggage_weight',
        ]

        writer.writerow(column_headers)

        for passenger in queryset:
            row = []
            for field in field_names:
                value = getattr(passenger, field, '')
                if field == 'date_of_birth' and isinstance(value, (datetime.date, datetime.datetime)):
                    value = value.strftime('%Y-%m-%d')  
                row.append(value)
            writer.writerow(row)

        return response

    export_as_csv.short_description = "Export CSV"



    
    
    
class FlightSeatsInline(admin.TabularInline):
    model = FlightSeats
    extra = 0  # չցուցադրել ավելորդ դատարկ row-եր
    readonly_fields = ('seat_type', 'seat_number', 'is_taken')
    can_delete = False




class FlightSeatsInline(admin.TabularInline):
    model = FlightSeats
    extra = 0
    fields = ('seat_number', 'seat_type', 'is_taken')
    show_change_link = True





@admin.register(Flights)
class FlightsAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_here', 'to_there', 'departure_date', 'is_active')
    list_filter = (
        ('departure_date', DateRangeFilter),
        'from_here',
        'to_there',
        'is_active',
    )
    search_fields = ('from_here', 'to_there')
    inlines = [ FlightSeatsInline]

# TicketsInline

class SubnavbarsListInline(admin.TabularInline):  
    model = SubnavbarsList
    extra = 1  

@admin.register(Navbars)
class NavbarsList(admin.ModelAdmin):
    inlines = [SubnavbarsListInline]


class CalendarFieldListInline(admin.StackedInline): 
    model = CalendarFieldList
    extra = 1

class PassangerFieldListInline(admin.StackedInline): 
    model = PassangerFieldList
    extra = 1
    
@admin.register(HomepageBookingSearch)
class Booking(admin.ModelAdmin):
    inlines = [CalendarFieldListInline,PassangerFieldListInline]


class ReasonsList(admin.StackedInline):
    model = ReasonsList
    extra = 1

@admin.register(HomePageWhyChooseUs)
class WhyChooseUs(admin.ModelAdmin):
    inlines = [ReasonsList]



class FaqQuestionInline(admin.StackedInline):
    model = HomePageQuestion
    extra = 1

@admin.register(HomePageFaq)
class FaqAdmin(admin.ModelAdmin):
    inlines = [FaqQuestionInline]


class FooterLinksInline(admin.StackedInline):
    model = FooterLinks
    extra = 1

class FooterSocialInline(admin.StackedInline):
    model = FooterSocial
    extra = 1

@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin): 
    inlines = [FooterLinksInline, FooterSocialInline]



