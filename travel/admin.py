from django.contrib import admin
from django.contrib.sites.models import Site
from .permissions import IsAdminOrOwner
from django.contrib.staticfiles.storage import staticfiles_storage
from django.templatetags.static import static

from .models import (
    Logo, Navbars, SubnavbarsList, HomePageIntro, HomepageBookingSearch, 
    CalendarFieldList, PassangerFieldList, HomePageWhyChooseUs, ReasonsList, 
    HomePageFaq, HomePageQuestion, Footer, FooterLinks, FooterSocial,AvailableTickets,
    PlaneSeats,PassngerList,SoldTickets,LanguageList
)


admin.site.unregister(Site) 
admin.site.site_header = 'NOVAIR'
admin.site.site_title = 'NOVAIR'
admin.site.index_title = 'Welcome to NOVAIR Admin Panel'




admin.site.register(Logo)
admin.site.register(HomePageIntro)
admin.site.register(AvailableTickets)
admin.site.register(PlaneSeats)
admin.site.register(LanguageList)


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


class PassngerListInline(admin.StackedInline):
    model = PassngerList
    extra = 1

@admin.register(SoldTickets)
class SoldTicketsAdmin(admin.ModelAdmin): 
    inlines = [ PassngerListInline ]

