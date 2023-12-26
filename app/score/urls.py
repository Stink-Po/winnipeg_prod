from .views import user_discount_code, create_new_code, search_discount_code, flag_code_to_used, how_score_work
from django.urls import path

app_name = 'score'

urlpatterns = [
    path("", user_discount_code, name="user_discount_code"),
    path("create-new-code/", create_new_code, name="create_new_code"),
    path("search/", search_discount_code, name="search_discount_code"),
    path("is_used/<int:code_id>/", flag_code_to_used, name="flag_code_to_used"),
    path("how-score-work/", how_score_work, name="how_score_work"),
]