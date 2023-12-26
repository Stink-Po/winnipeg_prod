from django import forms
from .models import SiteOffers


class CustomDateTimeInput(forms.DateTimeInput):
    input_type = "datetime"


class OffersForm(forms.ModelForm):
    class Meta:
        model = SiteOffers
        exclude = ['slug', 'created_at', "availability", "status"]

    widgets = {

        'title': forms.TextInput(),
        'image': forms.ImageField(),
        "description": forms.Textarea(),
    }
    available_till = forms.DateTimeField(
        label='Available Till',
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
    )
