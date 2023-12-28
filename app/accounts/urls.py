from django.urls import path
from .views import (signup_view, dashboard, edit_account_information, confirm_delete_account, delete_account,
                    logout_view, confirm_email, send_confirmation_email, generate_referral_link,
                    CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView,
                    CustomPasswordResetCompleteView, email_not_found, CustomLoginView)
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("accounts/login/", CustomLoginView.as_view(), name="login"),
    path("signup/", signup_view, name="signup"),
    path("logout/", logout_view, name="logout"),
    path("password-change/", auth_views.PasswordChangeView.as_view(), name="password_change"),
    path("password-change/done/", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("edit-information/", edit_account_information, name="edit_account_information"),
    path("confirm-delete-account/", confirm_delete_account, name="confirm_delete_account"),
    path("delete-account/", delete_account, name="delete_account"),
    path('confirm/<str:uidb64>/<str:token>/', confirm_email, name='confirm_email'),
    path("Send-confirm-Email/<int:user_id>/", send_confirmation_email, name="send_email_confirmation"),
    path('generate-referral-link/', generate_referral_link, name='generate_referral_link'),
    path("email-not-found/", email_not_found, name='email_not_found'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
