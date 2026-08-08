from rest_framework import viewsets, permissions, filters
from .models import Video
from .serializers import VideoSerializer

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.filter(is_public=True).order_by('-created_at')
    serializer_class = VideoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]   # ✅ lecture publique
        return [permissions.IsAuthenticated()]  # ✅ upload/update/delete mande login




from django.shortcuts import render

def backend_status(request):
    return render(request, "status.html")
