import random
import string
from django.db import models
from accounts.models import CustomUser


class DiscountCode(models.Model):
    code = models.CharField(max_length=30)
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='discount_codes')


def generate_discount_code():
    code_length = 8
    characters = string.ascii_letters + string.digits
    unique_code = ''.join(random.choice(characters) for _ in range(code_length))
    duplicate = DiscountCode.objects.filter(code=unique_code)
    if duplicate:
        generate_discount_code()

    return unique_code
