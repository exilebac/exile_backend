from rest_framework import viewsets, permissions
from .models import Evenement
from .serializers import EvenementSerializer

class EvenementViewSet(viewsets.ModelViewSet):
    serializer_class = EvenementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Evenement.objects.filter(owner=user)

        # filtre selon onglet (status)
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # barre de recherche (nom, titre, description)
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(name__icontains=search) |
                models.Q(title__icontains=search) |
                models.Q(description__icontains=search)
            )

        return queryset.order_by('-date_debut')
