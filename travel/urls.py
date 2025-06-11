from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import (
    LogoViewSet, NavbarsViewSet, 
    HomePageIntroViewSet, HomePageWhyChooseUsViewSet,
    HomePageFaqViewSet, FooterViewSet, BookingSearchViewSet, LanguageListViewSet, 
    FlightsViewSet, FlightSeatsViewSet, TicketsViewSet, PassngersViewSet,
    my_login_view, my_logout_view, SearchAvailableFlightsView,PassangersCountViewSet,
    FlightDirectionViewSet,AirTransContactView,InfoForTransferView,ImportantInfoView,
    TopHeadingAirTransView,TopHeadingBaggageView,BaggageBoxView,
    TopHeadingCertificateView,CertificateDescrView,CertificatesImagesView,TopHeadingContactView,
    ContactImagesView,ContactInfoView,
    SeatChoiceDescriptionView,TopHeadingSeatChoiceView,SeatChoicePriceViews,ListTransContactView,   BookingResultsPageLabelView ,BookingNavigationView,
    OrderSummaryView, BookingClientInfoPageLabelView, BookingClientInfoPageLabelView,
    BookingPaymentPageLabelView
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
router.register(r'passangers_count', PassangersCountViewSet, basename="passangers_count")
router.register(r'flight_direction', FlightDirectionViewSet, basename="flight_direction")

router.register(r'air_trans_contact', AirTransContactView, basename="air_trans_contact")
router.register(r'air_list', ListTransContactView, basename="air_list")
router.register(r'inf_for_transfer', InfoForTransferView, basename="inf_for_transfer")
router.register(r'import_info', ImportantInfoView, basename="import_info")
router.register(r'top_heading_air_trans', TopHeadingAirTransView, basename="top_heading_air_trans")
router.register(r'top_heading_baggage', TopHeadingBaggageView, basename="top_heading_baggage")
router.register(r'baggage_row_box', BaggageBoxView, basename="baggage_row_box")
router.register(r'top_heading_certificate', TopHeadingCertificateView, basename="top_heading_certificate")
router.register(r'certificate_descr', CertificateDescrView, basename="certificate_descr")
router.register(r'certificates_images', CertificatesImagesView, basename="certificates_images")
router.register(r'top_heading_contact', TopHeadingContactView, basename="top_heading_contact")
router.register(r'contact_images', ContactImagesView, basename="contact_images")
router.register(r'contact_info', ContactInfoView, basename="contact_info")
router.register(r'seat_choice_description', SeatChoiceDescriptionView, basename="seat_choice_description")
router.register(r'top_heading_seat_choice', TopHeadingSeatChoiceView, basename="top_heading_seat_choice")
router.register(r'seat_choice_price', SeatChoicePriceViews, basename="seat_choice_price")
router.register(r'booking_results_page_label', BookingResultsPageLabelView, basename="booking_results_page_label")
router.register(r'booking_navigation', BookingNavigationView, basename="booking_navigation")
router.register(r'order_summary', OrderSummaryView, basename="order_summary")

router.register(r'booking_client_info_page_label', BookingClientInfoPageLabelView, basename="booking_client_info_page_label")
router.register(r'booking_payment_page_label', BookingPaymentPageLabelView, basename="booking_payment_page_labe")    
    
    
    
    

    
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/search-flights/', SearchAvailableFlightsView.as_view(), name="search_flights"),  # ✅ Ահա այստեղ ճիշտ գրանցված է
    path('api-auth/', include('rest_framework.urls')),
    path('login/', my_login_view, name="login"),
    path('logout/', my_logout_view, name="logout"),
]


