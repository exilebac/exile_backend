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

            # ✅ Si username pa voye, kreye yon default inik
            if not data.get("username"):
                base_name = data.get("full_name", "user")
                data["username"] = f"{base_name}_{uuid.uuid4().hex[:6]}"

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
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        print(f"DEBUG: Login attempt for username: {username}")
        print(f"DEBUG: Password length: {len(password) if password else 0}")
        
        key = f"login_attempts_{username}"
        attempts = cache.get(key, 0)

        if attempts >= 3:
            raise AuthenticationFailed("Trop de tentatives. Réessayez dans 10 minutes.")

        response = super().post(request, *args, **kwargs)
        print(f"DEBUG: Login response status: {response.status_code}")

        if response.status_code != 200:
            cache.set(key, attempts + 1, timeout=600)  # 10 min
        else:
            cache.delete(key)
            # ✅ Ajoute date + IP
            user = CustomUser.objects.filter(username=username).first()
            if user:
                user.last_login_time = timezone.now()
                user.last_login_ip = self.get_client_ip(request)
                user.save()

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
