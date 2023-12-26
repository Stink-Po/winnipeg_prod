from django.urls import path
from .views import add_project

app_name = "projects"

urlpatterns = [
    path("add_project/", add_project, name="add_project"),
]