from rest_framework import viewsets, permissions, filters
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Video
from .serializers import VideoSerializer
from API.services.supabase_service import upload_video

class VideoViewSet(viewsets.ModelViewSet):
    serializer_class = VideoSerializer
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

    def get_queryset(self):
        # Par défaut, uniquement les vidéos publiques pour l'accueil
        if self.action == 'list':
            return Video.objects.filter(is_public=True).order_by('-created_at')
        return Video.objects.all().order_by('-created_at')

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]   # ✅ lecture publique
        return [permissions.IsAuthenticated()]  # ✅ upload/update/delete mande login

    def create(self, request, *args, **kwargs):
        # Gérer l'upload vidéo vers Supabase
        video_file = request.FILES.get('file')
        if not video_file:
            return Response({'error': 'Aucun fichier vidéo fourni'}, status=400)
        
        try:
            # Upload vers Supabase
            filename = f"video_{request.user.id}_{video_file.name}"
            upload_result = upload_video(video_file, filename)
            
            # Déterminer si la vidéo est publique ou brouillon
            is_public_str = request.data.get('is_public', 'true')
            is_public = is_public_str == 'true'
            
            # Créer l'enregistrement dans Django avec le nom du fichier Supabase
            video_data = {
                'title': request.data.get('title', filename),
                'description': request.data.get('description', ''),
                'file': filename,  # Stocker le nom du fichier Supabase (CharField)
                'owner': request.user.id,
                'is_public': is_public
            }
            
            serializer = self.get_serializer(data=video_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return Response(serializer.data, status=201)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=500)

    @action(detail=False, methods=['get'])
    def my_videos(self, request):
        """Récupérer toutes les vidéos de l'utilisateur connecté (publiques et brouillons)"""
        if not request.user.is_authenticated:
            return Response({'error': 'Non authentifié'}, status=401)
        
        videos = Video.objects.filter(owner=request.user).order_by('-created_at')
        serializer = self.get_serializer(videos, many=True)
        return Response(serializer.data)




from django.shortcuts import render

def backend_status(request):
    return render(request, "status.html")
