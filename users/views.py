from rest_framework import generics, permissions
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.utils import timezone


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


from django.core.cache import cache
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import AuthenticationFailed

class CustomLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')   # ✅ itilize username
        key = f"login_attempts_{username}"
        attempts = cache.get(key, 0)

        if attempts >= 3:
            raise AuthenticationFailed("Trop de tentatives. Réessayez dans 10 minutes.")

        response = super().post(request, *args, **kwargs)

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
    
    def get_client_ip(self, request):   # ✅ ajoute metòd sa
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
