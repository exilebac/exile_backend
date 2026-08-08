from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta, date

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True, null=True)

    profession = models.CharField(max_length=100, blank=True, null=True)
    speciality = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    last_name_update = models.DateTimeField(null=True, blank=True)
    last_profession_update = models.DateTimeField(null=True, blank=True)
    last_login_time = models.DateTimeField(null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    USERNAME_FIELD = 'username'   # ✅ Fòse JWT itilize username
    REQUIRED_FIELDS = []  # Email et phone_number sont optionnels

    def save(self, *args, **kwargs):
        # username otomatik si pa defini
        if not self.username:
            self.username = f"@{self.full_name.lower().replace(' ', '_')}"
        super().save(*args, **kwargs)

    def is_adult(self):
        return (date.today().year - self.birth_date.year) >= 18

    def can_update_name(self):
        return not self.last_name_update or timezone.now() - self.last_name_update > timedelta(days=30)

    def can_update_profession(self):
        return not self.last_profession_update or timezone.now() - self.last_profession_update > timedelta(days=30)

    def __str__(self):
        return self.username
