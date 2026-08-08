from rest_framework import viewsets, permissions, filters
from .models import Profil
from .serializers import ProfilSerializer

# Custom permission: tout moun ka wè profil, men sèlman pwopriyetè ka modifye li
from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.user == request.user

class ProfilViewSet(viewsets.ModelViewSet):
    serializer_class = ProfilSerializer
    queryset = Profil.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'user__full_name', 'user__profession', 'user__speciality', 'user__country', 'user__city', 'bio', 'location']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
