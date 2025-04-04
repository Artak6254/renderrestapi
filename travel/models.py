from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator



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

class Booking(models.Model):
    booking_flights = models.ForeignKey('BookingFlights', on_delete=models.CASCADE, related_name='bookings')
    bort_number = models.CharField(max_length=100)
    from_here = models.CharField(max_length=120)
    to_there = models.CharField(max_length=120)
    adult_count = models.CharField(max_length=50)
    child_count = models.CharField(max_length=50)
    baby_count = models.CharField(max_length=50)
    price = models.CharField(max_length=90)

    def __str__(self):
        return f" {self.id} {self.from_here} {self.to_there}"


class BookingPassengers(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='passengers')
    seat_number = models.CharField(max_length=60)
    departure_baggage_weight = models.CharField(max_length=80)
    return_baggage_weight = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.booking.id} {self.seat_number}"


class BookingFlights(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='flight_details')
    checkin_date = models.CharField(max_length=150)
    checkout_date = models.CharField(max_length=150)
    checkin_time = models.CharField(max_length=150)
    checkout_time = models.CharField(max_length=150)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.booking.id}: {self.checkin_date} {self.checkout_date}"
    



    