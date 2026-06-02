# create_admin.py
import os
import django

from mainsystem.models import CustomUser

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newrp.settings') # আপনার প্রোজেক্টের নাম দিন
django.setup()

from django.contrib.auth import get_user_model

CustomUser = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'sadmin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '123456')

if not CustomUser.objects.filter(username=username).exists():
    CustomUser.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' created successfully!")
else:
    print(f"Superuser '{username}' already exists.")