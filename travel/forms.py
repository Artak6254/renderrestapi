from django import forms
from .models import Passengers
import re





COUNTRIES = [
    ("Armenian", "Armenian"),
    ("Russian", "Russian"),
    ("USA", "USA"),
    ("British", "British"),
    ("French", "French"),
]

class PassengersAdminForm(forms.ModelForm):
    citizenship = forms.ChoiceField(choices=COUNTRIES)  # Ահա սա փոխում ենք

    class Meta:
        model = Passengers
        fields = '__all__'

    def clean_passport_serial(self):
        passport_serial = self.cleaned_data.get('passport_serial')
        citizenship = self.cleaned_data.get('citizenship')

        PASSPORT_REGEXES = {
            "Armenian": r"^[A-Z]{2}\d{6,7}$",
            "Russian": r"^\d{10}$",
            "USA": r"^\d{9}$",
            "British": r"^\d{9}$",
            "French": r"^\d{2}[A-Z]{2}\d{5}$"
        }

        pattern = PASSPORT_REGEXES.get(citizenship)
        if pattern and passport_serial and not re.fullmatch(pattern, passport_serial):
            raise forms.ValidationError(
                f"Անվավեր անձնագրի ձևաչափ `{citizenship}` երկրի համար։"
            )

        return passport_serial


class BookingTicketsSearchForm(forms.Form):
    from_here = forms.CharField(label="Սկզբնակետ", required=True)
    to_there = forms.CharField(label="Վերջնակետ", required=True)
    departure_date_start = forms.DateField(label="Մեկնելու ամսաթիվ (սկիզբ)", required=True)
    departure_date_end = forms.DateField(label="Մեկնելու ամսաթիվ (վերջ)", required=True)
    return_date_start = forms.DateField(label="Վերադարձի ամսաթիվ (սկիզբ)", required=False)
    return_date_end = forms.DateField(label="Վերադարձի ամսաթիվ (վերջ)", required=False)
    is_round_trip = forms.BooleanField(label="Երկկողմանի է", required=False)
    adult_count = forms.IntegerField(label="Մեծահասակներ", min_value=0, initial=1)
    child_count = forms.IntegerField(label="Երեխաներ", min_value=0, initial=0)
    baby_count = forms.IntegerField(label="Մանկահասակներ", min_value=0, initial=0)