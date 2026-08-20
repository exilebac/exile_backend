from rest_framework import serializers
from django.conf import settings
from .models import Profil, Skill

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'category', 'level', 'created_at']
        read_only_fields = ['created_at']

class ProfilSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True, allow_blank=True)
    # Champs provenant de CustomUser (lecture seule)
    user_profession = serializers.CharField(source='user.profession', read_only=True, required=False, allow_blank=True)
    user_speciality = serializers.CharField(source='user.speciality', read_only=True, required=False, allow_blank=True)
    country = serializers.CharField(source='user.country', read_only=True)
    city = serializers.CharField(source='user.city', read_only=True)
    last_profession_update = serializers.DateTimeField(source='user.last_profession_update', read_only=True)
    date_joined = serializers.DateTimeField(source='user.date_joined', read_only=True)
    # Champs propres au modèle Profil (lecture/écriture)
    skills = SkillSerializer(many=True, read_only=True)
    photo_url = serializers.SerializerMethodField()
    banner_url = serializers.SerializerMethodField()
    # photo et banner sont read_only car gérés manuellement dans la vue
    photo = serializers.CharField(read_only=True, required=False, allow_blank=True)
    banner = serializers.CharField(read_only=True, required=False, allow_blank=True)

    class Meta:
        model = Profil
        fields = ['id', 'user', 'username', 'full_name', 'email', 'user_profession', 'user_speciality', 'country', 'city', 'photo', 'photo_url', 'bio', 'location', 'website', 'profession', 'speciality', 'banner', 'banner_url', 'created_at', 'skills', 'last_profession_update', 'date_joined']
    
    def get_photo_url(self, obj):
        if obj.photo:
            try:
                from API.services.supabase_service import supabase
                signed_url = supabase.storage.from_("Exile_images").create_signed_url(obj.photo, 3600)
                return signed_url.get('signed_url') if isinstance(signed_url, dict) else signed_url
            except:
                return None
        return None
    
    def get_banner_url(self, obj):
        if obj.banner:
            try:
                from API.services.supabase_service import supabase
                signed_url = supabase.storage.from_("Exile_images").create_signed_url(obj.banner, 3600)
                return signed_url.get('signed_url') if isinstance(signed_url, dict) else signed_url
            except:
                return None
        return None
