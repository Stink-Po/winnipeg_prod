from django.shortcuts import render, redirect
from .forms import ProjectsForm
from django.contrib.auth.decorators import user_passes_test


def is_admin(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_admin)
def add_project(request):
    project_form = ProjectsForm
    if request.method == "POST":
        project_form = ProjectsForm(request.POST, request.FILES)
        if project_form.is_valid():
            project_form.save()
            return redirect("accounts:dashboard")
    return render(request, "projects/add_project_form.html", {"project_form": project_form})
