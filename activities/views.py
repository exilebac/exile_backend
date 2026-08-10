from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Activity
from .serializers import ActivitySerializer

class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Activity.objects.filter(user=user)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Retourne les activités récentes de l'utilisateur"""
        activities = self.get_queryset()[:10]
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)
