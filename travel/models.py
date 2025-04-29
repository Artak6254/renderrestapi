from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator



class LanguageList(models.Model):
    title = models.CharField(max_length=30)
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
    title_logo_image = models.FileField(upload_to="home_page_intro/images/")  # Փոխարինեք static/image-ը
    descr = models.CharField(max_length=255)
    image = models.FileField(
        upload_to="home_page_intro/images/",  # Փոխարինեք static/image-ը
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
    to_field_text = models.CharField(max_length=50)
    date_field_text = models.CharField(max_length=50)
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
    baby_title = models.CharField(max_length=255, default="")
    baby_descr = models.CharField(max_length=255, default="")
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

class Flights(models.Model): 
    is_active = models.BooleanField(default=True)
    from_here = models.CharField(max_length=120)
    to_there = models.CharField(max_length=120)
    airport_name = models.CharField(max_length=100, default="Unknown Airport")
    airport_short_name = models.CharField(max_length=100, default="Unknown short Airport")
    departure_date = models.CharField(max_length=20, default="2025-03-12")
    departure_time = models.CharField(max_length=20, default="00:00")
    arrival_time = models.CharField(max_length=20, default="00:00")
    departure_date = models.DateField(default="2025-03-12")
    return_date = models.DateField()
    return_arrival_time = models.CharField(max_length=20, default="00:00")
    bort_number = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.from_here} ➝ {self.to_there} ({self.departure_date})"

    def has_available_seats(self, required_count=1):
        """Վերադարձնում է՝ արդյոք կա գոնե N ազատ տեղ"""
        return self.flight_seats.filter(is_taken=False).count() >= required_count

    def available_departure_seats(self):
        return self.flight_seats.filter(seat_type='departure', is_taken=False).count()

    def available_return_seats(self):
        return self.flight_seats.filter(seat_type='return', is_taken=False).count()


class Tickets(models.Model):
    flight_id = models.ForeignKey(Flights, on_delete=models.CASCADE, related_name="tickets")
    is_active = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)
    adult_count = models.CharField(max_length=10, default=0)
    child_count = models.CharField(max_length=10, default=0)
    baby_count = models.CharField(max_length=10, default=0)
    departure_price = models.CharField(max_length=10, default=0)
    return_price = models.CharField(max_length=10, default=0)

    def __str__(self):
        return f"Ticket #{self.id} | Flight: {self.flight_id}"

class FlightSeats(models.Model):
    SEAT_TYPE_CHOICES = [
        ('departure', 'Departure'),
        ('return', 'Return'),
    ]

    flight = models.ForeignKey(Flights, related_name='flight_seats', on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    seat_type = models.CharField(max_length=10, choices=SEAT_TYPE_CHOICES)
    is_taken = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.flight} | {self.seat_type.upper()} Seat {self.seat_number}"

class Passengers(models.Model):
    ticket_id = models.ForeignKey(Tickets, on_delete=models.CASCADE, related_name="passengers")
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=60)
    title = models.CharField(max_length=10)
    full_name = models.CharField(max_length=100)
    date_of_birth = models.CharField(max_length=20)
    citizenship = models.CharField(max_length=30)
    passport_serial = models.CharField(max_length=60)
    departure_baggage_weight = models.CharField(max_length=20)
    return_baggage_weight = models.CharField(max_length=20)
    departure_seat = models.ForeignKey(FlightSeats, on_delete=models.CASCADE, related_name="departure_passengers")
    return_seat = models.ForeignKey(FlightSeats, on_delete=models.CASCADE, related_name="return_passengers")

    def __str__(self):
        return f"{self.full_name} ({self.passport_serial})"








    


