from django.db import models
from accounts.models import CustomUser
from django.utils import timezone


class OurServices(models.Model):
    class ServicesChoice(models.TextChoices):
        FREE_DUCT_INSPECTION = "DI", "Free Duct Inspection"
        FREE_SANITIZATION = "FS", "Free Sanitization"
        DUCT_CLEANING = "DC", "Duct Cleaning"
        FURNACE_INSTALLATION = "FI", "Furnace Installation"
        FURNACE_REPAIR = "FR", "Furnace Repair"
        FURNACE_CLEANING = "FC", "Furnace Cleaning"
        AIR_CONDITIONER_INSTALLATION = "AI", "Air Conditioner Installation"
        AIR_CONDITIONER_TUNE_UP = "AR", "Air Conditioner Tune Up"

    service = models.CharField(max_length=2, choices=ServicesChoice.choices)
    is_user = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    order_time = models.DateTimeField(auto_now=True)
    finished_time = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()

    def __str__(self):
        return self.service