from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LogoViewSet, NavbarsViewSet, 
    HomePageIntroViewSet, HomePageWhyChooseUsViewSet,
    HomePageFaqViewSet, FooterViewSet, BookingSearchViewSet,
    my_login_view, my_logout_view
)

router = DefaultRouter()
router.register(r'logo', LogoViewSet, basename="logo")
router.register(r'navbars', NavbarsViewSet, basename='navbars')
router.register(r'homepage_intro', HomePageIntroViewSet, basename="homepage_intro")
router.register(r'homepage_booking_search', BookingSearchViewSet, basename='homepage_booking_search')
router.register(r'homepage_why_choose_us', HomePageWhyChooseUsViewSet, basename="homepage_why_choose_us")
router.register(r'homepage_faq', HomePageFaqViewSet, basename="homepage_faq")
router.register(r'footers', FooterViewSet, basename="footers")

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('login/', my_login_view, name="login"),
    path('logout/', my_logout_view, name="logout"),
]
