from .models import OurProjects
from django import forms


class ProjectsForm(forms.ModelForm):  # Corrected the class name
    class Meta:
        model = OurProjects
        fields = ["image", "title"]
        widgets = {
            'title': forms.Select(attrs={"class": "form-control"}, choices=OurProjects.TitleChoices.choices),
        }
