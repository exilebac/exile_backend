from django.db import models
from django.conf import settings

class UserStatistics(models.Model):
    """Track user statistics"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='statistics'
    )
    
    # View counts
    total_views = models.IntegerField(default=0)
    monthly_views = models.IntegerField(default=0)
    
    # Subscriber counts
    total_subscribers = models.IntegerField(default=0)
    new_subscribers_this_month = models.IntegerField(default=0)
    
    # Engagement
    total_likes = models.IntegerField(default=0)
    total_comments = models.IntegerField(default=0)
    total_shares = models.IntegerField(default=0)
    
    # Content
    total_videos = models.IntegerField(default=0)
    total_events = models.IntegerField(default=0)
    
    # Timestamps
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'User Statistics'
        verbose_name_plural = 'User Statistics'
    
    def __str__(self):
        return f"Statistics for {self.user.username}"

class DailyStatistics(models.Model):
    """Daily statistics tracking for analytics"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='daily_statistics'
    )
    date = models.DateField()
    
    views = models.IntegerField(default=0)
    new_subscribers = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date']
        verbose_name = 'Daily Statistics'
        verbose_name_plural = 'Daily Statistics'
    
    def __str__(self):
        return f"{self.user.username} - {self.date}"

