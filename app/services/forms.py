from django import forms
from .models import OurServices


class OurServicesForm(forms.ModelForm):
    class Meta:
        model = OurServices
        fields = ('service', 'name', 'phone', 'email', 'message')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = OurServices.ServicesChoice.choices
        self.fields['service'].widget = forms.Select(choices=choices, attrs={"class": "form-select"})
        self.fields['message'].required = False


class UsersServicesForm(forms.ModelForm):
    class Meta:
        model = OurServices
        fields = ("service", "message")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = OurServices.ServicesChoice.choices
        self.fields['service'].widget = forms.Select(choices=choices, attrs={"class": "form-select"})
        self.fields['message'].required = False
