from django.db import models


class Logo(models.Model):
    logo = models.URLField()

    def __str__(self):
        return f"{self.logo}"

class Navbars(models.Model): 
    lang = models.CharField(max_length=20)
    title = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.lang} {self.title}"

class SubnavbarsList(models.Model):
    navbar = models.ForeignKey(Navbars, on_delete=models.CASCADE, related_name="subnavbar_list")  
    lang = models.CharField(max_length=20)
    title = models.CharField(max_length=120)
    url = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.lang} {self.title} {self.url}"

class HomePageIntro(models.Model):
    lang = models.CharField(max_length=20)
    title_logo_image = models.URLField()
    descr = models.CharField(max_length=255)
    image = models.URLField()

    def __str__(self):
        return f"{self.lang} {self.title_logo_iamge} {self.descr} {self.image}"

class HomepageBookingSearch(models.Model):
    lang = models.CharField(max_length=20)
    from_field_text = models.CharField(max_length=50)
    to_field_text = models.CharField(max_length=50)
    date_field_text = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.lang} {self.from_field} {self.to_field_text} {self.date_field_text}"

class CalendarFieldList(models.Model):
    booking_search_calendar = models.ForeignKey(
        HomepageBookingSearch,
        on_delete=models.CASCADE,
        related_name="calendar_field_list"
    )
    lang = models.CharField(max_length=70)
    departure_field_text = models.CharField(max_length=100)
    return_field_text = models.CharField(max_length=100)
    btn_text = models.CharField(max_length=100)
    one_way_ticket_btn_text = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.lang} {self.departure_field_text}"

class PassangerFieldList(models.Model):
    booking_search_passangers =  models.ForeignKey(HomepageBookingSearch, on_delete=models.CASCADE, related_name="passangers_field_list")  
    lang = models.CharField(max_length=70)
    adult_title = models.CharField(max_length=70)
    adult_descr = models.CharField(max_length=255)
    child_text = models.CharField(max_length=70)
    child_descr = models.CharField(max_length=255)
    baby_title = models.CharField(max_length=255)
    baby_descr = models.CharField(max_length=255)
    btn_text = models.CharField(max_length=60)
    
    def __str__(self):
        return f"{self.lang} {self.adult_title} {self.adult_descr} {self.child_text}  {self.child_descr}  {self.baby_title} {self.baby_descr} {self.btn_text}"
    
class HomePageWhyChooseUs(models.Model):
    lang = models.CharField(max_length=20)
    title = models.CharField(max_length=120)
    sub_title = models.CharField(max_length=100)
    image = models.URLField()
    map_image = models.URLField()

class ReasonsList(models.Model):
    homepage_why_choose_us = models.ForeignKey(
        HomePageWhyChooseUs, 
        on_delete=models.CASCADE, 
        related_name="why_choose_reasons"  
    )
    lang = models.CharField(max_length=20)
    title = models.CharField(max_length=120)
    descr = models.TextField()
    
    def __str__(self):
        return f"{self.lang} {self.title} {self.descr}"
    
class HomePageFaq(models.Model):
    lang = models.CharField(max_length=20)
    title = models.CharField(max_length=120)
    
    def __str__(self):
        return f"{self.lang} {self.title}"

class HomePageQuestion(models.Model):
    faq = models.ForeignKey(HomePageFaq, on_delete=models.CASCADE, related_name="question_list", null=True)  
    lang = models.CharField(max_length=20)
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.lang} {self.question} {self.answer}"
                      
class Footer(models.Model):
    lang = models.CharField(max_length=10)
    title = models.CharField(max_length=255) 
    url = models.URLField()
    
    def __str__(self):
        return f"{self.lang} {self.title} {self.url}"