from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + (
            "email", "address", "phone", "first_name", "last_name")


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class EditInformationForm(CustomUserChangeForm):
    class Meta(CustomUserChangeForm.Meta):
        fields = ("email", "address", "first_name", "last_name", "phone")

    def __init__(self, *args, **kwargs):
        super(EditInformationForm, self).__init__(*args, **kwargs)
        self.fields.pop('password', None)
        self.fields["email"].required = False
        self.fields["first_name"].required = False
        self.fields["last_name"].required = False
        self.fields["phone"].required = False
        self.fields["address"].required = False


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()
