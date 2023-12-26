from django.urls import path
from .views import contact, MessageView, MessageDetailView, set_message_read, say_thanks_for_cantact_us

app_name = 'messages_app'

urlpatterns = [
    path('send_message/', MessageView.as_view(), name='send_message'),
    path('contact/', contact, name="contact"),
    path("read-messages/<int:pk>/", MessageDetailView.as_view(), name="read_messages"),
    path("is_read/<int:message_id>/", set_message_read, name="is_read"),
    path("thank-you/", say_thanks_for_cantact_us, name="thanks"),
]
