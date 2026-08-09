from rest_framework import serializers
from .models import Profil

class ProfilSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    profession = serializers.CharField(source='user.profession', read_only=True)
    speciality = serializers.CharField(source='user.speciality', read_only=True)
    country = serializers.CharField(source='user.country', read_only=True)
    city = serializers.CharField(source='user.city', read_only=True)

    class Meta:
        model = Profil
        fields = ['id', 'username', 'full_name', 'profession', 'speciality', 'country', 'city', 'photo', 'bio', 'location', 'website', 'created_at']
