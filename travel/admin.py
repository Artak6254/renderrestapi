from django.contrib import admin
from .permissions import IsAdminOrOwner
from django.contrib.staticfiles.storage import staticfiles_storage
from django.templatetags.static import static

from .models import (
    Logo, Navbars, SubnavbarsList, HomePageIntro, HomepageBookingSearch, 
    CalendarFieldList, PassangerFieldList, HomePageWhyChooseUs, ReasonsList, 
    HomePageFaq, HomePageQuestion, Footer, FooterLinks, FooterSocial
)


admin.site.site_header = 'NOVAIR'
admin.site.site_title = 'NOVAIR'
admin.site.index_title = 'Welcome to NOVAIR Admin Panel'





@admin.register(Logo)
class LogoAdmin(admin.ModelAdmin):
    list_display = ('id', 'logo')
    search_fields = ('logo',)
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_staff



class SubmavbarsListInline(admin.TabularInline):
    model = SubnavbarsList
    extra = 1
    
@admin.register(Navbars)
class NavbarsAdmin(admin.ModelAdmin):
    list_display = ('id', 'lang', 'title')
    search_fields = ('lang', 'title')
    inlines = [SubmavbarsListInline]
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    


@admin.register(HomePageIntro)
class HomePageIntroAdmin(admin.ModelAdmin):
    list_display = ('id', 'lang', 'title_logo_image', 'descr', 'image')
    search_fields = ('lang', 'title_logo_image', 'descr')
    list_filter = ('lang',)
    def has_change_permission(self, request, obj=None):
        return request.user.is_staff


class CalendarFieldListInline(admin.TabularInline):
    model = CalendarFieldList
    extra = 1
    classes = ['calendar-field-inline'] 


class PassengerFieldListInline(admin.TabularInline):
    model = PassangerFieldList
    extra = 1
    classes = ['passenger-field-inline'] 


@admin.register(HomepageBookingSearch)
class HomepageBookingSearchAdmin(admin.ModelAdmin):
    inlines = [CalendarFieldListInline, PassengerFieldListInline]

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff





class ReasonsListAdminInline(admin.TabularInline):  
    model = ReasonsList
    extra = 1  

@admin.register(HomePageWhyChooseUs)
class HomePageWhyChooseUsAdmin(admin.ModelAdmin):
    list_display = ('id', 'lang', 'title', 'sub_title', 'image', 'map_image')
    search_fields = ('lang', 'title', 'sub_title')
    list_filter = ('lang',)
    inlines = [ReasonsListAdminInline] 
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_staff
    

class HomePageQuestionInline(admin.TabularInline):  
    model = HomePageQuestion
    extra = 1  

@admin.register(HomePageFaq)
class HomePageFaqAdmin(admin.ModelAdmin):
    list_display = ('id', 'lang', 'title')
    search_fields = ('lang', 'title')
    inlines = [HomePageQuestionInline]  

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff




class FooterLinksInline(admin.TabularInline): 
    model = FooterLinks
    extra = 1  

class FooterSocialInline(admin.TabularInline):  
    model = FooterSocial
    extra = 1 

@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    list_display = ('id', 'lang')
    search_fields = ('lang',)
    inlines = [FooterLinksInline, FooterSocialInline]  # Ավելացնում ենք ներքին դասերը

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff