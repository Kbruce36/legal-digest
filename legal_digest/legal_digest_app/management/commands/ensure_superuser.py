"""
Create initial superuser if none exists.
Run this with: python manage.py ensure_superuser
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):
    help = 'Creates a superuser if none exists'

    def handle(self, *args, **options):
        User = get_user_model()
        
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS('Superuser already exists'))
            return
        
        username = os.getenv('SUPERUSER_USERNAME', 'Martha')
        email = os.getenv('SUPERUSER_EMAIL', 'brucemalloy36@gmail.com')
        password = os.getenv('SUPERUSER_PASSWORD', 'Martha@36')
        
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        
        self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully!'))
