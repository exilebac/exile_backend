from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserStatisticsViewSet, DailyStatisticsViewSet

router = DefaultRouter()
router.register(r'user-stats', UserStatisticsViewSet, basename='user-statistics')
router.register(r'daily-stats', DailyStatisticsViewSet, basename='daily-statistics')

urlpatterns = [
    path('', include(router.urls)),
]
