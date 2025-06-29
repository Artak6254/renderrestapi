from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime
from django.core.validators import FileExtensionValidator
import random


class LanguageList(models.Model):
    title = models.CharField(max_length=30)
    code = models.CharField(max_length=10, null=True, blank=True)
    image = models.FileField(
        upload_to="language_list/images/", 
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg'])]
    )
    def __str__(self):
        return f"{self.title} {self.image}"

class Logo(models.Model):
    logo = models.FileField(
        upload_to="logos/",
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg'])]
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="logos", null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.logo}"

class Navbars(models.Model): 
    lang = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="navbars", null=True)
    
    class Meta:
        ordering = ['id']
    def __str__(self):
        return f"{self.lang} {self.title}"

class SubnavbarsList(models.Model):
    navbar = models.ForeignKey(Navbars, on_delete=models.CASCADE, related_name="subnavbar_list")  
    lang = models.CharField(max_length=20)
    title = models.CharField(max_length=120)
    url = models.CharField(max_length=30)
    class Meta:
        ordering = ['id']
        
    def __str__(self):
        return f"{self.lang} {self.title} {self.url}"


class HomePageIntro(models.Model):
    lang = models.CharField(max_length=20)
    title_logo_image = models.FileField(upload_to="home_page_intro/images/",
    validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg'])])  
    descr = models.CharField(max_length=255)
    image = models.FileField(
        upload_to="home_page_intro/images/",  
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg'])]
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="homepageIntro", null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.lang} {self.title_logo_image} {self.descr} {self.image}"




class HomepageBookingSearch(models.Model):
    lang = models.CharField(max_length=20)
    from_field_text = models.CharField(max_length=50)
    search_btn_text = models.CharField(max_length=90, default="Search")
    to_field_text = models.CharField(max_length=50)
    date_field_text = models.CharField(max_length=50)
    passangers_field_text = models.CharField( max_length=50, null=True)
    passangers_field_text_2 = models.CharField( max_length=50, null=True)
    select_field_text = models.CharField( max_length=50, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="homepagebookingsearch", null=True)
    class Meta:
        ordering = ['id'] 
    def __str__(self):
        return f"{self.lang} {self.from_field_text} {self.to_field_text} {self.date_field_text}"
    
    
    
    
class CalendarFieldList(models.Model):
    booking_search_calendar = models.ForeignKey(
        HomepageBookingSearch,
        on_delete=models.CASCADE,
        related_name="calendar_field_list"
    )
    lang = models.CharField(max_length=70)
    departure_field_text = models.CharField(max_length=100)
    return_field_text = models.CharField(max_length=100)
    btn_text = models.CharField(max_length=100, default='Default Value')
    one_way_ticket_btn_text = models.CharField(max_length=100, default='Default Value')
    class Meta:
        ordering = ['id'] 
    def __str__(self):
        return f"{self.lang} {self.departure_field_text}"

class PassangerFieldList(models.Model):
    booking_search_passangers = models.ForeignKey(HomepageBookingSearch, on_delete=models.CASCADE, related_name="passangers_field_list")  
    lang = models.CharField(max_length=70)
    adult_title = models.CharField(max_length=70, default="")
    adult_descr = models.CharField(max_length=255, default='Default adult description')
    child_text = models.CharField(max_length=70, default="")
    child_descr = models.CharField(max_length=255, default="")
    baby_title = models.CharField(max_length=255)
    baby_descr = models.CharField(max_length=255)
    btn_text = models.CharField(max_length=60, default='Default Value')
    class Meta:
        ordering = ['id'] 
    def __str__(self):
        return f"{self.lang} {self.adult_title} {self.adult_descr} {self.child_text}  {self.child_descr}  {self.baby_title} {self.baby_descr} {self.btn_text}"



class HomePageWhyChooseUs(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="choose_us", null=True)
    lang = models.CharField(max_length=20)
    title = models.CharField(max_length=120)
    sub_title = models.CharField(max_length=100)
    image = models.FileField(
        upload_to="why_choose_us/images/",  # Փոխարինել static/image-ս չփոխարկելու
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg'])]
    )
    map_image = models.FileField(upload_to="why_choose_us/images/")  # Փոխարինել static/image-ս

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.lang} {self.title} {self.sub_title} {self.image}"
    
    
class ReasonsList(models.Model):
    homepage_why_choose_us = models.ForeignKey(
        HomePageWhyChooseUs, 
        on_delete=models.CASCADE, 
        related_name="why_choose_reasons"  
    )
    lang = models.CharField(max_length=20)
    title = models.CharField(max_length=120)
    descr = models.TextField()
    class Meta:
        ordering = ['id']
    def __str__(self):
        return f"{self.lang} {self.title} {self.descr}"

class HomePageFaq(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="faq", null=True)
    lang = models.CharField(max_length=20)
    title = models.CharField(max_length=120)
    
    class Meta:
        ordering = ['id'] 
    def __str__(self):
        return f"{self.lang} {self.title}"

class HomePageQuestion(models.Model):
    faq = models.ForeignKey(HomePageFaq, on_delete=models.CASCADE, related_name="question_list", null=True)  
    lang = models.CharField(max_length=20)
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    class Meta:
        ordering = ['id']
    def __str__(self):
        return f"{self.lang} {self.question} {self.answer}"

class Footer(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="footer", null=True)
    lang = models.CharField(max_length=20)
    class Meta:
        ordering = ['id'] 
        
    def __str__(self):
        return f"{self.lang}"    
        
        
class FooterLinks(models.Model):
    footer = models.ForeignKey(
        Footer, 
        on_delete=models.CASCADE, 
        related_name="links"  
    )
    lang = models.CharField(max_length=10)
    title = models.CharField(max_length=255) 
    url = models.CharField(max_length=255)
    class Meta:
        ordering = ['id'] 
        
    def __str__(self):
        return f"{self.lang} {self.title} {self.url}"

class FooterSocial(models.Model):
    footer = models.ForeignKey(
        Footer, 
        on_delete=models.CASCADE, 
        related_name="social"  
    )
    lang = models.CharField(max_length=10)
    title = models.CharField(max_length=255) 
    url = models.CharField(max_length=255)
    class Meta:
        ordering = ['id'] 
        
    def __str__(self):
        return f"{self.lang} {self.title} {self.url}"



#------- booking ----------

# models.py
                      
class SoldFlightArchive(models.Model):
    archived_at = models.DateTimeField(auto_now_add=True)
    
    flight_from = models.CharField(max_length=120)
    flight_to = models.CharField(max_length=120)
    flight_departure_date = models.DateField(null=True, blank=True)
    flight_return_date = models.DateField(null=True, blank=True)
    departure_time = models.CharField(max_length=20)
    arrival_time = models.CharField(max_length=20)
    
    total_passengers = models.IntegerField()
    total_price = models.CharField(max_length=30, null=True, blank=True)

    passengers_data = models.JSONField()  # Ուղևորների տվյալներ
    ticket_data = models.JSONField(null=True, blank=True)  # Վաճառված տոմսերի ամբողջական տվյալներ
    seats = models.JSONField(null=True, blank=True)        # Նստատեղերի տվյալներ

    def __str__(self):
        return f"{self.flight_from} → {self.flight_to} | {self.flight_departure_date}"

   

class Flights(models.Model): 
    is_active = models.BooleanField(default=True)
    from_here = models.CharField(max_length=120)
    to_there = models.CharField(max_length=120)
    flight_airport_name = models.CharField(max_length=100, default="Unknown Airport")  
    flight_airport_short_name = models.CharField(max_length=100, default="Unknown short Airport")
    arrival_airport_name = models.CharField(max_length=20, null=True, blank=True)
    arrival_airport_short_name = models.CharField(max_length=20, null=True, blank=True)
    departure_time = models.CharField(max_length=20, default="00:00")
    arrival_time = models.CharField(max_length=20, default="00:00")
    departure_date = models.DateField(default="")
    bort_number = models.CharField(max_length=50)



    def has_available_seats(self, required_count=1):
        """Վերադարձնում է՝ արդյոք կա գոնե N ազատ տեղ"""
        return self.flight_seats.filter(is_taken=False).count() >= required_count

    def available_departure_seats(self):
        return self.flight_seats.filter(seat_type='departure', is_taken=False).count()

    def available_return_seats(self):
        return self.flight_seats.filter(seat_type='return', is_taken=False).count()



class Tickets(models.Model):
    flight_id = models.ForeignKey("Flights", on_delete=models.CASCADE, related_name="tickets")
    ticket_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)
    price = models.CharField(max_length=50, default="", blank=True)

    # ✅ Ավելացրու սա սխալը վերացնելու համար
    ticket_type = models.CharField(
        max_length=20,
        choices=[("one-way", "One Way"), ("round-trip", "Round Trip")]
    )

    def save(self, *args, **kwargs):
        if not self.ticket_number:
            self.ticket_number = self.generate_unique_ticket_number()
        super().save(*args, **kwargs)

    def generate_unique_ticket_number(self):
        while True:
            number = str(random.randint(1000000000, 9999999999))
            if not Tickets.objects.filter(ticket_number=number).exists():
                return number

    @property
    def total_price(self):
        return sum(p.price for p in self.passenger_tickets.all())

    def __str__(self):
        return f"Ticket #{self.ticket_number} | Flight: {self.flight_id}"

    
class Passengers(models.Model):
    ticket_id = models.ForeignKey("Tickets", on_delete=models.CASCADE, related_name="passengers")
    passenger_type = models.CharField(max_length=10, choices=[
        ('adult', 'Adult'),
        ('child', 'Child'),
        ('baby', 'Baby'),
    ], default="adult")
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=60, blank=True, null=True)
    title = models.CharField(max_length=10)
    name = models.CharField(max_length=100, default="add name")
    surname = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    citizenship = models.CharField(max_length=30)
    price = models.IntegerField(default=0)
    passport_serial = models.CharField(max_length=60)
    passport_validity_period = models.CharField(max_length=60, blank=True, null=True)
    departure_baggage_weight = models.CharField(max_length=20, blank=True, null=True, default="10")
    return_baggage_weight = models.CharField(max_length=20,blank=True, null=True, default="10")
    departure_seat_id = models.ForeignKey("FlightSeats", on_delete=models.CASCADE, related_name="departure_passengers", null=True, blank=True)
    return_seat_id = models.ForeignKey("FlightSeats", on_delete=models.CASCADE, related_name="return_passengers", null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} ({self.passenger_type})"


class FlightSeats(models.Model):
    SEAT_TYPE_CHOICES = [
        ('departure', 'Departure'),
        ('return', 'Return'),
    ]

    flight = models.ForeignKey('Flights', related_name='flight_seats', null=True, blank=True, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    seat_type = models.CharField(max_length=10, choices=SEAT_TYPE_CHOICES)
    is_taken = models.BooleanField(default=False)
    hold_until = models.DateTimeField(null=True, blank=True)
    hold_by = models.CharField(max_length=100, null=True, blank=True)
    departure_price = models.PositiveIntegerField(default=0)
    return_price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.flight} | {self.seat_type.upper()} Seat {self.seat_number}"
    
    
class BookingTickets(models.Model):
    is_round_trip = models.BooleanField(default=False)
    from_here = models.CharField(max_length=100)
    to_there = models.CharField(max_length=100)
    departure_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)

    adult_count = models.PositiveIntegerField(default=1)
    child_count = models.PositiveIntegerField(default=0)
    baby_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking from {self.from_here} to {self.to_there} ({'round' if self.is_round_trip else 'one-way'})"
    

class PassengersPrice(models.Model):
    adult_price = models.CharField(max_length=50, default="20000")
    child_price = models.CharField(max_length=50, default="10000")
    baby_price= models.CharField(max_length=50, default="5000")
    
    def __str__(self):
        return f"adult {self.adult_price} child {self.child_price} baby{self.baby_price}"
    


class FlightSchedule(models.Model):
    FLIGHT_TYPES = (
        ('departure', 'Departure'),
        ('return', 'Return')
    )
    flightschedule = models.ForeignKey('Flights', related_name='schedule', on_delete=models.CASCADE, null=True, blank=True)
    from_here = models.CharField(max_length=120)
    to_there = models.CharField(max_length=120)
    start_date = models.DateField()
    end_date = models.DateField()
    time = models.TimeField()
    flight_type = models.CharField(max_length=10, choices=FLIGHT_TYPES)
    flight_airport_name = models.CharField(max_length=100)
    flight_airport_short_name = models.CharField(max_length=100)
    arrival_time = models.CharField(max_length=20, default="00:00")
    arrival_airport_name = models.CharField(max_length=100)
    arrival_airport_short_name = models.CharField(max_length=100)
    bort_number = models.CharField(max_length=50, default='Unknown')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.generate_flights()

    def generate_flights(self):
        current_date = self.start_date
        seat_numbers = [
            'C1', 'C2', 'C3', 'C4', 'C5', 'C6',
            'B1', 'B2', 'B3', 'B4', 'B5', 'B6',
            'A1', 'A2', 'A3', 'A4', 'A5'
        ]

        while current_date <= self.end_date:
            flight = Flights.objects.create(
                from_here=self.from_here,
                to_there=self.to_there,
                flight_airport_name=self.flight_airport_name,
                flight_airport_short_name=self.flight_airport_short_name,
                arrival_airport_name=self.arrival_airport_name,
                arrival_airport_short_name=self.arrival_airport_short_name,
                departure_date=current_date,
                departure_time=self.time.strftime('%H:%M'),
                arrival_time=self.arrival_time, 
                bort_number=self.bort_number
            )

            # Ավելացնել նստատեղեր
            for seat_number in seat_numbers:
                FlightSeats.objects.create(
                    flight=flight,
                    seat_number=seat_number,
                    seat_type=self.flight_type,
                    is_taken=False
                )

            # Ավելացնել տոմսեր՝ յուրաքանչյուր տեղադրման համար
            for _ in seat_numbers:
                Tickets.objects.create(
                    flight_id=flight,
                    is_active=True,
                    is_sold=False,
                )

            current_date += timedelta(days=1)
            
    def __str__(self):
        return f"{self.from_here} {self.to_there}"        
            
         

class PassangersCount(models.Model):
    flight_id = models.ForeignKey(Flights, on_delete=models.CASCADE, related_name="passangers_count")
    adult_count = models.IntegerField(default=0)
    child_count = models.IntegerField(default=0)
    baby_count = models.IntegerField(default=0)
   
    def __str__(self):
        return f"Adult #{self.adult_count} | Child: {self.child_count} | Baby: {self.baby_count}"

 
class FlightDirection(models.Model):
    from_there = models.CharField(max_length=100)    
    to_there = models.CharField(max_length=100)
    flight_airport_name = models.CharField(max_length=100, default="Unknown Airport")
    flight_airport_short_name = models.CharField(max_length=100, default="Unknown short Airport")
    
    def __str__(self):
        return f"{self.from_there} {self.to_there} {self.flight_airport_name} {self.flight_airport_short_name}"
    


class TicketPrice(models.Model):
    ticket = models.ForeignKey(Tickets, on_delete=models.CASCADE, related_name="passenger_tickets")
    passenger = models.ForeignKey("Passengers", on_delete=models.CASCADE)  # Պահպանիր ուղևորի ինֆո
    passenger_type = models.CharField(max_length=10, choices=[("adult", "Adult"), ("child", "Child"), ("baby", "Baby")])
    price = models.PositiveIntegerField()





    # static





class BaggagesPage(models.Model):
    class Meta:
        verbose_name = "Air Baggage Page"
        verbose_name_plural = "Air Baggage Page"

    def __str__(self):
        return "Air Baggage Page"      
    
    

class CertificatePage(models.Model):
    class Meta:
        verbose_name = "Certificate Page"
        verbose_name_plural = "Certificate Page"

    def __str__(self):
        return "Air Certificate Page"      


class HeadContactPage(models.Model):
    class Meta:
        verbose_name = "HeadContact Page"
        verbose_name_plural = "HeadContact Page"

    def __str__(self):
        return "Air HeadContact Page"        
    

class OnlineRegistrationPage(models.Model):
    class Meta:
        verbose_name = "OnlineRegistration Page"
        verbose_name_plural = "OnlineRegistration Page"

    def __str__(self):
        return "Air OnlineRegistration Page"        

class SeatChoicePage(models.Model):
    class Meta:
        verbose_name = "SeatChoice Page"
        verbose_name_plural = "SeatChoice Page"

    def __str__(self):
        return "Air SeatChoice Page"       
    

class TransportConditionalPage(models.Model):
    class Meta:
        verbose_name = "TransportConditional Page"
        verbose_name_plural = "TransportConditional Page"

    def __str__(self):
        return "Air TransportConditional Page"       
    
    
    
    
    
class AirTransContact(models.Model):
    lang = models.CharField(max_length=20)
    heading = models.CharField(max_length=60)   
    text = models.CharField(max_length=255)
    subheading = models.CharField(max_length=50) 
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="air", null=True)
    def __str__(self):
        return self.heading
        
    

class ListAirContact(models.Model):
    list = models.ForeignKey(AirTransContact, on_delete=models.CASCADE, related_name="list", null=True, blank=True)
    text = models.CharField(max_length=120)    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="list_air", null=True)
   
    
class InfoForTransferContact(models.Model):
    lang = models.CharField(max_length=20)
    heading = models.CharField(max_length=60)   
    text = models.CharField(max_length=255)
    subheading = models.CharField(max_length=50) 
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transfer", null=True)
    def __str__(self):
        return self.heading
        

class ListTransferInfo(models.Model):
    list = models.ForeignKey(InfoForTransferContact, on_delete=models.CASCADE, related_name="list", null=True, blank=True)
    text = models.CharField(max_length=120)    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transfer_list_info", null=True)
    

class ImportantInfo(models.Model):
    lang = models.CharField(max_length=20)
    heading = models.CharField(max_length=60)   
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="inportant_heading", null=True)
    def __str__(self):
        return self.heading
        
    

class ListImportantInfo(models.Model):
    list = models.ForeignKey(ImportantInfo, on_delete=models.CASCADE, related_name="list", null=True, blank=True)
    text = models.CharField(max_length=120)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="list_important", null=True)
    
    
    
class TopHeadingAirTrans(models.Model):
    lang = models.CharField(max_length=20)
    subheading = models.CharField(max_length=60)   
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="air_heading", null=True)
    def __str__(self):
        return self.subheading
        
    

class SectionHeadingAirTrans(models.Model):
    section = models.ForeignKey(TopHeadingAirTrans, on_delete=models.CASCADE, related_name="section", null=True, blank=True)
    text = models.CharField(max_length=120)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="section", null=True)



class TopHeadingBaggage(models.Model):
    page = models.ForeignKey('BaggagesPage', on_delete=models.CASCADE, related_name='air10',null=True, blank=True)
    lang = models.CharField(max_length=20) 
    section = models.CharField(max_length=50)
    page = models.CharField(max_length=40)   
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="top_baggages", null=True)
    def __str__(self):
        return self.page
        

class BaggageRowBox(models.Model):
    page = models.ForeignKey('BaggagesPage', on_delete=models.CASCADE, related_name='air11',null=True, blank=True)
    lang = models.CharField(max_length=20)
    heading = models.CharField(max_length=30)
    text = models.TextField()    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="baggage_box", null=True)
    def __str__(self):
        return self.heading
        
        
        
        
        
# class BaggageDescr(models.Model):
#     page = models.ForeignKey('BaggagesPage', on_delete=models.CASCADE, related_name='air12',null=True, blank=True)
#     lang = models.CharField(max_length=20)
#     heading = models.CharField(max_length=50)
#     owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="baggage_descr", null=True)
#     def __str__(self):
#         return self.heading
    
# class Groups(models.Model):
#     page = models.ForeignKey('BaggagesPage', on_delete=models.CASCADE, related_name='air13',null=True, blank=True)
#     groups = models.ForeignKey(BaggageDescr, on_delete=models.CASCADE, related_name="groups",null=True, blank=True)
#     type = models.CharField(max_length=30)
#     note = models.CharField(max_length=50)
#     owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group", null=True)
#     def __str__(self):
#         return self.type
    
        
class HandLuggage(models.Model):
    page = models.ForeignKey('BaggagesPage', on_delete=models.CASCADE, related_name='air14',null=True, blank=True)
    text = models.CharField(max_length=80)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hand", null=True)
    def __str__(self):
        return self.text
    

class Baggage(models.Model):
    page = models.ForeignKey('BaggagesPage', on_delete=models.CASCADE, related_name='air15',null=True, blank=True)
    text = models.CharField(max_length=80)       
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="baggages", null=True)
    def __str__(self):
        return self.text
    
    
    
class TopHeadingCertificate(models.Model):
    page = models.ForeignKey('CertificatePage', on_delete=models.CASCADE, related_name='air16',null=True, blank=True)
    lang = models.CharField(max_length=20)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="top_certificate", null=True)
    
class PathCertificate(models.Model):
    page = models.ForeignKey('CertificatePage', on_delete=models.CASCADE, related_name='air17',null=True, blank=True)
    top_heading = models.ForeignKey(TopHeadingCertificate, on_delete=models.CASCADE, related_name="path",null=True, blank=True)
    label = models.CharField(max_length=100)        
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="certificate_path", null=True)
    def __str__(self):
        return self.label
    
    
    
    
class CertificateDescr(models.Model):
    page = models.ForeignKey('CertificatePage', on_delete=models.CASCADE, related_name='air18',null=True, blank=True)
    lang = models.CharField(max_length=20)  
    heading = models.CharField(max_length=40)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="certificate_descr", null=True)
    def __str__(self):
        return self.heading


class Paragraphs(models.Model):
    page = models.ForeignKey('CertificatePage', on_delete=models.CASCADE, related_name='air19',null=True, blank=True)
    certificate_descr = models.ForeignKey(CertificateDescr, on_delete=models.CASCADE, related_name="paragraphs",null=True, blank=True)
    text = models.CharField(max_length=60)    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="paragraph", null=True)
    def __str__(self):
        return self.text
    
    
    

class CertificatesImages(models.Model):
    page = models.ForeignKey('CertificatePage', on_delete=models.CASCADE, related_name='air20',null=True, blank=True)
    lang = models.CharField(max_length=20)
    heading = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="certificate_img", null=True)
    def __str__(self):
        return self.heading
    

class Image(models.Model):
    page = models.ForeignKey('CertificatePage', on_delete=models.CASCADE, related_name='air21',null=True, blank=True)
    certificates_images = models.ForeignKey(CertificatesImages, on_delete=models.CASCADE, related_name='images', null=True, blank=True)    
    image = models.FileField(
        upload_to="certificates/images/", 
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg'])]
    )    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="certificates", null=True)
    



class TopHeadingContact(models.Model):
        page = models.ForeignKey('HeadContactPage', on_delete=models.CASCADE, related_name='air22', null=True, blank=True)
        lang = models.CharField(max_length=20)
        owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="top_heading", null=True)
   
   
    
class TopHeadingPath(models.Model):
    page = models.ForeignKey('HeadContactPage', on_delete=models.CASCADE, related_name='air23',null=True, blank=True)
    top_heading = models.ForeignKey(TopHeadingContact, on_delete=models.CASCADE, related_name="path",null=True, blank=True)
    label = models.CharField(max_length=100)        
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="path", null=True)
    def __str__(self):
        return self.label    
    
    

class ContactImages(models.Model):
    page = models.ForeignKey('HeadContactPage', on_delete=models.CASCADE, related_name='air24',null=True, blank=True)
    image = models.FileField(
        upload_to="certificates/images/", 
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg'])]
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images", null=True)
    def __str__(self):
        return self.image.name 




class ContactInfo(models.Model):
    page = models.ForeignKey('HeadContactPage', on_delete=models.CASCADE, related_name='air25',null=True, blank=True) 
    lang = models.CharField(max_length=20)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts", null=True)

class Contact(models.Model):
    page = models.ForeignKey('HeadContactPage', on_delete=models.CASCADE, related_name='air26',null=True, blank=True) 
    contact_info = models.ForeignKey(ContactInfo, on_delete=models.CASCADE, related_name="contact")
    label = models.CharField(max_length=40)
    value = models.CharField(max_length=80)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contact_info", null=True)
    
    def __str__(self):
        return self.value
       

class Social(models.Model):
    page = models.ForeignKey('HeadContactPage', on_delete=models.CASCADE, related_name='air27',null=True, blank=True) 
    contact_social = models.ForeignKey(ContactInfo, on_delete=models.CASCADE, related_name="social",null=True, blank=True)     
    name = models.CharField( max_length=30) 
    url = models.URLField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="social_contact", null=True)
    def __str__(self):
        return self.name
    
class SupportText(models.Model):
    page = models.ForeignKey('HeadContactPage', on_delete=models.CASCADE, related_name='air28',null=True, blank=True)
    contact_support = models.ForeignKey(ContactInfo, on_delete=models.CASCADE, related_name="support_text",null=True, blank=True) 
    text = models.CharField(max_length=80)      
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="support", null=True)
    def __str__(self):
        return self.text
    
    
    

   
   
   
class SeatChoiceDescription(models.Model):
    page = models.ForeignKey('SeatChoicePage', on_delete=models.CASCADE, related_name='air50',null=True, blank=True)   
    lang = models.CharField(max_length=20)
    heading = models.CharField(max_length=60) 
    description = models.CharField(max_length=70, default='description') 
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="descr", null=True)
    def __str__(self):
        return self.heading
    
    
    
    
class TopHeadingSeatChoice(models.Model):   
    page10 = models.ForeignKey('SeatChoicePage', on_delete=models.CASCADE, related_name='air51',null=True, blank=True)     
    lang = models.CharField(max_length=20)
    section = models.CharField(max_length=60) 
    page = models.CharField(max_length=70)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seatchoice", null=True)
    def __str__(self):
        return self.page
    
    
    

class SeatChoicePrice(models.Model):  
    page = models.ForeignKey('SeatChoicePage', on_delete=models.CASCADE, related_name='air52',null=True, blank=True)      
    lang = models.CharField(max_length=20)
    heading = models.CharField(max_length=60) 
    description = models.CharField(max_length=70, default='description') 
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="price", null=True)
    def __str__(self):
        return self.heading
    

   




class BookingResultsPageLabel(models.Model):
    lang= models.CharField(max_length=20)
    navigation= models.CharField(max_length=120)
    hours_mins_text= models.CharField(max_length=220)
    transit_text= models.CharField(max_length=250)
    select_btn_text= models.CharField(max_length=120)
    selected_btn_text= models.CharField(max_length=120)
    continue_btn_text= models.CharField(max_length=120)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="booking_results", null=True)
    def __str__(self):
       return self.navigation
   

class BookingNavigation(models.Model):
    lang = models.CharField(max_length=20)
    title = models.CharField(max_length=120)
    section_number = models.IntegerField(default=1)     
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="navigation", null=True)
    def __str__(self):
       return self.title
   
   

class OrderSummary(models.Model):
    lang =  models.CharField(max_length=20)
    btn_text = models.CharField(max_length=100, default="countinue/pay")
    title = models.CharField(max_length=120)
    sub_total_text_field= models.CharField(max_length=120)
    quantity_text_field = models.CharField(max_length=120)
    seat_text_field = models.CharField(max_length=100)
    total_text_field= models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_sum", null=True)
    
    def __str__(self):
       return self.title
   
   

   


class BookingClientInfoPageLabel(models.Model):
    lang = models.CharField(max_length=20)
    passanger_types = models.CharField(max_length=120)
    order_data_title = models.CharField(max_length=120)
    visitor_details_title = models.CharField(max_length=120)
    seat_title = models.CharField(max_length=120)
    phone_text_field = models.CharField(max_length=120)
    email_text_field = models.CharField(max_length=120)
    baggage_airport_info = models.TextField(default="լրացուցիչ տեղեկությունների")
    title_text_field =  models.CharField(max_length=120)
    title_select = models.CharField(max_length=120)
    full_name_text_field = models.CharField(max_length=120)
    birth_text_field = models.CharField(max_length=120)
    citizenship_text_field = models.CharField(max_length=120)
    passport_text_field = models.CharField(max_length=120)
    passport_validity_period_field = models.CharField(max_length=120, default="The passport is valid until")
    select_btn_text = models.CharField(max_length=120)
    selected_btn_text =  models.CharField(max_length=120)  
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="client_info", null=True)
    
    
    def __str__(self):
       return f"{self.full_name_text_field} {self.citizenship_text_field}"
   
   
class BookingPaymentPageLabel(models.Model):
    lang = models.CharField(max_length=20)
    title = models.CharField(max_length=120)
    credit_card_text = models.CharField(max_length=120)
    privacy_notice_text = models.TextField()   
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pyment_info", null=True)
    
    def __str__(self):
       return f"{self.title} {self.credit_card_text}"
   
   
   
   
   
   
#    nor

class AboutUsTopHeading(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="top", null=True)
    lang = models.CharField(max_length=15)
    section = models.CharField(max_length=60)
    page = models.CharField(max_length=60)   
    
    def __str__(self):
       return f"{self.section} {self.page}"
   
   
class AboutUsDescr(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="aboutus_descriptions", null=True)
    lang = models.CharField(max_length=15)
    title = models.CharField(max_length=60)
    descr = models.TextField()
    
    def __str__(self):
       return f"{self.title} {self.descr}"
   
   
class ContactIntro(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="intro", null=True)
    lang = models.CharField(max_length=15)
    title = models.CharField(max_length=60)
    img_url = models.CharField(max_length=120)
    
    def __str__(self):
        return f"{self.title} {self.lang}"
    
    

class TopContact(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="topContact", null=True)
    lang = models.CharField(max_length=15)
    section = models.CharField(max_length=60)
    page = models.CharField(max_length=120)
    
    def __str__(self):
        return f"{self.lang} {self.page}"
        
    
       
class ContactNewInfo(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="new_info", null=True)
    lang = models.CharField(max_length=15)
    title = models.CharField(max_length=60)
    descr = models.TextField()
    img_url = models.CharField(max_length=120)
    
    def __str__(self):
        return f"{self.title} {self.lang}"
    
    
class ContactMap(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="map", null=True)
    url = models.URLField()
    
    def __str__(self):
        return f"{self.title} {self.lang}"    