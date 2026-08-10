from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Abonnement, Favoris
from .serializers import AbonnementSerializer, FavorisSerializer
from accueil.models import Video

class AbonnementViewSet(viewsets.ModelViewSet):
    serializer_class = AbonnementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Abonnement.objects.filter(user=user)

    @action(detail=False, methods=['get'], url_path='subscribers')
    def subscribers(self, request):
        """Retourne la liste des abonnés de l'utilisateur connecté"""
        from profil.models import Profil
        try:
            user_profile = Profil.objects.get(user=request.user)
            # Compter les utilisateurs qui s'abonnent à ce professionnel
            subscribers_count = Abonnement.objects.filter(professionnel=request.user).count()
            return Response({
                'count': subscribers_count,
                'subscribers': list(Abonnement.objects.filter(professionnel=request.user).values_list('user__username', flat=True))
            })
        except Profil.DoesNotExist:
            return Response({'count': 0, 'subscribers': []})

class FavorisViewSet(viewsets.ModelViewSet):
    serializer_class = FavorisSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Favoris.objects.filter(user=user)

# Feed (Tous)
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
