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




@admin.register(SoldFlightArchive)
class SoldFlightArchiveAdmin(admin.ModelAdmin):
    actions = ['export_sold_archive_with_passengers']

    list_display = (
        'flight_from', 'flight_to', 'flight_departure_date', 'flight_return_date',
        'departure_time', 'arrival_time', 'total_price', 'total_passengers',
    )
 
    readonly_fields = (
        'flight_from', 'flight_to', 'flight_departure_date', 'flight_return_date',
        'departure_time', 'arrival_time', 'total_price',
        'total_passengers', 'display_passenger_table',
        'display_ticket_table', 'display_seat_table',
        'display_cancel_buttons',
    )

    exclude = ('passengers_data', 'ticket_data', 'seats')

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
                'display_ticket_table',
            )
        }),
        ('💺 Seat Info', {
            'fields': (
                'display_seat_table',
            )
        }),
        ('👥 Passenger Info', {
            'fields': (
                'display_passenger_table',
            )
        }),
        ('❌ Չեղարկման Գործողություն', {
            'fields': (
                'display_cancel_buttons',
            )
        }),
    )

    @admin.action(description="📤 Export All Passenger Data as CSV")
    def export_sold_archive_with_passengers(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sold_flight_archive.csv"'
        response.write('\ufeff')  # Excel BOM

        writer = csv.writer(response, delimiter=';')
        headers = [
            'Flight From', 'Flight To', 'Departure Date', 'Return Date',
            'Departure Time', 'Arrival Time', 'Total Price',
            'Ticket Number', 'Ticket Type', 'Ticket Is Sold',
            'Passenger Full Name', 'Passport Serial', 'Title',
            'Date of Birth', 'Citizenship', 'Phone', 'Email', 'Price', 'Passenger Type'
        ]
        writer.writerow(headers)

        for archive in queryset:
            passengers = archive.passengers_data or []
            for p in passengers:
                writer.writerow([
                    archive.flight_from,
                    archive.flight_to,
                    archive.flight_departure_date.strftime('%Y-%m-%d') if archive.flight_departure_date else '',
                    archive.flight_return_date.strftime('%Y-%m-%d') if archive.flight_return_date else '',
                    archive.departure_time,
                    archive.arrival_time,
                    archive.total_price,
                    p.get('ticket_number', ''),
                    p.get('ticket_type', ''),
                    p.get('ticket_is_sold', ''),
                    p.get('full_name', ''),
                    p.get('passport_serial', ''),
                    p.get('title', ''),
                    p.get('date_of_birth', ''),
                    p.get('citizenship', ''),
                    p.get('phone', ''),
                    p.get('email', ''),
                    p.get('price', ''),
                    p.get('passenger_type', ''),
                ])
        return response

    def display_passenger_table(self, obj):
        rows = ""
        for p in obj.passengers_data or []:
            rows += f"""
                <tr>
                    <td>{p.get("full_name", "")}</td>
                    <td>{p.get("passport_serial", "")}</td>
                    <td>{p.get("title", "")}</td>
                    <td>{p.get("date_of_birth", "")}</td>
                    <td>{p.get("citizenship", "")}</td>
                    <td>{p.get("phone", "")}</td>
                    <td>{p.get("email", "")}</td>
                    <td>{p.get("ticket_number", "")}</td>
                    <td>{p.get("ticket_type", "")}</td>
                    <td>{p.get("passenger_type", "")}</td>
                    <td>{p.get("price", "")}</td>
                </tr>
            """
        return mark_safe(f"""
        <table style="width:100%; border-collapse: collapse;" border="1">
            <tr>
                <th>Full Name</th><th>Passport</th><th>Title</th><th>Date of Birth</th>
                <th>Citizenship</th><th>Phone</th><th>Email</th><th>Ticket No.</th>
                <th>Type</th><th>Category</th><th>Price</th>
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
                        onclick="cancelTicket('{ticket_id}', '{ticket_number}')" 
                        style="
                            background-color:#dc3545; color:white; border:none; 
                            padding:6px 12px; border-radius:5px; cursor:pointer; margin-bottom: 5px;
                        ">
                        Չեղարկել {ticket_number}
                    </button>
                """

        buttons += """
        <script>
        function cancelTicket(ticketId, ticketNumber) {
            if (!confirm('Չեղարկե՞լ տոմս ' + ticketNumber + '։')) return;

            fetch('/api/cancel_ticket/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ ticket_id: ticketId }),
                credentials: 'same-origin'
            })
            .then(response => {
                if (!response.ok) {
                    return response.text().then(text => { throw new Error(text) });
                }
                return response.json();
            })
            .then(data => {
                if (data.message) {
                    alert(data.message);
                    location.reload();
                } else if (data.error) {
                    alert("թռիչքը չեղարկվեց")
                }
            })
            .catch(error => {
                console.error("Սերվերի սխալ:", error);
                alert("Թռիչքը չեղարկվեց։");
            });
        }
        </script>
        """
        return mark_safe(buttons)




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



# class FlightTicketInline(admin.TabularInline):
#     model = Tickets
#     extra = 0
#     readonly_fields = (
#         'is_active', 'is_sold',
#         'ticket_number',
#         'price'
#     )
#     can_delete = False
    
    
    
class FlightSeatsInline(admin.TabularInline):
    model = FlightSeats
    extra = 0  # չցուցադրել ավելորդ դատարկ row-եր
    readonly_fields = ('seat_type', 'seat_number', 'is_taken')
    can_delete = False



# class TicketsInline(admin.TabularInline):
#     model = Tickets
#     extra = 0  
#     fields = ('is_active', 'is_sold','price')  
#     show_change_link = True



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



