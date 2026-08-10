from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlockedUserViewSet

router = DefaultRouter()
router.register(r'blocked', BlockedUserViewSet, basename='blocked')

urlpatterns = [
    path('', include(router.urls)),
]
