from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Profil, Skill
from .serializers import ProfilSerializer, SkillSerializer

class SkillViewSet(viewsets.ModelViewSet):
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Skill.objects.filter(profile__user=self.request.user)
    
    def perform_create(self, serializer):
        # Récupérer ou créer le profil de l'utilisateur
        profile, created = Profil.objects.get_or_create(user=self.request.user)
        serializer.save(profile=profile)

class ProfilViewSet(viewsets.ModelViewSet):
    serializer_class = ProfilSerializer
    queryset = Profil.objects.select_related('user').prefetch_related('skills').all()
    permission_classes = [permissions.AllowAny]  # Changed to allow public viewing
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'user__full_name', 'user__profession', 'user__speciality', 'user__country', 'user__city', 'bio', 'location']

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        # Synchroniser la profession depuis CustomUser vers Profil lors de la création
        if self.request.user.profession:
            serializer.instance.profession = self.request.user.profession
            serializer.instance.save()

    @action(detail=False, methods=['get', 'put', 'patch'], url_path='me')
    def me(self, request):
        try:
            if not request.user.is_authenticated:
                return Response({'detail': 'Authentication required'}, status=401)

            profile, created = Profil.objects.get_or_create(user=request.user)

            # Synchroniser les données CustomUser vers Profil lors de la création
            if created:
                profile.profession = request.user.profession
                profile.speciality = request.user.speciality
                profile.save()

            if request.method in ['PUT', 'PATCH']:
                # Gérer l'upload de fichiers vers Supabase
                if 'photo' in request.FILES:
                    from API.services.supabase_service import upload_file
                    photo_file = request.FILES['photo']
                    photo_filename = f"profile_{request.user.id}_{photo_file.name}"
                    upload_result = upload_file(photo_file, photo_filename)
                    # Stocker le nom réellement généré par Supabase (il contient un UUID)
                    profile.photo = upload_result["filename"]
                
                if 'banner' in request.FILES:
                    from API.services.supabase_service import upload_file
                    banner_file = request.FILES['banner']
                    banner_filename = f"banner_{request.user.id}_{banner_file.name}"
                    upload_result = upload_file(banner_file, banner_filename)
                    # Stocker le nom réellement généré par Supabase (il contient un UUID)
                    profile.banner = upload_result["filename"]
                
                # Synchroniser la profession entre CustomUser et Profil
                if 'profession' in request.data:
                    profession = request.data['profession']
                    # Mettre à jour CustomUser avec restriction de 30 jours
                    if hasattr(request.user, 'can_update_profession') and request.user.can_update_profession():
                        request.user.profession = profession
                        request.user.last_profession_update = timezone.now()
                        request.user.save()
                    # Mettre à jour Profil (sans restriction)
                    profile.profession = profession
                
                # Créer une copie de request.data sans les fichiers
                data_copy = request.data.copy()
                if 'photo' in data_copy:
                    del data_copy['photo']
                if 'banner' in data_copy:
                    del data_copy['banner']
                
                # Mettre à jour les autres champs (sans les fichiers)
                serializer = ProfilSerializer(profile, data=data_copy, partial=request.method == 'PATCH', context={'request': request})
                serializer.is_valid(raise_exception=True)
                serializer.save()
                
                # Sauvegarder le profil avec les noms de fichiers Supabase
                profile.save()
                
                return Response(serializer.data)
            serializer = ProfilSerializer(profile, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'detail': str(e)}, status=500)
