from rest_framework import serializers
from .models import Video
from API.services.supabase_service import get_signed_url, supabase

class VideoSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    file_url = serializers.SerializerMethodField()
    cover_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'owner', 'file_url', 'cover_url', 'created_at', 'is_public']

    def get_file_url(self, obj):
        if not obj.file:
            return None
        
        try:
            signed_url = supabase.storage.from_("Exile_videos").create_signed_url(obj.file, 3600)
            return signed_url.get('signed_url') if isinstance(signed_url, dict) else signed_url
        except:
            return None

    def get_cover_url(self, obj):
        if not obj.cover:
            return None
        
        try:
            signed_url = supabase.storage.from_("Exile_images").create_signed_url(obj.cover, 3600)
            return signed_url.get('signed_url') if isinstance(signed_url, dict) else signed_url
        except:
            return None
