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
    BookingPaymentPageLabel,
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





# @admin.register(SoldFlightArchive)
# class SoldFlightArchiveAdmin(admin.ModelAdmin):
#     actions = ['export_sold_archive_with_passengers']
    
#     list_display = (
#         'flight_from', 'flight_to', 'flight_date', 'departure_time',
#         'arrival_time', 'bort_number', 'total_price',
#         'adult_count', 'child_count', 'baby_count', 'passenger_count',
#     )
    
#     readonly_fields = (
#         'flight_from', 'flight_to', 'flight_date', 'departure_time',
#         'arrival_time', 'bort_number', 'total_price',
#         'ticket_number', 'ticket_type', 'ticket_created_at',
#         'ticket_updated_at', 'ticket_is_sold',
#         'adult_count', 'child_count', 'baby_count', 'passenger_count',
#         'display_passenger_table','adult_price', 'child_price', 'baby_price',
#     )

#     exclude = ('passengers_data',)

#     fieldsets = (
#         ('✈️ Flight Info', {
#             'fields': (
#                 'flight_from', 'flight_to', 'flight_date',
#                 'departure_time', 'arrival_time', 'bort_number',
#             )
#         }),
#         ('🎫 Ticket Info', {
#             'fields': (
#                 'ticket_number', 'ticket_type',
#                 'ticket_created_at', 'ticket_updated_at',
#                 'ticket_is_sold', 'total_price',
#             )
#         }),
#         ('💵 Ticket Prices', {
#             'fields': (
#                 'adult_price', 'child_price', 'baby_price',
#             )
#         }),
#          ('👥 Passenger Info', {
#             'fields': (
#                 'adult_count', 'child_count', 'baby_count',
#                 'passenger_count', 'display_passenger_table',
#             )
#         }),
#     )

#     @admin.action(description="📤 Export All Passenger Data as CSV")
#     def export_sold_archive_with_passengers(self, request, queryset):
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="sold_flight_archive.csv"'
#         response.write('\ufeff')  # UTF-8 BOM for Excel

#         writer = csv.writer(response, delimiter=';')
#         headers = [
#             'Flight From', 'Flight To', 'Flight Date', 'Departure Time',
#             'Arrival Time', 'Bort Number', 'Total Price',
#             'Adult Count', 'Child Count', 'Baby Count', 'Total Passengers',
#             'Ticket Number', 'Ticket Type', 'Created At', 'Updated At', 'Is Sold',
#             'Passenger Full Name', 'Email', 'Passport', 'Seat (Dep)', 'Seat (Ret)',
#             'Baggage (Dep)', 'Baggage (Ret)', 'Individual Price', 'Gender'
#         ]
#         writer.writerow(headers)

#         for archive in queryset:
#             passengers = archive.passengers_data or []
#             for p in passengers:
#                 writer.writerow([
#                     archive.flight_from,
#                     archive.flight_to,
#                     archive.flight_date.strftime('%Y-%m-%d') if archive.flight_date else '',
#                     archive.departure_time.strftime('%H:%M') if archive.departure_time else '',
#                     archive.arrival_time.strftime('%H:%M') if archive.arrival_time else '',
#                     archive.bort_number,
#                     archive.total_price,
#                     archive.adult_count,
#                     archive.child_count,
#                     archive.baby_count,
#                     archive.passenger_count,
#                     archive.ticket_number,
#                     archive.ticket_type,
#                     archive.ticket_created_at.strftime('%Y-%m-%d %H:%M') if archive.ticket_created_at else '',
#                     archive.ticket_updated_at.strftime('%Y-%m-%d %H:%M') if archive.ticket_updated_at else '',
#                     archive.ticket_is_sold,
#                     p.get('full_name', ''),
#                     p.get('email', ''),
#                     p.get('passport_serial', ''),
#                     p.get('seat_departure', ''),
#                     p.get('seat_return', ''),
#                     p.get('departure_baggage', ''),
#                     p.get('return_baggage', ''),
#                     p.get('individual_total_price', ''),
#                     p.get('title', ''),
#                 ])
#         return response

#     def adult_count(self, obj):
#         return sum(1 for p in obj.passengers_data if str(p.get('title', '')).strip().lower() in ['adult', 'մեծահասակ'])
#     adult_count.short_description = "Adults"

#     def child_count(self, obj):
#         return sum(1 for p in obj.passengers_data if str(p.get('title', '')).strip().lower() in ['child', 'երեխա'])
#     child_count.short_description = "Children"

#     def baby_count(self, obj):
#         return sum(1 for p in obj.passengers_data if str(p.get('title', '')).strip().lower() in ['baby', 'մանուկ'])
#     baby_count.short_description = "Babies"

#     def passenger_count(self, obj):
#         return len(obj.passengers_data)
#     passenger_count.short_description = "Total Passengers"

#     def display_passenger_table(self, obj):
#         rows = ""
#         total_all_price = 0

#         for p in obj.passengers_data:
#             individual_total = p.get("individual_total_price", 0) or 0
#             try:
#                 individual_total = int(individual_total)
#             except (ValueError, TypeError):
#                 individual_total = 0
#             total_all_price += individual_total
#             rows += f"""
#                 <tr>
#                     <td>{p.get("full_name", "")}</td>
#                     <td>{p.get("email", "")}</td>
#                     <td>{p.get("title", "")}</td>
#                     <td>{p.get("passport_serial", "")}</td>
#                     <td>{p.get("seat_departure", "")} - {p.get("seat_departure_price", 0)} ֏</td>
#                     <td>{p.get("seat_return", "")} - {p.get("seat_return_price", 0)} ֏</td>
#                     <td>{p.get("departure_baggage", 0)} kg</td>
#                     <td>{p.get("return_baggage", 0)} kg</td>
#                     <td>{individual_total} ֏</td>
#                 </tr>
#             """

#         rows += f"""
#             <tr style="font-weight: bold; background-color: #e6f7ff;">
#                 <td colspan="8" style="text-align: right;">Total All Price:</td>
#                 <td>{total_all_price} ֏</td>
#             </tr>
#         """

#         html = f"""
#         <style>
#             table.passenger-table {{
#                 border-collapse: collapse;
#                 width: 100%;
#                 margin-top: 10px;
#             }}
#             table.passenger-table th, table.passenger-table td {{
#                 border: 1px solid #999;
#                 padding: 5px 10px;
#                 text-align: center;
#             }}
#             table.passenger-table th {{
#                 background-color: #f0f0f0;
#             }}
#         </style>
#         <table class="passenger-table">
#             <tr>
#                 <th>Full Name</th>
#                 <th>Email</th>
#                 <th>Gender</th>
#                 <th>Passport</th>
#                 <th>Seat (Dep) + Price</th>
#                 <th>Seat (Ret) + Price</th>
#                 <th>Baggage (Dep)</th>
#                 <th>Baggage (Ret)</th>
#                 <th>Total (Each)</th>
#             </tr>
#             {rows}
#         </table>
#         """
#         return mark_safe(html)
#     display_passenger_table.short_description = "Passenger Info"

#     def has_add_permission(self, request):
#         return False

#     def has_change_permission(self, request, obj=None):
#         return False






@admin.register(Tickets)
class TicketsAdmin(admin.ModelAdmin):
    list_display = ("ticket_number", "flight_id", "is_sold", "is_active")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Եթե is_sold=True է ու տվյալն արդեն պահպանված է բազայում
        # if obj.is_sold:
            # archive_sold_ticket_data(obj.id)




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



