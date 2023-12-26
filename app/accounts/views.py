from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings
from django.urls import reverse, reverse_lazy
from score.models import DiscountCode
from .forms import CustomUserCreationForm, EditInformationForm
from django.contrib.auth.decorators import login_required
from services.models import OurServices
from blog.forms import PostForm
from .models import CustomUser, create_referral_code
from django.contrib.auth import logout, authenticate, login
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import redirect
from projects.forms import ProjectsForm
from mail_service.forms import EmailForm
from score.forms import SearchForm
from django.contrib.sites.models import Site
from .decorator import unauthenticated_user
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from messages_app.models import Message
from offers.forms import OffersForm


@login_required
def logout_view(request):
    logout(request)
    return redirect("pages:index")


@login_required
def generate_referral_link(request):
    signup_url = reverse('accounts:signup')
    referral_link = request.build_absolute_uri(f'{signup_url}?ref={request.user.referral_code}')
    return render(request, 'refer.html', {'referral_link': referral_link})


@unauthenticated_user(template_name='accounts/unauthenticated_error.html')
def signup_view(request):
    if request.user.is_authenticated:
        return redirect("pages:index")

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Additional logic before saving the form
            referral_code = request.GET.get('ref', None)
            if referral_code:
                user_referral = CustomUser.objects.filter(referral_code__code=referral_code).first()
                if user_referral:
                    user_referral.score += 5
                    user_referral.save()
            new_user = form.save()
            if referral_code:
                new_user.have_referral = True
                new_user.save()
            user = authenticate(request, username=new_user.username, password=form.cleaned_data['password1'])
            if user:
                login(request, user)
                send_welcome_email(user)
                send_mail_function(user, request)
                return render(request, 'accounts/send_confirmation_email.html', {"user": user})
            # Redirect to the success URL
            else:
                return redirect("pages:index")
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/signup.html", {'form': form})


@login_required
def dashboard(request):
    offer_form = None
    messages = None
    search_form = None
    email_form = None
    project_form = None
    all_user_codes = DiscountCode.objects.filter(user=request.user).all()
    signup_url = reverse('accounts:signup')
    referral_link = request.build_absolute_uri(f'{signup_url}?ref={request.user.referral_code}')
    form = None
    all_services = None
    if request.user.is_staff:
        offer_form = OffersForm()
        messages = Message.objects.filter(status=Message.Status.NEW).all()
        search_form = SearchForm()
        email_form = EmailForm()
        project_form = ProjectsForm()
        form = PostForm()
        all_services = OurServices.objects.filter(finished=False)
    user_services = OurServices.objects.filter(user=request.user)
    return render(request,
                  'accounts/test_dashboard.html',
                  {
                      'section': 'dashboard',
                      "user_services": user_services,
                      "all_services": all_services,
                      "form": form,
                      "referral_link": referral_link,
                      "project_form": project_form,
                      "discount_codes": all_user_codes,
                      "email_form": email_form,
                      "search_form": search_form,
                      "messages": messages,
                      "offer_form": offer_form,
                  })


@login_required
def edit_account_information(request):
    user = request.user
    form = EditInformationForm()
    if request.method == "POST":
        form = EditInformationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()

            return redirect("accounts:dashboard")
        form = EditInformationForm(instance=user)
    return render(request, "accounts/edit-account.html", {"form": form})


@login_required
def delete_account(request):
    user = request.user
    user.delete()
    return redirect('pages:index')


@login_required
def confirm_delete_account(request):
    return render(request, 'accounts/confirm_delete_account.html')


@login_required
def send_confirmation_email(request, user_id):
    user = CustomUser.objects.get(pk=user_id)
    send_mail_function(user, request)
    return render(request, 'accounts/send_confirmation_email.html', {"user": user})


def confirm_email(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist) as e:
        print(f"Error during confirmation: {e}")
        user = None
    if not user.email_confirmed:
        if user is not None and default_token_generator.check_token(user, token):
            if user.have_referral:
                user.email_confirmed = True
                user.score += 10
                user.save()
                create_referral_code(user)
            else:
                user.email_confirmed = True
                user.score += 5
                user.save()
                create_referral_code(user)
            return redirect("accounts:dashboard")
        else:
            return render(request, "accounts/confirm_error.html", {
                "user": user,
                "message": "There was an Error When we Try to Confirm Your Email Address Please Request a New Email "
                           "Conformation Email With The button Bellow"
            })
    else:
        return render(request, "accounts/confirm_error.html", {
            "user": user,
            "message": "Email Already is confirmed",
        })


def send_mail_function(user, request):
    user_name = user.first_name + " " + user.last_name
    current_site = Site.objects.get_current(request)
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    scheme = request.scheme
    confirmation_url = reverse('accounts:confirm_email', args=[uid, token])
    confirmation_url = f"{scheme}://{current_site.domain}{confirmation_url}"
    html_message = render_to_string("registration/confirm_email.html", {"user": user_name, "link": confirmation_url})
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject="Confirm Your Email",
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email],
        body=plain_message,
    )
    message.attach_alternative(html_message, "text/html")
    message.send()


def send_welcome_email(user):
    recipient_list = [user.email]
    user_name = user.first_name + " " + user.last_name
    html_message = render_to_string("accounts/welcome_email.html", {"user": user_name})
    plain_message = strip_tags(html_message)
    message = EmailMultiAlternatives(
        subject="Welcome to Winni Furnace",
        from_email=settings.EMAIL_HOST_USER,
        to=recipient_list,
        body=plain_message,
    )
    message.attach_alternative(html_message, "text/html")
    message.send()


class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/rest_password_form.html'
    email_template_name = 'registration/password_forget_mail.html'
    success_url = reverse_lazy('accounts:password_reset_done')

    def form_valid(self, form):
        user = self.get_user(form)
        if user is not None:
            self.send_custom_password_reset_email(form)
        else:
            return redirect("accounts:email_not_found")
        response = super().form_valid(form)

        return response

    def send_custom_password_reset_email(self, form):
        user_email = form.cleaned_data['email']
        try:
            user = CustomUser.objects.get(email=user_email)
        except CustomUser.DoesNotExist:
            user = None
        print(user)
        if user:
            user_name = user.first_name + " " + user.last_name
            current_site = Site.objects.get_current(self.request)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            scheme = self.request.scheme
            confirmation_url = reverse('accounts:password_reset_confirm', args=[uid, token])
            confirmation_url = f"{scheme}://{current_site.domain}{confirmation_url}"
            html_message = render_to_string("registration/password_forget_mail.html",
                                            {"user": user_name, "link": confirmation_url})
            plain_message = strip_tags(html_message)

            message = EmailMultiAlternatives(
                subject="Rest Password",
                from_email=settings.EMAIL_HOST_USER,
                to=[user.email],
                body=plain_message,
            )
            message.attach_alternative(html_message, "text/html")
            message.send()
        else:
            return redirect("accounts:email_not_found")

    def get_user(self, form):
        user_email = form.cleaned_data['email']

        try:
            user = CustomUser.objects.get(email=user_email)
        except CustomUser.DoesNotExist:
            user = None

        return user


def email_not_found(request):
    return render(request, "accounts/user_not_found.html")


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_rest_send.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'
