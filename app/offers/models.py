from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse


class SiteOffers(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "A", "Available"
        EXPIRED = "E", "Expired"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="created_at")
    image = models.ImageField(upload_to="offers_images", null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    available_till = models.DateTimeField(null=True, blank=True)
    availability = models.CharField(max_length=1, choices=Status.choices, default=Status.AVAILABLE)

    def __str__(self):
        return self.title

    def check_availability(self):
        current_date = timezone.now()
        if self.available_till:
            if current_date > self.available_till and self.availability == self.Status.AVAILABLE:
                self.availability = self.Status.EXPIRED
                self.save()

    def save(self, *args, **kwargs):
        # Generate slug from title if not provided
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def mark_unnavigable(self):
        self.availability = SiteOffers.Status.EXPIRED
        self.save()

    def get_absolute_url(self):
        return reverse("offers:offer_detail", args=[
            self.slug,
        ])

    def get_available_date(self):
        # Check if available_till is not None before calling date() to avoid NoneType error
        if self.available_till:
            return self.available_till.date()
        return None
