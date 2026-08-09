from django.db import models
from django.conf import settings

class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('video_upload', 'Upload de vidéo'),
        ('video_like', 'Like vidéo'),
        ('video_comment', 'Commentaire vidéo'),
        ('profile_update', 'Mise à jour profil'),
        ('subscription', 'Abonnement'),
        ('badge_earned', 'Badge gagné'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Activité'
        verbose_name_plural = 'Activités'
    
    def __str__(self):
        return f"{self.user.username} - {self.activity_type}"
