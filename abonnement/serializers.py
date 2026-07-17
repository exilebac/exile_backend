from rest_framework import serializers
from .models import Abonnement, Favoris

class AbonnementSerializer(serializers.ModelSerializer):
    professionnel = serializers.CharField(source='professionnel.username', read_only=True)

    class Meta:
        model = Abonnement
        fields = '__all__'

class FavorisSerializer(serializers.ModelSerializer):
    video_title = serializers.CharField(source='video.title', read_only=True)

    class Meta:
        model = Favoris
        fields = '__all__'
