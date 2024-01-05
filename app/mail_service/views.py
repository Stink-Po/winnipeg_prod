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
from email.utils import formataddr
import boto3
from decouple import config

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = 'wiini'
AWS_S3_REGION_NAME = 'ca-central-1'
AWS_S3_SIGNATURE_NAME = 's3v4'
AWS_S3_FILE_OVERWRITE = False


def get_s3_favicon_url():
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_S3_REGION_NAME,
        config=boto3.session.Config(signature_version=AWS_S3_SIGNATURE_NAME)
    )

    favicon_key = 'favicon-32x32.png'

    url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': AWS_STORAGE_BUCKET_NAME, 'Key': favicon_key},
        ExpiresIn=3600,  # Set an appropriate expiration time in seconds
        HttpMethod='GET',  # Specify the HTTP method
    )

    return url


@csrf_protect
@user_passes_test(is_admin)
def send_email_to_all_users(request):
    image_url = get_s3_favicon_url()
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            recipient_list = CustomUser.objects.exclude(is_superuser=True).values_list("email", flat=True)
            body = form.cleaned_data['body']
            html_message = render_to_string("mail_service/send_mass_email.html", {
                "body": body,
                "favicon_url": image_url,
                "subject": form.cleaned_data['subject'],
            })
            plain_message = strip_tags(html_message)
            message = EmailMultiAlternatives(
                subject=form.cleaned_data['subject'],
                from_email=formataddr(("Winni furnace", settings.EMAIL_HOST_USER)),
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
    image_url = get_s3_favicon_url()
    body = "We have New Order Check Your Admin panel"
    html_message = render_to_string("mail_service/admin_mail.html", {
        "body": body,
        "favicon_url": image_url,
        "subject": "New Order On Winni Furance",
    })
    plain_message = strip_tags(html_message)
    message = EmailMultiAlternatives(
        subject="New Order On Winni Furance",
        from_email=formataddr(("Winni furnace", settings.EMAIL_HOST_USER)),
        to=["morteza.behnezhad@gmail.com"],
        body=plain_message,
    )
    message.attach_alternative(html_message, "text/html")
    message.send()


def we_got_new_message():
    image_url = get_s3_favicon_url()
    body = "We have New Message Check Your Admin panel"
    html_message = render_to_string("mail_service/admin_mail.html", {
        "body": body,
        "favicon_url": image_url,
        "subject": "New Message On Winni Furance",
    })
    plain_message = strip_tags(html_message)
    message = EmailMultiAlternatives(
        subject="New Order On Winni Furance",
        from_email=formataddr(("Winni furnace", settings.EMAIL_HOST_USER)),
        to=["morteza.behnezhad@gmail.com"],
        body=plain_message,
    )
    message.attach_alternative(html_message, "text/html")
    message.send()
