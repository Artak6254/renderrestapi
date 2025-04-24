from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LogoViewSet, NavbarsViewSet, 
    HomePageIntroViewSet, HomePageWhyChooseUsViewSet,
    HomePageFaqViewSet, FooterViewSet, BookingSearchViewSet,LanguageListViewSet, 
    FlightsViewSet, FlightSeatsViewSet, TicketsViewSet, PassngersViewSet,
    my_login_view, my_logout_view, AvailableFlightsView
)

router = DefaultRouter()
router.register(r'languages', LanguageListViewSet, basename="languages")
router.register(r'logo', LogoViewSet, basename="logo")
router.register(r'navbars', NavbarsViewSet, basename='navbars')
router.register(r'homepage_intro', HomePageIntroViewSet, basename="homepage_intro")
router.register(r'homepage_booking_search', BookingSearchViewSet, basename='homepage_booking_search')
router.register(r'homepage_why_choose_us', HomePageWhyChooseUsViewSet, basename="homepage_why_choose_us")
router.register(r'homepage_faq', HomePageFaqViewSet, basename="homepage_faq")
router.register(r'footers', FooterViewSet, basename="footers")
router.register(r'flights', FlightsViewSet, basename="flights")
router.register(r'flights_seats', FlightSeatsViewSet, basename="flights_seats")
router.register(r'tickets', TicketsViewSet, basename="tickets")
router.register(r'passangers', PassngersViewSet, basename="passangers")




urlpatterns = [
    path('api/', include(router.urls)),
    path("flights/search/", AvailableFlightsView.as_view(), name="available-flights"),
    path('api-auth/', include('rest_framework.urls')),
    path('login/', my_login_view, name="login"),
    path('logout/', my_logout_view, name="logout"),
]
