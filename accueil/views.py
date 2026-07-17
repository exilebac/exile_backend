from rest_framework import viewsets, permissions
from .models import Video
from .serializers import VideoSerializer

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.filter(is_public=True).order_by('-created_at')
    serializer_class = VideoSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]   # ✅ lecture publique
        return [permissions.IsAuthenticated()]  # ✅ upload/update/delete mande login
