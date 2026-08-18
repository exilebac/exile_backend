from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone
from django.core.cache import cache
from django.db import IntegrityError
import uuid

from .models import CustomUser
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            data = request.data.copy()

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except IntegrityError:
            return Response(
                {"error": "Username oswa email deja egziste."},
                status=status.HTTP_400_BAD_REQUEST
            )


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class ResetPasswordView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        new_password = request.data.get('new_password')
        
        if not email or not new_password:
            return Response(
                {"error": "Email et nouveau mot de passe requis"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if len(new_password) < 8:
            return Response(
                {"error": "Le mot de passe doit contenir au moins 8 caractères"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = CustomUser.objects.filter(email=email).first()
        if not user:
            return Response(
                {"error": "Email non trouvé"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        user.set_password(new_password)
        user.save()
        
        return Response(
            {"success": "Mot de passe réinitialisé avec succès"},
            status=status.HTTP_200_OK
        )


class CustomLoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]  # Explicitement AllowAny pour le login

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except Exception as e:
            print(f"DEBUG: Login error: {e}")
            import traceback
            traceback.print_exc()
            raise

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
