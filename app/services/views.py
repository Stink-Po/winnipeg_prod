from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, reverse, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from .forms import OurServicesForm, UsersServicesForm
from .models import OurServices
from projects.views import is_admin
from django.contrib.auth.decorators import user_passes_test
from mail_service.views import we_got_new_order
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def order(request):
    if request.user.is_authenticated:
        form = UsersServicesForm()
    else:
        form = OurServicesForm()
    if request.method == "POST" and request.user.is_authenticated:
        form = UsersServicesForm(request.POST)
        if form.is_valid():
            service_code = form.cleaned_data.get("service")
            service_instance = OurServices.ServicesChoice(service_code)
            service_name = service_instance.label
            name = f"{request.user.first_name} {request.user.last_name}"
            phone = request.user.phone
            email = request.user.email
            message = form.cleaned_data.get("message")
            if not message:
                message = " "
            return redirect(reverse("services:confirm_order", kwargs={
                "service_name": service_name,
                "name": name,
                "phone": phone,
                "email": email,
                "message": message}))
    else:
        if request.method == "POST":
            form = OurServicesForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get("name")
                service_code = form.cleaned_data.get("service")
                service_instance = OurServices.ServicesChoice(service_code)
                service_name = service_instance.label
                phone = form.cleaned_data.get("phone")
                email = form.cleaned_data.get("email")
                message = form.cleaned_data.get("message")
                if not message:
                    message = " "

                return redirect(reverse("services:confirm_order", kwargs={
                    "service_name": service_name,
                    "name": name,
                    "phone": phone,
                    "email": email,
                    "message": message}))

    return render(request, "services/choice_a_service.html", {"service_form": form})


def review_order(request, service_name, name, phone, email, message=None):
    return render(request, "services/confirm_order.html", {
        "service_name": service_name,
        "name": name,
        "phone": phone,
        "email": email,
        "message": message
    })


def confirm_order(request, service_name, name, phone, email, message):
    original_service_name = service_name
    service_name = service_name.upper().replace(" ", "_")
    service_choice_value = OurServices.ServicesChoice[service_name].value
    if request.user.is_authenticated:
        is_user = True
        user = request.user
        new_order = OurServices(
            user=user,
            service=service_choice_value,
            is_user=is_user,
            name=name,
            email=email,
            message=message,
            phone=phone
        )
        new_order.save()
    else:
        is_user = False
        new_order = OurServices(
            service=service_choice_value,
            is_user=is_user,
            name=name,
            email=email,
            message=message,
            phone=phone
        )
        new_order.save()
    we_got_new_order()
    user_name = new_order.name
    current_site = Site.objects.get_current(request)
    scheme = request.scheme
    site_url = f"{scheme}://{current_site.domain}"
    html_message = render_to_string("services/say_thanks_email.html", {
        "user": user_name,
        "link": site_url,
        "order": original_service_name,
    })
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject="Thank You For Choosing Winni Furnace",
        from_email=settings.EMAIL_HOST_USER,
        to=[new_order.email],
        body=plain_message,
    )
    message.attach_alternative(html_message, "text/html")
    message.send()

    return render(request, "services/success_order.html", {"service_name": original_service_name})


@user_passes_test(is_admin)
def finish_order(request, order_id):
    user_order = OurServices.objects.get(id=order_id)
    if user_order.is_user:
        user = user_order.user
        user.score += 10
        user.save()
        user_order.finished = True
        user_order.finished_time = timezone.now()
        user_order.save()
    else:
        user_order.finished = True
        user_order.finished_time = timezone.now()
        user_order.save()

    return redirect("accounts:dashboard")


def cancel_order(request, order_id):
    user_order = OurServices.objects.get(id=order_id)
    user_order.delete()
    return redirect("accounts:dashboard")


@user_passes_test(is_admin)
def view_order_details(request, order_id):
    this_order = OurServices.objects.get(id=order_id)
    return render(request, "services/view_order.html", {"order": this_order})
