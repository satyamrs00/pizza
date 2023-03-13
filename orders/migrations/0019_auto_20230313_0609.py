# Generated by Django 3.2.5 on 2023-03-13 00:39

from django.db import migrations
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.db import transaction
from django.db.utils import IntegrityError


def generate_superuser(apps, schema_editor):
    User = apps.get_model("orders", "User")

    email = settings.DJANGO_SUPERUSER_EMAIL
    password = settings.DJANGO_SUPERUSER_PASSWORD
    username = settings.DJANGO_SUPERUSER_USERNAME

    with transaction.atomic():    
        user = User()
        user.email = BaseUserManager.normalize_email(email)
        user.password = make_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.username = username
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0018_alter_address_phone'),
    ]

    operations = [
        migrations.RunPython(generate_superuser),
    ]
