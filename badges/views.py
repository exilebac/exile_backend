from rest_framework import viewsets, permissions
from .models import Badge, UserBadge
from .serializers import BadgeSerializer, UserBadgeSerializer

class BadgeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BadgeSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Badge.objects.all()

class UserBadgeViewSet(viewsets.ModelViewSet):
    serializer_class = UserBadgeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return UserBadge.objects.filter(user=user)
