from rest_framework import serializers
from .models import Profil

class ProfilSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profil
        fields = '__all__'
