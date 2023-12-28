from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import EmailForm
from accounts.models import CustomUser
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from projects.views import is_admin
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_protect


@csrf_protect
@user_passes_test(is_admin)
def send_email_to_all_users(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            recipient_list = CustomUser.objects.exclude(is_superuser=True).values_list("email", flat=True)
            body = form.cleaned_data['body']
            html_message = render_to_string("mail_service/send_mass_email.html", {
                "body": body,
                "subject": form.cleaned_data['subject'],
            })
            plain_message = strip_tags(html_message)
            message = EmailMultiAlternatives(
                subject=form.cleaned_data['subject'],
                from_email=settings.EMAIL_HOST_USER,
                to=recipient_list,
                body=plain_message,
            )
            message.attach_alternative(html_message, "text/html")
            message.send()

            return redirect('accounts:dashboard')  # Redirect to a success page or any other URL
    else:
        form = EmailForm()

    return render(request, 'mail_service/send_email.html', {'form': form})


def we_got_new_order():
    body = "We have New Order Check Your Admin panel"
    html_message = render_to_string("mail_service/admin_mail.html", {
        "body": body,
        "subject": "New Order On Winni Furance",
    })
    plain_message = strip_tags(html_message)
    message = EmailMultiAlternatives(
        subject="New Order On Winni Furance",
        from_email=settings.EMAIL_HOST_USER,
        to=["morteza.behnezhad@gmail.com"],
        body=plain_message,
    )
    message.attach_alternative(html_message, "text/html")
    message.send()


def we_got_new_message():
    body = "We have New Message Check Your Admin panel"
    html_message = render_to_string("mail_service/admin_mail.html", {
        "body": body,
        "subject": "New Message On Winni Furance",
    })
    plain_message = strip_tags(html_message)
    message = EmailMultiAlternatives(
        subject="New Order On Winni Furance",
        from_email=settings.EMAIL_HOST_USER,
        to=["morteza.behnezhad@gmail.com"],
        body=plain_message,
    )
    message.attach_alternative(html_message, "text/html")
    message.send()
