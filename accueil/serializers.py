from rest_framework import serializers
from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    file_url = serializers.SerializerMethodField()
    cover_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'owner', 'file_url', 'cover_url', 'created_at']

    def get_file_url(self, obj):
        return obj.file.url if obj.file else None

    def get_cover_url(self, obj):
        return obj.cover.url if obj.cover else None
