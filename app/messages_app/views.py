from django.shortcuts import redirect, render
from .forms import MessageForm
from django.views.generic import View, DetailView
from .models import Message
from projects.views import is_admin
from django.contrib.auth.decorators import user_passes_test
from mail_service.views import we_got_new_message


def contact(request):
    if request.method == 'POST':
        form = MessageForm(data=request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.save()
            we_got_new_message()
            return redirect("messages_app:thanks")
    else:
        form = MessageForm()
        return render(request, "messages_app/contact.html", {"form": form})


class MessageView(View):
    def post(self, request, *args, **kwargs):
        form = MessageForm(data=request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.save()
        return redirect("messages_app:thanks")

    def get(self, request, *args, **kwargs):
        form = MessageForm()
        return render(request, "messages_app/message_form.html", {"form": form})


class MessageDetailView(DetailView):
    model = Message
    template_name = "messages_app/read_message.html"
    context_object_name = 'message'

    def test_func(self):
        return self.request.user.is_superuser


@user_passes_test(is_admin)
def set_message_read(request, message_id):
    try:
        message = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
        message = None

    if message is not None:
        message.status = Message.Status.ANSWERED
        message.save()
    return redirect("accounts:dashboard")


def say_thanks_for_cantact_us(request):
    return render(request, "messages_app/thank_you.html")
