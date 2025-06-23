import logging
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from .auth import CsrfExemptSessionAuthentication 
from django.db.models import Q, F
from rest_framework.decorators import action
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
from datetime import timedelta
from django.db import transaction
from django.core.mail import EmailMessage
from django.utils import timezone
from email.utils import formataddr
from django.views.decorators.csrf import ensure_csrf_cookie
from django_ratelimit.decorators import ratelimit
from django.http import JsonResponse
from rest_framework import viewsets, permissions
from django.contrib.sessions.models import Session
from django.shortcuts import render, get_object_or_404
from django.db.models.signals import post_save
from django.dispatch import receiver
from reportlab.pdfgen import canvas
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from io import BytesIO
from .utils import send_ticket_email


from datetime import datetime
from travel.permissions import IsAdminOrOwner
from .models import (
    Logo, Navbars, HomepageBookingSearch, HomePageIntro, LanguageList,
    HomePageWhyChooseUs, HomePageFaq, Footer, Flights, FlightSeats, Passengers, 
    Tickets, PassangersCount, FlightDirection, AirTransContact,InfoForTransferContact,
    ImportantInfo,TopHeadingAirTrans,TopHeadingBaggage,BaggageRowBox,
    TopHeadingCertificate,CertificateDescr,CertificatesImages,TopHeadingContact,
    ContactImages,ContactInfo,SeatChoiceDescription,
    TopHeadingSeatChoice,SeatChoicePrice,ListAirContact,TicketPrice,
    BookingResultsPageLabel ,BookingNavigation, OrderSummary, BookingClientInfoPageLabel,
    BookingPaymentPageLabel,SoldFlightArchive,AboutUsTopHeading,AboutUsDescr,ContactIntro,
    TopContact,ContactNewInfo,ContactMap
    )
from .serializers import (
    LogoSerializer, NavbarsSerializer, BookingSearchSerializer,
    HomePageIntroSerializer, HomePageWhyChooseUsSerializer, LanguageListSerializer,
    HomePageFaqSerializer, FooterSerializer, FlightsSerializer, FlightSeatsSerializer,
    TicketsSerializer, PassengersSerializer,FlightSearchSerializer, PassangersCountSerializer,
    FlightDirectionSerializer,AirTransContactSerializer,InfoForTransferContactSerializer, 
    ImportantInfoSerializer,TopHeadingAirTransSerializer,TopHeadingBaggageSerializer,
    BaggageBoxSerializer,TopHeadingCertificateSerializer,
    CertificateDescrSerializer,CertificatesImagesSerializer,TopHeadingContactSerializer,
    ContactImagesSerializer,ContactInfoSerializer,SeatChoiceDescriptionSerializer,
    TopHeadingSeatChoiceSerializer,SeatChoicePriceSerializer,ListAirContactSerializer, BookingResultsPageLabelSerializer,
    BookingNavigationSerializer, OrderSummarySerializer, BookingClientInfoPageLabelSerializer,
     BookingClientInfoPageLabelSerializer,BookingPaymentPageLabelSerializer,SoldFlightArchiveSerializer,ContactNewInfoSerializer,
     AboutUsTopHeadingSerializer,AboutUsDescrSerializer,ContactIntroSerializer,TopContactSerializer,ContactMapSerializer
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

        # Որոշում ենք տոմսի տեսակ
        ticket_type = "round-trip" if return_date else "one-way"

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

                    if passenger_type == "adult":
                        price = 20000
                    elif passenger_type == "child":
                        price = 10000
                    else:
                        price = 5000

                    serialized_ticket = TicketsSerializer(ticket).data
                    serialized_ticket["passenger_type"] = passenger_type
                    serialized_ticket["price"] = price
                    serialized_ticket["ticket_type"] = ticket_type  # ✅ Ավելացրինք

                    tickets_data.append(serialized_ticket)

                flight_data = FlightsSerializer(flight).data
                flight_data["tickets"] = tickets_data

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
        if not departure_flights:
            departure_flights = collect_flights(from_here, to_there, departure_date, seat_type="return")

        return_flights = []
        if return_date:
            return_flights = collect_flights(to_there, from_here, return_date, seat_type="return")
            if not return_flights:
                return_flights = collect_flights(to_there, from_here, return_date, seat_type="departure")

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
    
    
    
class CancelTicketAPIView(APIView):
    def post(self, request):
        ticket_id = request.data.get("ticket_id")
        if not ticket_id:
            return Response({"error": "Ticket ID պետք է տրամադրել։"}, status=400)

        try:
            ticket = Tickets.objects.get(id=ticket_id)

            # Ուղևորների ազատում
            for passenger in ticket.passengers.all():
                if passenger.departure_seat_id:
                    departure_seat = passenger.departure_seat_id
                    departure_seat.is_taken = False
                    departure_seat.flight = None  # ջնջում ենք flight_id-ը
                    departure_seat.save()

                if passenger.return_seat_id:
                    return_seat = passenger.return_seat_id
                    return_seat.is_taken = False
                    return_seat.flight = None  # ջնջում ենք flight_id-ը
                    return_seat.save()

                passenger.delete()

            ticket.is_sold = False
            ticket.save()
            return Response({"message": "Տոմսը չեղարկվեց։"}, status=200)

        except Tickets.DoesNotExist:
            return Response({"error": "Տոմսը գոյություն չունի։"}, status=404)


class PassngersViewSet(viewsets.ModelViewSet):
    serializer_class = PassengersSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Passengers.objects.filter(
            Q(departure_seat_id__isnull=False) | Q(return_seat_id__isnull=False)
        ).distinct()

    def perform_create(self, serializer):
        passenger = serializer.save()

        # Թարմացնում ենք նստատեղերը որպես զբաղված
        if passenger.departure_seat_id:
            passenger.departure_seat_id.is_taken = True
            passenger.departure_seat_id.save()

        if passenger.return_seat_id:
            passenger.return_seat_id.is_taken = True
            passenger.return_seat_id.save()

        ticket = passenger.ticket_id
        passengers = ticket.passengers.all()

        all_seats_taken = all(
            (p.departure_seat_id and p.departure_seat_id.is_taken) and
            (not p.return_seat_id or p.return_seat_id.is_taken)
            for p in passengers
        )

        if all_seats_taken:
            ticket.is_sold = True
            ticket.save()





class FlightSeatsViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = FlightSeatsSerializer
    

    # Անջատում ենք pagination–ը
    pagination_class = None

    def get_queryset(self):
        queryset = FlightSeats.objects.all()

        # Ֆիլտր only flight_id, եթե կա
        flight_id = self.request.query_params.get('flight_id')
        if flight_id:
            queryset = queryset.filter(flight_id=flight_id)
    
        # Ֆիլտր ըստ is_taken, եթե պետք է
        is_taken = self.request.query_params.get('is_taken')
        if is_taken is not None:
            if is_taken.lower() == 'true':
                queryset = queryset.filter(is_taken=True)
            elif is_taken.lower() == 'false':
                queryset = queryset.filter(is_taken=False)

        # Սորտավորում՝ նախ departure (A/B), ապա return (C)
        return queryset.order_by('seat_type', 'seat_number')
    
    @action(detail=True, methods=['post'])
    def set_taken(self, request, pk=None):
        try:
            seat = FlightSeats.objects.get(pk=pk)
            seat.is_taken = True
            seat.save()
            return Response({'success': True, 'message': 'Նստատեղը նշվել է որպես վերցված։'})
        except FlightSeats.DoesNotExist:
            return Response({'error': 'Նստատեղը չի գտնվել։'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def hold(self, request, pk=None):
        try:
            with transaction.atomic():
                seat = FlightSeats.objects.select_for_update().get(pk=pk)
                if seat.is_taken:
                    return Response({"error": "Նստատեղը արդեն վաճառված է։", "ok": False}, status=status.HTTP_400_BAD_REQUEST)
                if seat.hold_until and seat.hold_until > timezone.now():
                    r_ret_am = seat.seat_type
                    r_ret_ru = seat.seat_type

                    if r_ret_am == "return":
                        r_ret_am = "վերադարձի"
                        r_ret_ru = "обратного"
                    elif r_ret_am == "departure":
                        r_ret_am = "մեկնման"
                        r_ret_ru = "отправления"

                    return Response({
                        "en": f"Seat {seat.seat_number} ({seat.seat_type}) is already reserved.",
                        "ru": f"Место {seat.seat_number} ({r_ret_ru} рейса) уже забронировано.",
                        "am": f"{seat.seat_number} {r_ret_am} նստատեղը արդեն պահված է։"
                    }, status=status.HTTP_400_BAD_REQUEST)


                seat.hold_until = timezone.now() + timedelta(minutes=35)
                seat.hold_by = request.data.get('user_id', 'anonymous')
                seat.save()

                return Response({"success": f"Նստատեղը պահվել է մինչև {seat.hold_until}։ ", "ok": True})
        except FlightSeats.DoesNotExist:
            return Response({"error": "Նստատեղը չի գտնվել։"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def book(self, request, pk=None):
        try:
            with transaction.atomic():
                seat = FlightSeats.objects.select_for_update().get(pk=pk)
                if seat.is_taken:
                    return Response({"error": "Նստատեղը արդեն վաճառված է։"}, status=status.HTTP_400_BAD_REQUEST)
                if seat.hold_until and seat.hold_until < timezone.now():
                    return Response({"error": "Նստատեղի պահելու ժամկետը անցել է։"}, status=status.HTTP_400_BAD_REQUEST)
                if seat.hold_by and seat.hold_by != request.data.get('user_id', 'anonymous'):
                    return Response({"error": "Դուք չեք պահել այս նստատեղը։"}, status=status.HTTP_403_FORBIDDEN)

                seat.is_taken = True
                seat.hold_until = None
                seat.hold_by = None
                seat.save()

                return Response({"success": "Պատվերը հաջողությամբ կատարվեց։"})
        except FlightSeats.DoesNotExist:
            return Response({"error": "Նստատեղը գոյություն չունի։"}, status=status.HTTP_404_NOT_FOUND)



class FlightsViewSet(viewsets.ModelViewSet):
    serializer_class = FlightsSerializer
    
    def get_queryset(self):
        return Flights.objects.filter(is_active=True).filter(
            id__in=[f.id for f in Flights.objects.all() if f.has_available_seats()]
        )

    
    
    
class TicketsViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = TicketsSerializer
    
    @action(detail=True, methods=['post'])
    def set_total_price(self, request, pk=None):
        try:
            ticket = Tickets.objects.get(pk=pk)
            total_price = request.data.get('total_price')

            if total_price is None:
                return Response({'error': 'Պետք է փոխանցել total_price։'}, status=status.HTTP_400_BAD_REQUEST)

            ticket.total_price = total_price
            ticket.save()

            return Response({'success': True, 'message': f'Total price-ը հաջողությամբ մուտքագրվեց', 'ticket_id': ticket.id})
        except Tickets.DoesNotExist:
            return Response({'error': 'Տոմսը չի գտնվել։'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def set_sold(self, request, pk=None):
        try:
            ticket = Tickets.objects.get(pk=pk)
            ticket.is_sold = True
            ticket.save()
            return Response({'success': True, 'message': f'Տոմսը վաճառված է։{ticket.id}'})
        except Tickets.DoesNotExist:
            return Response({'error': 'Տոմսը չի գտնվել։'}, status=status.HTTP_404_NOT_FOUND)
    
    def get_queryset(self):
        if self.action == 'list':
            return Tickets.objects.exclude(
                Q(passengers__departure_seat_id__is_taken=True) |
                Q(passengers__return_seat_id__is_taken=True)
            ).distinct()
        return Tickets.objects.all()

        



class PassangersCountViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = PassangersCount.objects.all()
    serializer_class = PassangersCountSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]



# views.py
class SoldFlightArchiveAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logger.info(f"Received data: {request.data}")
        serializer = SoldFlightArchiveSerializer(data=request.data)
        if serializer.is_valid():
            archive_instance = serializer.save()
            logger.info(f"Archive saved: {archive_instance}")

            try:
                # Որպես dict փոխանցում ենք validated_data
                send_ticket_email(serializer.validated_data)
                logger.info(f"Email sent for archive {archive_instance.id}")
            except Exception as e:
                logger.error(f"Email sending failed for archive {archive_instance.id}: {e}")

            return Response({"message": "Տվյալները հաջողությամբ արխիվացվեցին։"}, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
class FlightDirectionViewSet(viewsets.ModelViewSet):
      permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]

      @action(detail=False, methods=['get'], url_path='grouped')
      def grouped(self, request):
                flights = Flights.objects.all()

                from_here_data = []
                to_there_data = []

                seen_from = set()
                seen_to = set()

                for flight in flights:
                    if flight.from_here not in seen_from:
                        seen_from.add(flight.from_here)
                        from_here_data.append({
                            "id": flight.id,
                            "from_here": flight.from_here,
                            "flight_airport_name": flight.flight_airport_name,
                            "flight_airport_short_name": flight.flight_airport_short_name,
                        })

                    if flight.to_there not in seen_to:
                        seen_to.add(flight.to_there)
                        to_there_data.append({
                            "id": flight.id,
                            "to_there": flight.to_there,
                            "arrival_airport_name": flight.arrival_airport_name,
                            "arrival_airport_short_name": flight.arrival_airport_short_name,
                        })

                return Response({
                    "from_here": from_here_data,
                    "to_there": to_there_data
                })
                



# # static
class AirTransContactView(LangFilteredViewSet):
    queryset = AirTransContact.objects.all()
    serializer_class = AirTransContactSerializer   



class ListTransContactView(LangFilteredViewSet):
    queryset = ListAirContact.objects.all()
    serializer_class = ListAirContactSerializer       
    
    
    

class InfoForTransferView(LangFilteredViewSet):
    queryset = InfoForTransferContact.objects.all()
    serializer_class = InfoForTransferContactSerializer
                      
                
                



class ImportantInfoView(LangFilteredViewSet):
        queryset = ImportantInfo.objects.all()
        serializer_class = ImportantInfoSerializer
                
    
    
class TopHeadingAirTransView(LangFilteredViewSet):
        queryset = TopHeadingAirTrans.objects.all()
        serializer_class = TopHeadingAirTransSerializer
     
    
    
class TopHeadingBaggageView(LangFilteredViewSet):
        queryset = TopHeadingBaggage.objects.all()
        serializer_class = TopHeadingBaggageSerializer
        
    
    
class BaggageBoxView(LangFilteredViewSet):
        queryset = BaggageRowBox.objects.all()
        serializer_class = BaggageBoxSerializer
          
    


     


class TopHeadingCertificateView(LangFilteredViewSet):
        queryset = TopHeadingCertificate.objects.all()
        serializer_class = TopHeadingCertificateSerializer
      




class CertificateDescrView(LangFilteredViewSet):
        queryset = CertificateDescr.objects.all()
        serializer_class = CertificateDescrSerializer
        
    
    
  
class CertificatesImagesView(LangFilteredViewSet):
        queryset = CertificatesImages.objects.all()
        serializer_class = CertificatesImagesSerializer

    



class TopHeadingContactView(LangFilteredViewSet):
        queryset = TopHeadingContact.objects.all()
        serializer_class = TopHeadingContactSerializer
      
    
    

class ContactImagesView(LangFilteredViewSet):
        queryset = ContactImages.objects.all()
        serializer_class = ContactImagesSerializer
 
 
    

class ContactInfoView(LangFilteredViewSet):
        queryset = ContactInfo.objects.all()
        serializer_class = ContactInfoSerializer
  



class SeatChoiceDescriptionView(LangFilteredViewSet):
    queryset = SeatChoiceDescription.objects.all()
    serializer_class = SeatChoiceDescriptionSerializer
            
    
    
class TopHeadingSeatChoiceView(LangFilteredViewSet):
    queryset = TopHeadingSeatChoice.objects.all()
    serializer_class = TopHeadingSeatChoiceSerializer
                     
    
    

class SeatChoicePriceViews(LangFilteredViewSet):
        queryset = SeatChoicePrice.objects.all()
        serializer_class = SeatChoicePriceSerializer
              
    
    
    


        




 

class  BookingResultsPageLabelView(LangFilteredViewSet):
    queryset =  BookingResultsPageLabel.objects.all()
    serializer_class =  BookingResultsPageLabelSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]
    

class  BookingNavigationView(LangFilteredViewSet):
    queryset =  BookingNavigation.objects.all()
    serializer_class =  BookingNavigationSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]
    
    
class  OrderSummaryView(LangFilteredViewSet):
    queryset =  OrderSummary.objects.all()
    serializer_class =  OrderSummarySerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]
    

class  BookingClientInfoPageLabelView(LangFilteredViewSet):
    queryset =  BookingClientInfoPageLabel.objects.all()
    serializer_class =  BookingClientInfoPageLabelSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]
            
        

        
class BookingPaymentPageLabelView(LangFilteredViewSet):
    queryset =  BookingPaymentPageLabel.objects.all()
    serializer_class =  BookingPaymentPageLabelSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]
    
  
  
  
class AboutUsTopHeadingViewSet(LangFilteredViewSet):
    queryset = AboutUsTopHeading.objects.all()
    serializer_class = AboutUsTopHeadingSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]
    

class AboutUsDescrViewSet(LangFilteredViewSet):
    queryset = AboutUsDescr.objects.all()
    serializer_class = AboutUsDescrSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]
 
class ContactIntroViewSet(LangFilteredViewSet):
    queryset = ContactIntro.objects.all()
    serializer_class = ContactIntroSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]


class TopContactViewSet(LangFilteredViewSet):
    queryset = TopContact.objects.all()
    serializer_class = TopContactSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]
                                                                

class ContactNewInfoViewSet(LangFilteredViewSet):
    queryset = ContactNewInfo.objects.all()
    serializer_class = ContactNewInfoSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]


class ContactMapViewSet(LangFilteredViewSet):
    queryset = ContactMap.objects.all()
    serializer_class = ContactMapSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrOwner]
                                                                                                            