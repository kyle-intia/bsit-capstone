from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password2')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email",)

# Pre-Assessment   

class TransportationForm(forms.Form):
    vehicle_km = forms.ChoiceField(
        choices=[
            ('<5000', 'Less than 5,000 km'),
            ('5000-10000', '5,000–10,000 km'),
            ('10000-15000', '10,000–15,000 km'),
            ('>15000', 'More than 15,000 km'),
        ],
        required=True,
        label='About your personal vehicle use',
    )
    commute_modes = forms.MultipleChoiceField(
        choices=[
            ('walking', 'Walking'),
            ('bicycle', 'Bicycle'),
            ('jeepney_bus', 'Jeepney/Bus'),
            ('train', 'Train (MRT/LRT)'),
            ('motorcycle', 'Motorcycle'),
            ('private_car', 'Private Car'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='How do you usually commute on a daily basis? (Choose all that apply)',
    )
    travel_days = forms.ChoiceField(
        choices=[
            ('1-2', '1–2 Days'),
            ('3-4', '3–4 Days'),
            ('5+', '5 or more Days'),
        ],
        widget=forms.RadioSelect,
        required=True,
        label='How many days a week do you travel for school/work?',
    )