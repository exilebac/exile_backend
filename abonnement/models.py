from django.db import models
from django.conf import settings
from accueil.models import Video

class Abonnement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    professionnel = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='abonnes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Favoris(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
