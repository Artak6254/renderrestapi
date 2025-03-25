from rest_framework import serializers
from .models import (
    Logo, Navbars, SubnavbarsList, HomepageBookingSearch,
    CalendarFieldList,PassangerFieldList,
    HomePageIntro, HomePageWhyChooseUs, ReasonsList, 
    HomePageFaq, HomePageQuestion, Footer, FooterLinks, FooterSocial
)

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

class LogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logo
        fields = "__all__"

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
         fields = ['id','lang', 'adult_title', 'adult_descr', 'child_text', 'child_descr', 'btn_text'] 

class BookingSearchSerializer(serializers.ModelSerializer):
    calendar_field_list = CalendarFieldListSerializer(many=True, required=False)  
    passangers_field_list = PassangerFieldListSerializer(many=True, required=False)  # Added this line

    class Meta:
        model = HomepageBookingSearch
        fields = ['id','lang', 'from_field_text', 'to_field_text', 'date_field_text', 'calendar_field_list', 'passangers_field_list']

    def create(self, validated_data):
        calendar_data = validated_data.pop('calendar_field_list', [])
        passangers_data = validated_data.pop('passangers_field_list', [])  # Extract passangers data

        booking_search = HomepageBookingSearch.objects.create(**validated_data)

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
          field = ['id', 'lang', 'title', 'url']

class FooterSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterSocial
        field = ['id', 'lang', 'title', 'url']         

class FooterSerializer(serializers.ModelSerializer):
    links = FooterLinksSerializer(many=True, required=False)  
    social = FooterSocialSerializer(many=True, required=False)  # Added this line

    class Meta:
        model = Footer
        fields = ['id', 'lang','links', 'social'] 
        
        def create(self, validated_data):
            links_data = validated_data.pop('links', [])
            social_data = validated_data.pop('social', [])  # Extract passangers data

            footer_data = Footer.objects.create(**validated_data)

            for link in links_data:
                FooterLinks.objects.create(footer_links=footer_data, **link)  # Ensure correct ForeignKey

            for social in social_data:
                FooterSocial.objects.create(footer_social=footer_data, **social)  # Ensure correct ForeignKey

            return footer_data