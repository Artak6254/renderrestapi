from rest_framework import serializers
import re
from django.db import transaction
from .models import (
    LanguageList,Logo, Navbars, SubnavbarsList, HomepageBookingSearch,
    CalendarFieldList,PassangerFieldList,
    HomePageIntro, HomePageWhyChooseUs, ReasonsList, 
    HomePageFaq, HomePageQuestion, Footer, FooterLinks, FooterSocial,
    Flights, FlightSeats, Passengers, Tickets,PassangersCount,FlightDirection,
    AirTransContact, ListAirContact, InfoForTransferContact,ListTransferInfo,
    ImportantInfo,ListImportantInfo,TopHeadingAirTrans,SectionHeadingAirTrans,
    TopHeadingBaggage, BaggageRowBox,HandLuggage,
    Baggage,TopHeadingCertificate,PathCertificate,CertificateDescr,
    Paragraphs, CertificatesImages, Image, TopHeadingContact, TopHeadingPath,
    ContactImages,ContactInfo, Contact,SeatChoiceDescription,
    TopHeadingSeatChoice,SeatChoicePrice,Social,SupportText,
    BookingResultsPageLabel ,BookingNavigation, OrderSummary, BookingClientInfoPageLabel,
    BookingPaymentPageLabel,SoldFlightArchive,AboutUsTopHeading,AboutUsDescr,ContactIntro,
    TopContact,ContactNewInfo,ContactMap
)

class LanguageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageList
        fields = '__all__'

class SubnavbarsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubnavbarsList
        fields = ['id', 'lang', 'title', 'url']

class NavbarsSerializer(serializers.ModelSerializer):
    subnavbar_list = SubnavbarsListSerializer(many=True, required=False)

    class Meta:
        model = Navbars
        fields = ['id', 'lang', 'title', 'subnavbar_list']  

    def create(self, validated_data):
        subnavbars_data = validated_data.pop('subnavbar_list', [])
        navbar = Navbars.objects.create(**validated_data)

        for subnav_data in subnavbars_data:
            SubnavbarsList.objects.create(navbar=navbar, **subnav_data)

        return navbar


class SoldFlightArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoldFlightArchive
        fields = '__all__'
        
    def create(self, validated_data):
        passengers = validated_data.pop("passengers_data", [])
        enriched_passengers = []

        default_ticket_number = validated_data.get("ticket_number")
        default_ticket_type = validated_data.get("ticket_type")
        ticket_is_sold = validated_data.get("ticket_is_sold", True)

        for p in passengers:
            p.setdefault("ticket_number", default_ticket_number)
            p.setdefault("ticket_type", default_ticket_type)
            p.setdefault("ticket_is_sold", ticket_is_sold)
            enriched_passengers.append(p)

        validated_data["passengers_data"] = enriched_passengers
        return super().create(validated_data)
        
        
class LogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logo
        fields = ['id', 'logo', 'owner']

class HomePageIntroSerializer(serializers.ModelSerializer):

    class Meta:
        model = HomePageIntro
        fields = '__all__'

class CalendarFieldListSerializer(serializers.ModelSerializer):  
    class Meta:
        model = CalendarFieldList
        fields = ['id','lang', 'departure_field_text', 'return_field_text', 'btn_text', 'one_way_ticket_btn_text'] 

class PassangerFieldListSerializer(serializers.ModelSerializer):
      class Meta:
         model = PassangerFieldList 
         fields = ['id','lang', 'adult_title', 'adult_descr', 'child_text', 'child_descr', 'baby_title','baby_descr', 'btn_text'] 



class BookingSearchSerializer(serializers.ModelSerializer):
    calendar_field_list = CalendarFieldListSerializer(many=True, required=False)  
    passangers_field_list = PassangerFieldListSerializer(many=True, required=False)  # Added this line

    class Meta:
        model = HomepageBookingSearch
        fields = '__all__'

    def create(self, validated_data):
        calendar_data = validated_data.pop('calendar_field_list', [])
        passangers_data = validated_data.pop('passangers_field_list', [])  # Extract passangers data
            
        booking_search = HomepageBookingSearch.objects.create(**validated_data)
        print(passangers_data)
        for calendar in calendar_data:
            CalendarFieldList.objects.create(booking_search_calendar=booking_search, **calendar)  # Ensure correct ForeignKey

        for passenger in passangers_data:
            PassangerFieldList.objects.create(booking_search_passangers=booking_search, **passenger)  # Ensure correct ForeignKey

        return booking_search





class ReasonsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReasonsList
        fields = ['id', 'lang', 'title', 'descr']

class HomePageWhyChooseUsSerializer(serializers.ModelSerializer):
    reasons_list = ReasonsListSerializer(many=True, required=False, source="why_choose_reasons")  

    class Meta:
        model = HomePageWhyChooseUs
        fields = ['id', 'lang', 'title', 'sub_title', 'image', 'map_image', 'reasons_list']

    def get_image(self, obj):
        # Մատուցում է լրիվ URL-ը
        return obj.image.url

    def get_map_image(self, obj):
        # Մատուցում է լրիվ URL-ը
            return obj.map_image.url
        
    def create(self, validated_data):
        # Ստանում ենք reasonsList-ը request-ից
        reasons_data = self.initial_data.get('reasonsList', [])  
        homepage_instance = HomePageWhyChooseUs.objects.create(**validated_data)

        # Ավելացնում ենք reasonsList-ի տվյալները
        for reason_data in reasons_data:
            ReasonsList.objects.create(homepage_why_choose_us=homepage_instance, **reason_data)

        return homepage_instance

class HomePageQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomePageQuestion
        fields = ['id', 'lang', 'question', 'answer']

class HomePageFaqSerializer(serializers.ModelSerializer):
    question_list = HomePageQuestionSerializer(many=True, required=False)

    class Meta:
        model = HomePageFaq
        fields = ['lang', 'title', 'question_list']  # Remove 'question' and 'answer'

    def create(self, validated_data):
        question_list_data = validated_data.pop('question_list', [])
        homepage_faq = HomePageFaq.objects.create(**validated_data)

        for question_data in question_list_data:
            HomePageQuestion.objects.create(faq=homepage_faq, **question_data)  # Fix the field reference

        return homepage_faq



class FooterLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterLinks
        fields = ['id', 'lang', 'title', 'url']  # Fixed 'field' -> 'fields'

class FooterSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterSocial
        fields = ['id', 'lang', 'title', 'url']  # Fixed 'field' -> 'fields'

class FooterSerializer(serializers.ModelSerializer):
    links = FooterLinksSerializer(many=True, required=False)  
    social = FooterSocialSerializer(many=True, required=False)

    class Meta:
        model = Footer
        fields = ['id', 'lang', 'links', 'social']  # Fixed 'field' -> 'fields'

    def create(self, validated_data):
        links_data = validated_data.pop('links', [])
        social_data = validated_data.pop('social', [])

        footer_data = Footer.objects.create(**validated_data)

        for link in links_data:
            FooterLinks.objects.create(footer_links=footer_data, **link)  

        for social in social_data:
            FooterSocial.objects.create(footer_social=footer_data, **social)  

        return footer_data
    
    
    

    
    

    
# #Booking logic    

class FlightSearchSerializer(serializers.Serializer):
    from_here = serializers.CharField()
    to_there = serializers.CharField()
    airport_name = serializers.CharField()
    ariport_short_name = serializers.CharField()
    arrival_airport_name = serializers.CharField()
    arrival_airport_short_name = serializers.CharField()
    departure_date = serializers.DateField()
    return_date = serializers.DateField(required=False, allow_null=True)
    adult_count = serializers.IntegerField()
    child_count = serializers.IntegerField()
    baby_count = serializers.IntegerField()
    
    

class FlightSeatsSerializer(serializers.ModelSerializer):
    flight_id = serializers.PrimaryKeyRelatedField(queryset=Flights.objects.all(), source='flight')

    class Meta:
        model = FlightSeats
        fields = ['id', 'flight_id',  'seat_type', 'seat_number', 'is_taken']





class PassengersSerializer(serializers.ModelSerializer):
    ticket_id = serializers.PrimaryKeyRelatedField(queryset=Tickets.objects.all())
    departure_seat_id = serializers.PrimaryKeyRelatedField(queryset=FlightSeats.objects.all(), required=False, allow_null=True)
    return_seat_id = serializers.PrimaryKeyRelatedField(queryset=FlightSeats.objects.all(), required=False, allow_null=True)
    passport_serial = serializers.CharField(required=False, allow_null=True)
    passport_validity_period = serializers.CharField(required=False, allow_null=True)
    departure_baggage_weight = serializers.CharField(required=False, allow_null=True)
    return_baggage_weight = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Passengers
        fields = '__all__'
        
    # def validate(self, data):
    #     passport_serial = data.get('passport_serial')
    #     citizenship = data.get('citizenship')

    #     PASSPORT_REGEXES = {
    #         "Armenian": r"^[A-Z]{2}\d{6,7}$",
    #         "Russian": r"^\d{10}$",
    #         "USA": r"^\d{9}$",
    #         "British": r"^\d{9}$",
    #         "French": r"^\d{2}[A-Z]{2}\d{5}$"
    #     }

    #     pattern = PASSPORT_REGEXES.get(citizenship)
    #     if pattern and not re.fullmatch(pattern, passport_serial):
    #         raise serializers.ValidationError({
    #             'passport_serial': f"Անվավեր անձնագրի ձևաչափ `{citizenship}` երկրի համար։"
    #         })

    #     return data  

    
       

class TicketsSerializer(serializers.ModelSerializer):
    passengers = PassengersSerializer(many=True)
    ticket_number = serializers.ReadOnlyField() 

    class Meta:
        model = Tickets
        fields = '__all__'







class FlightsSerializer(serializers.ModelSerializer):
    tickets = TicketsSerializer(many=True, read_only=True)  # related_name="tickets"
    flight_seats = FlightSeatsSerializer(many=True, read_only=True)  # related_name="flight_seats"
    available_departure_seats = serializers.SerializerMethodField()
    available_return_seats = serializers.SerializerMethodField()

    class Meta:
        model = Flights
        fields = '__all__'

    def get_available_departure_seats(self, obj):
        return obj.available_departure_seats()

    def get_available_return_seats(self, obj):
        return obj.available_return_seats()
    
    

class PassangersCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassangersCount
        fields = '__all__'    
        
        
class FromHereSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    from_here = serializers.CharField()
    flight_airport_name = serializers.CharField()
    flight_airport_short_name = serializers.CharField()

class ToThereSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    to_there = serializers.CharField()
    arrival_airport_name = serializers.CharField()
    arrival_airport_short_name = serializers.CharField()
    
    
class FlightDirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightDirection
        fields = '__all__'            
        
        
        
        
        
# Static Pages         


class ListAirContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListAirContact
        fields = ['id', 'text']

class AirTransContactSerializer(serializers.ModelSerializer):
    list = ListAirContactSerializer(many=True, read_only=True)

    class Meta:
        model = AirTransContact
        fields = ['lang', 'heading', 'text', 'subheading', 'list']
        
        
        
        



class ListTransferInfoSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = ListTransferInfo
        fields = [ 'text'] 
             


class InfoForTransferContactSerializer(serializers.ModelSerializer):
    list = ListTransferInfoSerializer(many=True, read_only=True )  
    class Meta:
        model = InfoForTransferContact
        fields = ['lang', 'heading', 'text', 'subheading', 'list']        
        
        

class ListImportantInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListImportantInfo
        fields = ['id', 'text']
        

class ImportantInfoSerializer(serializers.ModelSerializer):
    list = ListImportantInfoSerializer(many=True, read_only=True)

    class Meta:
        model = ImportantInfo
        fields = ['lang', 'heading', 'list']        
           
           

class SectionHeadingAirTransSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionHeadingAirTrans
        fields = ['id', 'text']

class TopHeadingAirTransSerializer(serializers.ModelSerializer):
    sections = SectionHeadingAirTransSerializer(source='section', many=True, read_only=True)
    class Meta:
        model = TopHeadingAirTrans
        fields = ['lang', 'subheading', 'sections']           
        


class TopHeadingBaggageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopHeadingBaggage
        fields = ['lang', 'section', 'page']       
        
class BaggageBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaggageRowBox
        fields = ['lang', 'heading', 'text']              
        
        
        

class HandLuggageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HandLuggage
        fields = ['id', 'text']

class BaggageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Baggage
        fields = ['id', 'text']


        
        
class PathCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PathCertificate
        fields = ['id', 'label']

class TopHeadingCertificateSerializer(serializers.ModelSerializer):
    path = PathCertificateSerializer(many=True, read_only=True)

    class Meta:
        model = TopHeadingCertificate
        fields = ['lang', 'path']        
        
    
    
        
class ParagraphsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paragraphs
        fields = ['id', 'text']

class CertificateDescrSerializer(serializers.ModelSerializer):
    paragraphs = ParagraphsSerializer(many=True, read_only=True)

    class Meta:
        model = CertificateDescr
        fields = ['lang', 'heading', 'paragraphs'] 
        
        
        
        
class ImageSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['id', 'src']

    def get_src(self, obj):
        request = self.context.get('request')  # վերցնում ենք request context-ից
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        elif obj.image:
            return obj.image.url  # fallback
        return None
    
class CertificatesImagesSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = CertificatesImages
        fields = ['lang', 'heading', 'images']    
    

        
class TopHeadingPathSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopHeadingPath
        fields = ['id', 'label']
        

class TopHeadingContactSerializer(serializers.ModelSerializer):
    path = TopHeadingPathSerializer(many=True, read_only=True)

    class Meta:
        model = TopHeadingContact
        fields = ['lang', 'path']
        

class ContactImagesSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ContactImages
        fields = [ 'image']

    def get_image(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url                        
    
    
    
    
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'label', 'value']


class SocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Social
        fields = ['id', 'name', 'url']


class SupportTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportText
        fields = ['id', 'text']


class ContactInfoSerializer(serializers.ModelSerializer):
    contact = ContactSerializer(many=True, read_only=True)
    social = SocialSerializer(many=True, read_only=True)
    support_text = SupportTextSerializer(many=True, read_only=True)

    class Meta:
        model = ContactInfo
        fields = ['id', 'lang', 'contact', 'social', 'support_text']  
        
        
        

        
        
       
        
        
        
class SeatChoiceDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatChoiceDescription  # ✅ սա է ճիշտը
        fields = ['id', 'lang', 'heading', 'description']
        
        
     

class TopHeadingSeatChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopHeadingSeatChoice
        fields = ['id', 'lang', 'section', 'page']
        
        
     
        
class SeatChoicePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatChoicePrice
        fields = ['id', 'lang', 'heading', 'description']     
        
        
        
    
       
        




class BookingResultsPageLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingResultsPageLabel
        fields = '__all__'

class BookingNavigationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingNavigation
        fields = '__all__'
        

class OrderSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderSummary
        fields = '__all__'        
                               

class BookingClientInfoPageLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingClientInfoPageLabel
        fields = '__all__'        
         
                                                                   

                                                                                                  

class BookingPaymentPageLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingPaymentPageLabel
        fields = '__all__'        
                                 
                                 
             
class AboutUsTopHeadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUsTopHeading
        fields = '__all__'
        
class AboutUsDescrSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUsDescr
        fields = '__all__'        
        
class ContactIntroSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactIntro
        fields = '__all__'    
        
class TopContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopContact
        fields = '__all__'    
        
class ContactNewInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactNewInfo
        fields = '__all__'   

class ContactMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMap
        fields = '__all__'                                                        
                                                                                                