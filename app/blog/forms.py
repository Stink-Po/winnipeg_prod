from django import forms
from .models import Post
from accounts.models import CustomUser


class SearchForm(forms.Form):
    query = forms.CharField()


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['slug', 'publish']

    widgets = {

        'title': forms.TextInput(),
        'image': forms.ImageField(),
        'author': forms.ModelChoiceField(
            queryset=CustomUser.objects.all(),  # Provide the queryset for the CustomUser model
            widget=forms.Select()
        ),


    }
    status = forms.ChoiceField(choices=Post.Status.choices, widget=forms.Select())
