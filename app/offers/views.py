from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import SiteOffers
from .forms import OffersForm
from projects.views import is_admin
from django.contrib.auth.decorators import user_passes_test
from accounts.models import CustomUser
from django.contrib.sites.models import Site


def view_offers(request):
    all_offers = SiteOffers.objects.all()
    for offer in all_offers:
        offer.check_availability()

    available_offers = SiteOffers.objects.filter(availability=SiteOffers.Status.AVAILABLE).all()
    titles = [item.title for item in available_offers]
    return render(request, "offers/all_offers.html", {
        "available_offers": available_offers,
        "titles": titles,
    })


@user_passes_test(is_admin)
def add_new_offer(request):
    offer_form = OffersForm()
    if request.method == "POST":
        offer_form = OffersForm(request.POST, request.FILES)
        if offer_form.is_valid():
            scheme = request.scheme
            current_site = Site.objects.get_current(request)
            new_offer = offer_form.save()
            print(new_offer.image)
            recipient_list = CustomUser.objects.exclude(is_superuser=True).values_list("email", flat=True)
            if new_offer.available_till:
                body = (f"We have {new_offer.title} offer for You Our New Offer Details : {new_offer.description} this "
                        f"offer Available till {new_offer.get_available_date()}")
            else:
                body = f"We have {new_offer.title} offer for You Our New Offer Details : {new_offer.description}"
            html_message = render_to_string("offers/offer_mail.html", {
                "body": body,
                "subject": "New Special Offer in Winni Furnace",
                "link": f"{scheme}://{current_site.domain}{new_offer.get_absolute_url()}",
                "new_offer": new_offer,
            })
            plain_message = strip_tags(html_message)
            message = EmailMultiAlternatives(
                subject="New Special Offer in Winni Furnace",
                from_email=settings.EMAIL_HOST_USER,
                to=recipient_list,
                body=plain_message,
            )
            message.attach_alternative(html_message, "text/html")
            message.send()
            return redirect(new_offer.get_absolute_url())

    return render(request, "offers/add_new_offer.html", {"offer_form": offer_form})


def offer_detail(request, slug):
    offer = get_object_or_404(SiteOffers, availability=SiteOffers.Status.AVAILABLE, slug=slug)
    return render(request, "offers/offer_details.html", {"offer": offer})
