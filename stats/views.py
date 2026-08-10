from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from .models import UserStatistics, DailyStatistics
from .serializers import UserStatisticsSerializer, DailyStatisticsSerializer, StatisticsSummarySerializer

class UserStatisticsViewSet(viewsets.ModelViewSet):
    serializer_class = UserStatisticsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return UserStatistics.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get statistics summary for a time period"""
        period = request.query_params.get('period', '30d')
        user = request.user
        
        # Get or create user statistics
        stats, created = UserStatistics.objects.get_or_create(user=user)
        
        # Calculate changes based on period
        days = 7 if period == '7d' else 30 if period == '30d' else 90 if period == '90d' else 365
        start_date = timezone.now() - timedelta(days=days)
        
        # Get daily statistics for the period
        daily_stats = DailyStatistics.objects.filter(
            user=user,
            date__gte=start_date.date()
        ).aggregate(
            total_views=Sum('views'),
            total_subscribers=Sum('new_subscribers'),
            total_likes=Sum('likes'),
            total_comments=Sum('comments')
        )
        
        # Calculate previous period for comparison
        prev_start_date = start_date - timedelta(days=days)
        prev_stats = DailyStatistics.objects.filter(
            user=user,
            date__gte=prev_start_date.date(),
            date__lt=start_date.date()
        ).aggregate(
            total_views=Sum('views'),
            total_subscribers=Sum('new_subscribers'),
            total_likes=Sum('likes'),
            total_comments=Sum('comments')
        )
        
        # Calculate percentage changes
        def calculate_change(current, previous):
            if not previous or previous == 0:
                return 0
            return ((current - previous) / previous) * 100
        
        current_views = daily_stats['total_views'] or 0
        prev_views = prev_stats['total_views'] or 0
        views_change = calculate_change(current_views, prev_views)
        
        current_subscribers = daily_stats['total_subscribers'] or 0
        prev_subscribers = prev_stats['total_subscribers'] or 0
        subscribers_change = calculate_change(current_subscribers, prev_subscribers)
        
        current_likes = daily_stats['total_likes'] or 0
        prev_likes = prev_stats['total_likes'] or 0
        likes_change = calculate_change(current_likes, prev_likes)
        
        current_comments = daily_stats['total_comments'] or 0
        prev_comments = prev_stats['total_comments'] or 0
        comments_change = calculate_change(current_comments, prev_comments)
        
        return Response({
            'period': period,
            'total_views': stats.total_views,
            'views_change': round(views_change, 1),
            'total_subscribers': stats.total_subscribers,
            'subscribers_change': round(subscribers_change, 1),
            'total_likes': stats.total_likes,
            'likes_change': round(likes_change, 1),
            'total_comments': stats.total_comments,
            'comments_change': round(comments_change, 1)
        })
    
    @action(detail=False, methods=['post'])
    def recalculate(self, request):
        """Recalculate statistics from scratch"""
        user = request.user
        
        # This would typically aggregate data from videos, events, etc.
        # For now, we'll just update the timestamp
        stats, created = UserStatistics.objects.get_or_create(user=user)
        stats.save()
        
        return Response({'status': 'statistics recalculated'})

class DailyStatisticsViewSet(viewsets.ModelViewSet):
    serializer_class = DailyStatisticsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return DailyStatistics.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

