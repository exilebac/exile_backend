from rest_framework import viewsets, permissions
from .models import Demande
from .serializers import DemandeSerializer

class DemandeViewSet(viewsets.ModelViewSet):
    serializer_class = DemandeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # itilizatè yo se menm pwofesyonèl yo → montre demandes kote yo sender oswa receiver
        queryset = Demande.objects.filter(sender=user) | Demande.objects.filter(receiver=user)

        # filtre selon onglet (status)
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # barre de recherche adapte selon onglet
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(message__icontains=search)

        return queryset.order_by('-created_at')
