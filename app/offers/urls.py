from django.urls import path
from .views import view_offers, add_new_offer, offer_detail

app_name = 'offers'

urlpatterns = [
    path("", view_offers, name="view_offers"),
    path("add-new-offer/", add_new_offer, name="add_new_offer"),
    path("<slug:slug>/", offer_detail, name="offer_detail"),
]
