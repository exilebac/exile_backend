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


class CustomLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        print(f"DEBUG: Login attempt for username: {username}")
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
