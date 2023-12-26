from django.urls import path
from .views import send_email_to_all_users

app_name = 'mail_service'

urlpatterns = [
    path("send-mass-mail/", send_email_to_all_users, name="send-mass-mail")
]