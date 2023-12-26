from django import template
from ..models import SiteOffers

register = template.Library()


@register.inclusion_tag('offers/available_offers.html')
def show_latest_offers():
    all_offers = SiteOffers.objects.all()
    for offer in all_offers:
        offer.check_availability()
    available_offers = SiteOffers.objects.filter(availability=SiteOffers.Status.AVAILABLE).all()
    return {'available_offers': available_offers}
