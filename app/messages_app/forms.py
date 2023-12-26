from .models import Message
from django import forms


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["name", "email", "phone", "address", "message"]

    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name'}),
        'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'email'}),
        'phone': forms.TextInput(attrs={'class': 'form-control', 'id': 'phone'}),
        'address': forms.TextInput(attrs={'class': 'form-control', 'id': 'address'}),
        'message': forms.Textarea(attrs={'class': 'form-control', 'id': 'message', 'rows': 5}),
    }
