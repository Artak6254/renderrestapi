import logging
from django.contrib.auth import login, authenticate, logout
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django_ratelimit.decorators import ratelimit
from django.http import JsonResponse
from rest_framework import viewsets, permissions
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



#  Log կարգավորումներ
logger = logging.getLogger(__name__)

#  Բոլոր view-երի համար base class
class LangFilteredViewSet(viewsets.ModelViewSet):
    """
    Ֆիլտրում է queryset-ը լեզվի և owner-ի հիման վրա։
    """
    def get_queryset(self):
        queryset = self.queryset
        lang = self.request.query_params.get('lang')  # Get language parameter
        user = self.request.user  # Get the current authenticated user
        
        if lang:
            queryset = queryset.filter(lang=lang)
        
        # 🔹 Ֆիլտրում ենք ըստ օգտատիրոջ
        if user.is_authenticated:
            queryset = queryset.filter(owner=user)
        
        return queryset

#  Անվտանգ login
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
@ensure_csrf_cookie
def my_login_view(request):
    """
    Հավելյալ անվտանգ login API:
    - Session Fixation պաշտպանություն
    - Brute-force պաշտպանության rate-limit
    - CSRF Token վերադարձ 
    """
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests allowed"}, status=405)

    username = request.POST.get('username')
    password = request.POST.get('password')

    if not username or not password:
        return JsonResponse({"error": "Username and password are required"}, status=400)

    user = authenticate(username=username, password=password)

    if user is not None:
        request.session.flush()  #  Session Fixation Attack պաշտպանություն
        login(request, user)
        request.session.cycle_key()

        logger.info(f"User {user.username} logged in successfully.")

        return JsonResponse({
            "message": "Login successful",
            "csrf_token": get_token(request)
        }, status=200)

    logger.warning(f"Failed login attempt for username: {username}")

    return JsonResponse({"error": "Invalid credentials"}, status=401)


def my_logout_view(request):
    """
    Օգտատիրոջ logout անելու ֆունկցիա:
    """
    logout(request)
    return JsonResponse({"message": "Logged out successfully"}, status=200)


class LogoViewSet(LangFilteredViewSet):
    queryset = Logo.objects.all().order_by("id")
    serializer_class = LogoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]


class NavbarsViewSet(LangFilteredViewSet):
    queryset = Navbars.objects.all().order_by("id")
    serializer_class = NavbarsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]


class HomePageIntroViewSet(LangFilteredViewSet):
    queryset = HomePageIntro.objects.all().order_by("id")
    serializer_class = HomePageIntroSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]


class BookingSearchViewSet(LangFilteredViewSet):
    queryset = HomepageBookingSearch.objects.all().order_by("id")
    serializer_class = BookingSearchSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]


class HomePageWhyChooseUsViewSet(LangFilteredViewSet):
    queryset = HomePageWhyChooseUs.objects.all().order_by("id")
    serializer_class = HomePageWhyChooseUsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]


class HomePageFaqViewSet(LangFilteredViewSet):
    queryset = HomePageFaq.objects.all().order_by("id")
    serializer_class = HomePageFaqSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]


class FooterViewSet(LangFilteredViewSet):
    queryset = Footer.objects.all().order_by("id")
    serializer_class = FooterSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]
