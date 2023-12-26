from django.db import models
from django.contrib.auth.models import AbstractUser
import random
import string


class ReferralCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    user = models.OneToOneField("CustomUser", on_delete=models.CASCADE)

    def __str__(self):
        return self.code


class CustomUser(AbstractUser):
    score = models.PositiveIntegerField(default=0)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=100)
    email_confirmed = models.BooleanField(default=False)
    have_referral = models.BooleanField(default=False)
    referral_code = models.OneToOneField(ReferralCode, on_delete=models.CASCADE, null=True, blank=True, unique=True)

    def __str__(self):
        return self.username


def generate_referral_code():
    code_length = 8
    characters = string.ascii_letters + string.digits
    unique_code = ''.join(random.choice(characters) for _ in range(code_length))
    duplicate = ReferralCode.objects.filter(code=unique_code)
    if duplicate:
        generate_referral_code()

    return unique_code


def create_referral_code(user):
    try:
        user = CustomUser.objects.get(pk=user.id)
        if user and not user.referral_code:
            code = generate_referral_code()
            new_code = ReferralCode(user=user, code=code)
            new_code.save()
            user.referral_code = new_code
            user.save()
    except CustomUser.DoesNotExist as e:
        print(f"Error in create_referral_code: {e}")
    except Exception as e:
        print(f"Unexpected error in create_referral_code: {e}")
