from django.shortcuts import render
from messages_app.forms import MessageForm
from django.views.generic import View
from projects.models import OurProjects
from services.forms import UsersServicesForm, OurServicesForm
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator


@csrf_protect
def index(request):
    all_projects = OurProjects.objects.all()
    if request.user.is_authenticated:
        service_form = UsersServicesForm()
    else:
        service_form = OurServicesForm()
    form = MessageForm()
    return render(request, template_name="pages/index.html", context={
        "form": form,
        "service_form": service_form,
        "projects": all_projects,
    }
                  )


@method_decorator(csrf_protect, name='dispatch')
class DuctCleaning(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            service_form = UsersServicesForm
        else:
            service_form = OurServicesForm
        return render(request, "pages/duct_cleaning.html", {"service_form": service_form})


@method_decorator(csrf_protect, name='dispatch')
class FurnaceCleaning(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            service_form = UsersServicesForm
        else:
            service_form = OurServicesForm

        return render(request, "pages/furnace cleaning.html", {"service_form": service_form})


@method_decorator(csrf_protect, name='dispatch')
class AirConditionerInstallation(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            service_form = UsersServicesForm
        else:
            service_form = OurServicesForm

        return render(request, "pages/Air_Conditioner_Installation.html", {"service_form": service_form})


@method_decorator(csrf_protect, name='dispatch')
class AirConditionerRepair(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            service_form = UsersServicesForm
        else:
            service_form = OurServicesForm

        return render(request, "pages/Air_Conditioner_Tune_Up.html", {"service_form": service_form}, )


@method_decorator(csrf_protect, name='dispatch')
class FurnaceInstallation(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            service_form = UsersServicesForm
        else:
            service_form = OurServicesForm
        return render(request, "pages/furnace_installation.html", {"service_form": service_form})


@method_decorator(csrf_protect, name='dispatch')
class FurnaceRepair(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            service_form = UsersServicesForm
        else:
            service_form = OurServicesForm
        return render(request, "pages/furnace_repair.html", {"service_form": service_form})


@method_decorator(csrf_protect, name='dispatch')
class ServicesView(View):
    def get(self, requset, *args, **kwargs):
        if requset.user.is_authenticated:
            service_form = UsersServicesForm()
        else:
            service_form = OurServicesForm()
        return render(requset, "pages/services.html", {"service_form": service_form})


class AboutView(View):
    def get(self, requset, *args, **kwargs):
        return render(requset, "pages/about.html")


def handler404_view(request, exception):
    return render(request, 'pages/404.html', status=404)


def handler500_view(request):
    return render(request, 'pages/500.html', status=500)
