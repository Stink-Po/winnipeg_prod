from django.db import models


class Message(models.Model):
    class Status(models.TextChoices):
        ANSWERED = "A", "Answered"
        NEW = "N", "New"

    name = models.CharField(max_length=250)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=350, null=True, blank=True)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.NEW)

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
        ]

    def __str__(self):
        return f"name: {self.name}, message = {self.message}"
