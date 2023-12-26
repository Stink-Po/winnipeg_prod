from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config


class Command(BaseCommand):
    help = 'Create a superuser'

    def handle(self, *args, **options):
        user = get_user_model()
        if not user.objects.filter(username='admin').exists():
            user.objects.create_superuser('admin', config("ADMIN_EMAIL"), config("ADMIN_PASSWORD"))
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists'))
