from django.db import models
from django.conf import settings

class Evenement(models.Model):
    FORMAT_CHOICES = [
        ('online', 'En ligne'),
        ('presentiel', 'Présentiel'),
    ]
    CATEGORY_CHOICES = [
        ('business', 'Business'),
        ('design', 'Design'),
        ('marketing', 'Marketing'),
        ('finance', 'Finance'),
        ('education', 'Education'),
        ('autre', 'Autre'),
    ]
    STATUS_CHOICES = [
        ('publier', 'Publier'),
        ('brouillon', 'Brouillon'),
        ('live', 'Live'),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='event_covers/')
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    format = models.CharField(max_length=20, choices=FORMAT_CHOICES)
    categorie = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    capacite = models.PositiveIntegerField()
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='brouillon')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
