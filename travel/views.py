from rest_framework import viewsets
from rest_framework import permissions
from travel.permissions import IsAdminOrOwner
from .models import (
    Logo, Navbars, HomepageBookingSearch,
    HomePageIntro, HomePageWhyChooseUs, 
    HomePageFaq, Footer
)
from .serializers import (
    LogoSerializer, NavbarsSerializer, BookingSearchSerializer,
    HomePageIntroSerializer, HomePageWhyChooseUsSerializer,
    HomePageFaqSerializer, FooterSerializer
)


class LangFilteredViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = self.queryset  
        lang = self.request.query_params.get('lang')  
        if lang:
            queryset = queryset.filter(lang=lang)  
        return queryset

class LogoViewSet(LangFilteredViewSet):
    queryset = Logo.objects.all()
    serializer_class = LogoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]
   
class NavbarsViewSet(LangFilteredViewSet):
    queryset = Navbars.objects.all()
    serializer_class = NavbarsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]

class HomePageIntroViewSet(LangFilteredViewSet):
    queryset = HomePageIntro.objects.all()
    serializer_class = HomePageIntroSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]
    
class BookingSearchViewSet(LangFilteredViewSet):
    queryset = HomepageBookingSearch.objects.all()
    serializer_class = BookingSearchSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]

class HomePageWhyChooseUsViewSet(LangFilteredViewSet):
    queryset = HomePageWhyChooseUs.objects.all()
    serializer_class = HomePageWhyChooseUsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]

class HomePageFaqViewSet(LangFilteredViewSet):
    queryset = HomePageFaq.objects.all()
    serializer_class = HomePageFaqSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]

class FooterViewSet(LangFilteredViewSet):
    queryset = Footer.objects.all()
    serializer_class = FooterSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]
