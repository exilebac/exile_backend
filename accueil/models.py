from django.db import models
from django.conf import settings

class Video(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.CharField(max_length=500)  # Stocke le nom du fichier Supabase
    cover = models.CharField(max_length=500, blank=True, null=True)  # Stocke le nom du fichier cover Supabase
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
