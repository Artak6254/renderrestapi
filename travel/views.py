import logging
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, F
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.middleware.csrf import get_token
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import qrcode
from django.db import transaction
from django.core.mail import EmailMessage
from django.views.decorators.csrf import ensure_csrf_cookie
from django_ratelimit.decorators import ratelimit
from django.http import JsonResponse
from rest_framework import viewsets, permissions
from django.contrib.sessions.models import Session
from django.db.models.signals import post_save
from django.dispatch import receiver
from reportlab.pdfgen import canvas
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .utils import generate_flight_ticket_pdf
from io import BytesIO
from datetime import datetime
from travel.permissions import IsAdminOrOwner
from .models import (
    Logo, Navbars, HomepageBookingSearch, HomePageIntro, LanguageList,
    HomePageWhyChooseUs, HomePageFaq, Footer, Flights, FlightSeats, Passengers, 
    Tickets, PassangersCount, FlightDirection)
from .serializers import (
    LogoSerializer, NavbarsSerializer, BookingSearchSerializer,
    HomePageIntroSerializer, HomePageWhyChooseUsSerializer, LanguageListSerializer,
    HomePageFaqSerializer, FooterSerializer, FlightsSerializer, FlightSeatsSerializer,
    TicketsSerializer, PassengersSerializer,FlightSearchSerializer, PassangersCountSerializer,
    FlightDirectionSerializer
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






class SearchAvailableFlightsView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        from_here = request.data.get("from_here")
        to_there = request.data.get("to_there")
        departure_date = request.data.get("departure_date")
        return_date = request.data.get("return_date")

        if not all([from_here, to_there]) or (not departure_date and not return_date):
            return Response({
                "error": "Provide at least one of departure_date or return_date, along with from_here and to_there"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Parse dates
        try:
            departure_date = datetime.strptime(departure_date, "%Y-%m-%d").date()
        except ValueError:
            return Response({
                "error": "Invalid departure_date format. Use YYYY-MM-DD."
            }, status=status.HTTP_400_BAD_REQUEST)

        if return_date:
            try:
                return_date = datetime.strptime(return_date, "%Y-%m-%d").date()
            except ValueError:
                return Response({
                    "error": "Invalid return_date format. Use YYYY-MM-DD."
                }, status=status.HTTP_400_BAD_REQUEST)

        adult_count = int(request.data.get("adult_count", 0))
        child_count = int(request.data.get("child_count", 0))
        baby_count = int(request.data.get("baby_count", 0))
        total_passenger_count = adult_count + child_count + baby_count
        seat_needed_count = adult_count + child_count  

        def collect_flights(from_h, to_h, date, seat_type):
            results = []
            flights = Flights.objects.filter(
                from_here=from_h,
                to_there=to_h,
                departure_date=date,
                is_active=True
            )

            for flight in flights:
                available_seats = FlightSeats.objects.filter(
                    flight=flight,
                    seat_type=seat_type,
                    is_taken=False
                ).order_by("seat_number")

                if available_seats.count() < seat_needed_count:
                    continue

                available_tickets = Tickets.objects.filter(
                    flight_id=flight,
                    is_active=True,
                    is_sold=False
                ).order_by("id")

                if available_tickets.count() < total_passenger_count:
                    continue

                selected_tickets = available_tickets[:total_passenger_count]
                remaining_adults = adult_count
                remaining_children = child_count
                remaining_babies = baby_count
                tickets_data = []

              
                for i, ticket in enumerate(selected_tickets):
                    seat = available_seats[i] if i < seat_needed_count else None

                    passenger_type = None
                    if remaining_adults > 0:
                        passenger_type = "adult"
                        remaining_adults -= 1
                    elif remaining_children > 0:
                        passenger_type = "child"
                        remaining_children -= 1
                    elif remaining_babies > 0:
                        passenger_type = "baby"
                        remaining_babies -= 1

                    serialized_ticket = TicketsSerializer(ticket).data
                    # if seat:
                    #     serialized_ticket["seat"] = seat.seat_number
                    serialized_ticket["passenger_type"] = passenger_type
                    tickets_data.append(serialized_ticket)

                flight_data = FlightsSerializer(flight).data
                flight_data["tickets"] = tickets_data

                # Միայն ուղևորների քանակով նստատեղեր
                flight_data["flight_seats"] = [
                    {
                        "id": seat.id,
                        "flight_id": seat.flight.id,
                        "seat_number": seat.seat_number,
                        "is_taken": seat.is_taken
                    }
                    for seat in available_seats[:seat_needed_count]
                ]

                flight_data["available_departure_seats"] = FlightSeats.objects.filter(
                    flight=flight, seat_type="departure", is_taken=False
                ).count()
                flight_data["available_return_seats"] = FlightSeats.objects.filter(
                    flight=flight, seat_type="return", is_taken=False
                ).count()

                results.append(flight_data)

            return results

        departure_flights = collect_flights(from_here, to_there, departure_date, seat_type="departure")
        return_flights = collect_flights(to_there, from_here, return_date, seat_type="return") if return_date else []

        if not departure_flights:
            return Response({
                "en": "No matching departure flights or tickets found.",
                "ru": "Подходящие рейсы на отправление или билеты не найдены.",
                "am": "Համապատասխան գնալու թռիչքներ կամ տոմսեր չեն գտնվել։"
            }, status=status.HTTP_404_NOT_FOUND)

        if return_date and not return_flights:
            return Response({
                "en": "No matching return flights or tickets found.",
                "ru": "Подходящие рейсы на возвращение или билеты не найдены.",
                "am": "Համապատասխան վերադարձի թռիչքներ կամ տոմսեր չեն գտնվել։"
            }, status=status.HTTP_404_NOT_FOUND)

        response_data = {
            "message": "Թռիչքները և տոմսերը հաջողությամբ գտնվեցին։",
            "departure_flights": departure_flights
        }

        if return_flights:
            response_data["return_flights"] = return_flights

        return Response(response_data, status=status.HTTP_200_OK)
        
        
        
        
        
        
class PassngersViewSet(viewsets.ModelViewSet):
    serializer_class = PassengersSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Passengers.objects.filter(
            Q(departure_seat__isnull=False) | Q(return_seat__isnull=False)
        ).distinct()

    def perform_create(self, serializer):
        passenger = serializer.save()

        # Գեներացնել PDF
        pdf_file = generate_flight_ticket_pdf(passenger)

        # Կցել PDF-ը ուղարկվող նամակին
        if pdf_file:
            email = EmailMessage(
                subject="Ձեր ավիատոմսը",
                body="Խնդրում ենք կցվածում գտնել Ձեր տոմսը:",
                from_email="noreply@yourdomain.com",
                to=[passenger.email],
            )
            email.attach("ticket.pdf", pdf_file, "application/pdf")
            email.send()




class FlightSeatsViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = FlightSeatsSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]

    def get_queryset(self):
        seat_type = self.request.query_params.get('seat_type', None)
        qs = FlightSeats.objects.filter(is_taken=False)

        if seat_type in ['departure', 'return']:
            qs = qs.filter(seat_type=seat_type)

        return qs
    

class FlightsViewSet(viewsets.ModelViewSet):
    serializer_class = FlightsSerializer

    def get_queryset(self):
        return Flights.objects.filter(is_active=True).filter(
            id__in=[f.id for f in Flights.objects.all() if f.has_available_seats()]
        )

    
    
    
class TicketsViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = TicketsSerializer

    def get_queryset(self):
        if self.action == 'list':
            return Tickets.objects.exclude(
                Q(passengers__departure_seat__is_taken=True) |
                Q(passengers__return_seat__is_taken=True)
            ).distinct()
        return Tickets.objects.all()

        
        



class PassangersCountViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = PassangersCount.objects.all()
    serializer_class = PassangersCountSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]
    

class FlightDirectionViewSet(viewsets.ModelViewSet):
    queryset = FlightDirection.objects.all()
    serializer_class = FlightDirectionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]    