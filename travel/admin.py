from django.contrib import admin
from .forms import PassengersAdminForm 
from django.contrib.sites.models import Site
from .permissions import IsAdminOrOwner
from rangefilter.filters import DateRangeFilter
from django.contrib.staticfiles.storage import staticfiles_storage
from django.templatetags.static import static

from .models import (
    Logo, Navbars, SubnavbarsList, HomePageIntro, HomepageBookingSearch, 
    CalendarFieldList, PassangerFieldList, HomePageWhyChooseUs, ReasonsList, 
    HomePageFaq, HomePageQuestion, Footer, FooterLinks, FooterSocial,
    LanguageList, Tickets,Flights, FlightSeats, Passengers,PassangersCount,
    FlightDirection
)


admin.site.unregister(Site) 
admin.site.site_header = 'NOVAIR'
admin.site.site_title = 'NOVAIR'
admin.site.index_title = 'Welcome to NOVAIR Admin Panel'



admin.site.register(Logo)
admin.site.register(HomePageIntro)
admin.site.register(LanguageList)
# admin.site.register(Passengers)
admin.site.register(PassangersCount)
admin.site.register(FlightDirection)


@admin.register(Passengers)
class PassengersAdmin(admin.ModelAdmin):
    form = PassengersAdminForm
    
    
    

class FlightTicketInline(admin.TabularInline):
    model = Tickets
    extra = 0
    readonly_fields = (
        'is_active', 'is_sold',
        'ticket_number',
        'price'
    )
    can_delete = False
    
    
    
class FlightSeatsInline(admin.TabularInline):
    model = FlightSeats
    extra = 0  # չցուցադրել ավելորդ դատարկ row-եր
    readonly_fields = ('seat_type', 'seat_number', 'is_taken')
    can_delete = False



class TicketsInline(admin.TabularInline):
    model = Tickets
    extra = 0  
    fields = ('is_active', 'is_sold','price')  
    show_change_link = True



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
    inlines = [TicketsInline, FlightSeatsInline]



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



