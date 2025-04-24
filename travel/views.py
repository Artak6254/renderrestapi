import logging
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.middleware.csrf import get_token
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie
from django_ratelimit.decorators import ratelimit
from django.http import JsonResponse
from rest_framework import viewsets, permissions
from django.contrib.sessions.models import Session
from django.db.models.signals import post_save
from django.dispatch import receiver

from travel.permissions import IsAdminOrOwner
from .models import (
    Logo, Navbars, HomepageBookingSearch, HomePageIntro, LanguageList,
    HomePageWhyChooseUs, HomePageFaq, Footer, Flights, FlightSeats, Passengers, Tickets)
from .serializers import (
    LogoSerializer, NavbarsSerializer, BookingSearchSerializer,
    HomePageIntroSerializer, HomePageWhyChooseUsSerializer, LanguageListSerializer,
    HomePageFaqSerializer, FooterSerializer, FlightsSerializer, FlightSeatsSerializer,
    TicketsSerializer, PassengersSerializer,FlightSearchSerializer
)

# Log կարգավորումներ
logger = logging.getLogger(__name__)

def get_csrf_token(request):
    response = JsonResponse({'csrfToken': get_token(request)})
    response.set_cookie('csrftoken', get_token(request))
    return response
# ✅ Base class for filtering by language and user ownership




# ✅ Անվտանգ login
logger = logging.getLogger(__name__)

@csrf_exempt 
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def my_login_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests allowed"}, status=405)

    import json
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return JsonResponse({"error": "Username and password are required"}, status=400)

    user = authenticate(username=username, password=password)
    if user is not None:
        request.session.flush()
        login(request, user)
        request.session.cycle_key()

        session_id = request.session.session_key

        logger.info(f"User {user.username} logged in successfully.")
        return JsonResponse({
            "message": "Login successful",
            "username": user.username,
            "session_id": session_id  
        }, status=200)

    logger.warning(f"Failed login attempt for username: {username}")
    return JsonResponse({"error": "Invalid credentials"}, status=401)




def my_logout_view(request):
    logout(request)
    request.session.modified = True  # Logout-ից հետո session-ի թարմացում
    return JsonResponse({"message": "Logged out successfully"}, status=200)

# ✅ Signals՝ session-ի թարմացման համար
@receiver(post_save, sender=Logo)
@receiver(post_save, sender=Navbars)
@receiver(post_save, sender=HomepageBookingSearch)
@receiver(post_save, sender=HomePageIntro)
@receiver(post_save, sender=HomePageWhyChooseUs)
@receiver(post_save, sender=HomePageFaq)
@receiver(post_save, sender=Footer)
@receiver(post_save, sender=LanguageList)


def update_session_after_save(sender, instance, **kwargs):
    for session in Session.objects.all():
        session.modified = True
        session.save()






# ✅ API ViewSets

class LangFilteredViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = self.queryset.all().distinct()  # ORM Cache-ի շրջանցում
        lang = self.request.query_params.get('lang')
        user = self.request.user
        
        if lang:
            queryset = queryset.filter(lang=lang)
        if user.is_authenticated:
            queryset = queryset.filter(owner=user)
        
        return queryset


class LanguageListViewSet(LangFilteredViewSet):
    queryset = LanguageList.objects.all()
    serializer_class = LanguageListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]


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







class AvailableFlightsView(APIView):
    def post(self, request):
        serializer = FlightSearchSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        total_passengers = (
            data.get('adult_count', 0) +
            data.get('child_count', 0) +
            data.get('baby_count', 0)
        )

        flights = Flights.objects.filter(
            from_here=data['from_here'],
            to_there=data['to_there'],
            departure_date=data['departure_date'],
            return_date=data['return_date'],
            is_active=True
        )

        # Օպտիմալ՝ ներքին queryset-ով հաշվարկ
        available_flights = []
        for flight in flights:
            if flight.has_available_seats(total_passengers):
                available_flights.append(flight)

        if not available_flights:
            return Response(
                {"message": "Բավարար ազատ նստատեղեր չկան այս թռիչքներում։"},
                status=status.HTTP_404_NOT_FOUND
            )

        result_serializer = FlightsSerializer(available_flights, many=True)
        return Response(result_serializer.data, status=status.HTTP_200_OK)




class FlightsViewSet(viewsets.ModelViewSet):
    serializer_class = FlightsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]

    def get_queryset(self):
        queryset = Flights.objects.filter(is_active=True)
        return [flight for flight in queryset if flight.has_available_seats()]


class TicketsViewSet(viewsets.ModelViewSet):
    serializer_class = TicketsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]

    def get_queryset(self):
        # Only tickets with at least one taken seat
        return Tickets.objects.filter(
            Q(passengers__departure_seat__is_taken=True) |
            Q(passengers__return_seat__is_taken=True)
        ).distinct()
        
        
class FlightSeatsViewSet(viewsets.ModelViewSet):
    serializer_class = FlightSeatsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]

    def get_queryset(self):
        seat_type = self.request.query_params.get('seat_type', None)
        qs = FlightSeats.objects.filter(is_taken=False)

        if seat_type in ['departure', 'return']:
            qs = qs.filter(seat_type=seat_type)

        return qs
    
    

class PassngersViewSet(viewsets.ModelViewSet):
    serializer_class = PassengersSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]
    
    def get_queryset(self):
        # Only passengers who have at least one seat booked
        return Passengers.objects.filter(
            Q(departure_seat__isnull=False) | Q(return_seat__isnull=False)
        ).distinct()