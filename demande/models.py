from django.db import models
from django.conf import settings

class Demande(models.Model):
    STATUS_CHOICES = [
        ('envoye', 'Envoyé'),
        ('refuse', 'Refusé'),
        ('accepte', 'Accepté'),
        ('bloque', 'Bloqué'),
    ]

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='demandes_envoyees')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='demandes_recues')
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='envoye')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Demande de {self.sender} à {self.receiver} ({self.status})"
