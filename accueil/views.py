from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from .models import Video
from .serializers import VideoSerializer
from API.services.supabase_service import upload_video

def backend_status(request):
    """Endpoint pour vérifier le statut du backend"""
    return Response({
        "status": "Backend Django fonctionne",
        "version": "1.0.0"
    })

class VideoViewSet(viewsets.ModelViewSet):
    serializer_class = VideoSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.action == 'list':
            return Video.objects.filter(is_public=True).order_by('-created_at')
        return Video.objects.all()

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_videos(self, request):
        """Retourne les vidéos de l'utilisateur connecté"""
        videos = Video.objects.filter(owner=request.user).order_by('-created_at')
        serializer = self.get_serializer(videos, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Upload une vidéo vers Supabase puis crée
        l'enregistrement correspondant dans Django.
        """

        if not request.user or not request.user.is_authenticated:
            return Response(
                {
                    "error": "Utilisateur non authentifié."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        video_file = request.FILES.get("file")

        if not video_file:
            return Response(
                {
                    "error": "Aucun fichier vidéo fourni."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # ====================================================
            # NOM INITIAL
            # ====================================================

            filename = (
                f"video_{request.user.id}_"
                f"{video_file.name}"
            )

            # ====================================================
            # UPLOAD SUPABASE
            # ====================================================

            upload_result = upload_video(
                video_file,
                filename,
            )

            # Récupérer le vrai nom unique créé
            # par upload_video()
            stored_filename = upload_result["filename"]

            if not stored_filename:
                raise ValueError("Le nom de fichier Supabase est vide")

            # ====================================================
            # PUBLIC / BROUILLON
            # ====================================================

            is_public_value = request.data.get(
                "is_public",
                "true",
            )

            if isinstance(is_public_value, bool):
                is_public = is_public_value
            else:
                is_public = str(
                    is_public_value
                ).lower() in (
                    "true",
                    "1",
                    "yes",
                )

            # ====================================================
            # DONNÉES DJANGO
            # ====================================================

            video_data = {
                "title": request.data.get(
                    "title",
                    video_file.name,
                ),

                "description": request.data.get(
                    "description",
                    "",
                ),

                # IMPORTANT :
                # enregistrer le vrai nom Supabase
                "file": stored_filename,

                "owner_id": request.user.id,

                "is_public": is_public,
            }

            # ====================================================
            # VALIDATION
            # ====================================================

            serializer = VideoSerializer(data=video_data)

            serializer.is_valid(
                raise_exception=True
            )

            # ====================================================
            # ENREGISTREMENT DATABASE
            # ====================================================

            video_instance = serializer.save()

            # ====================================================
            # RÉPONSE
            # ====================================================

            return Response(
                VideoSerializer(video_instance).data,
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:

            import traceback

            print(
                "=========================================="
            )
            print(
                "ERREUR UPLOAD VIDÉO"
            )
            print(
                "=========================================="
            )

            traceback.print_exc()

            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
