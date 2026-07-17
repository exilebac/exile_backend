from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AbonnementViewSet, FavorisViewSet, FeedViewSet

router = DefaultRouter()
router.register(r'abonnements', AbonnementViewSet, basename='abonnement')
router.register(r'favoris', FavorisViewSet, basename='favoris')
router.register(r'feed', FeedViewSet, basename='feed')

urlpatterns = [
    path('', include(router.urls)),
]
