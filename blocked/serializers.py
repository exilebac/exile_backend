from rest_framework import serializers
from .models import BlockedUser
from users.models import CustomUser

class BlockedUserSerializer(serializers.ModelSerializer):
    blocked_user = serializers.SerializerMethodField()
    
    class Meta:
        model = BlockedUser
        fields = ['id', 'blocked_user', 'created_at']
        read_only_fields = ['blocker']
    
    def get_blocked_user(self, obj):
        user = obj.blocked
        return {
            'id': user.id,
            'username': user.username,
            'full_name': user.full_name,
            'avatar_url': user.avatar_url
        }

class BlockUserSerializer(serializers.Serializer):
    blocked_id = serializers.IntegerField()
