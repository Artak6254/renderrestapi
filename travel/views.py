from rest_framework import viewsets
from .models import (
    Logo, Navbars, HomepageBookingSearch,
    HomePageIntro, HomePageWhyChooseUs, 
    HomePageFaq,  Footer
)
from .serializers import (
     LogoSerializer, NavbarsSerializer, BookingSearchSerializer,
     HomePageIntroSerializer, HomePageWhyChooseUsSerializer,
     HomePageFaqSerializer, FooterSerializer
)


class LogoViewSet(viewsets.ModelViewSet):
    queryset = Logo.objects.all()
    serializer_class = LogoSerializer

class NavbarsViewSet(viewsets.ModelViewSet):
    queryset = Navbars.objects.all()  # Ավելացնել queryset
    serializer_class = NavbarsSerializer

    def get_queryset(self):
        lang = self.request.query_params.get('lang')  
        if lang:
            return Navbars.objects.filter(lang=lang) 
        return Navbars.objects.all()  

    

class HomePageIntroViewSet(viewsets.ModelViewSet):
    queryset = HomePageIntro.objects.all()
    serializer_class = HomePageIntroSerializer
    
    def get_queryset(self):
        lang = self.request.query_params.get('lang')  
        if lang:
            return HomePageIntro.objects.filter(lang=lang) 
        return HomePageIntro.objects.all()  



class BookingSearchViewSet(viewsets.ModelViewSet):
    queryset = HomepageBookingSearch.objects.all()
    serializer_class = BookingSearchSerializer

    def get_queryset(self):
        lang = self.request.query_params.get('lang')  
        if lang:
            return HomepageBookingSearch.objects.filter(lang=lang) 
        return HomepageBookingSearch.objects.all()  

class HomePageWhyChooseUsViewSet(viewsets.ModelViewSet):
     queryset = HomePageWhyChooseUs.objects.all()
     serializer_class = HomePageWhyChooseUsSerializer
    
     def get_queryset(self):
        lang = self.request.query_params.get('lang')  
        if lang:
            return HomePageWhyChooseUs.objects.filter(lang=lang) 
        return HomePageWhyChooseUs.objects.all()  



class HomePageFaqViewSet(viewsets.ModelViewSet):
    queryset = HomePageFaq.objects.all()
    serializer_class = HomePageFaqSerializer
    
    def get_queryset(self):
        lang = self.request.query_params.get('lang')  
        if lang:
            return HomePageFaq.objects.filter(lang=lang) 
        return HomePageFaq.objects.all()  





class FooterViewSet(viewsets.ModelViewSet):
    queryset = Footer.objects.all()  
    serializer_class = FooterSerializer
    
    def get_queryset(self):
        lang = self.request.query_params.get('lang')  
        if lang:
            return Footer.objects.filter(lang=lang) 
        return Footer.objects.all()  

               