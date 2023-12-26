from django.urls import path
from .views import order, review_order, confirm_order, finish_order,cancel_order, view_order_details
app_name = 'services'

urlpatterns = [
    path("", order, name="order"),
    path('Order/confirm/<str:service_name>/<str:name>/<str:phone>/<str:email>/<str:message>/', review_order,
         name='confirm_order'),
    path("Order/success/<str:service_name>/<str:name>/<str:phone>/<str:email>/<str:message>/", confirm_order,
         name="success_order"),
    path("finish-order/<int:order_id>", finish_order, name="finish_order"),
    path("cancel-order/<int:order_id>", cancel_order, name="cancel_order"),
    path("order-details/<int:order_id>/", view_order_details, name="view_order_details"),

]