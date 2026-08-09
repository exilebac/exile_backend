from rest_framework import serializers
from .models import UserStatistics, DailyStatistics

class UserStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStatistics
        fields = [
            'id', 'user', 'total_views', 'monthly_views',
            'total_subscribers', 'new_subscribers_this_month',
            'total_likes', 'total_comments', 'total_shares',
            'total_videos', 'total_events',
            'last_updated', 'created_at'
        ]
        read_only_fields = ['user']

class DailyStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyStatistics
        fields = ['id', 'user', 'date', 'views', 'new_subscribers', 'likes', 'comments']
        read_only_fields = ['user']

class StatisticsSummarySerializer(serializers.Serializer):
    """Serializer for aggregated statistics"""
    period = serializers.CharField()
    total_views = serializers.IntegerField()
    views_change = serializers.FloatField()
    total_subscribers = serializers.IntegerField()
    subscribers_change = serializers.FloatField()
    total_likes = serializers.IntegerField()
    likes_change = serializers.FloatField()
    total_comments = serializers.IntegerField()
    comments_change = serializers.FloatField()
