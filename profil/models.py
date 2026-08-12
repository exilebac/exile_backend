from django.db import models
from django.conf import settings

class Profil(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.CharField(max_length=500, blank=True, null=True)  # Stocke le nom du fichier Supabase
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True)
    profession = models.CharField(max_length=255, blank=True)
    speciality = models.CharField(max_length=255, blank=True)
    banner = models.CharField(max_length=500, blank=True, null=True)  # Stocke le nom du fichier Supabase
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profil de {self.user.username}"

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('technical', 'Technique'),
        ('soft', 'Soft Skills'),
        ('language', 'Langue'),
        ('communication', 'Communication'),
        ('management', 'Management'),
        ('other', 'Autre'),
    ]
    
    LEVEL_CHOICES = [
        ('beginner', 'Débutant'),
        ('intermediate', 'Intermédiaire'),
        ('advanced', 'Avancé'),
        ('expert', 'Expert'),
    ]
    
    profile = models.ForeignKey(Profil, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='intermediate')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"
