from rest_framework import viewsets, permissions
from .models import Abonnement, Favoris
from .serializers import AbonnementSerializer, FavorisSerializer
from accueil.models import Video

class AbonnementViewSet(viewsets.ModelViewSet):
    serializer_class = AbonnementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Abonnement.objects.filter(user=user)

class FavorisViewSet(viewsets.ModelViewSet):
    serializer_class = FavorisSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Favoris.objects.filter(user=user)

# Feed (Tous)
from rest_framework.response import Response
from rest_framework.decorators import action

class FeedViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def tous(self, request):
        user = request.user
        abonnements = Abonnement.objects.filter(user=user).values_list('professionnel', flat=True)
        videos = Video.objects.filter(owner__in=abonnements, is_public=True)
        favoris = Favoris.objects.filter(user=user)
        return Response({
            "videos": [v.title for v in videos],
            "favoris": [f.video.title for f in favoris],
            "suggestions": ["Suggestion 1", "Suggestion 2"]  # Placeholder
        })
