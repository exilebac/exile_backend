from rest_framework import serializers
from .models import Conversation, Message, ConversationParticipant
from users.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'full_name', 'avatar_url']

class ConversationParticipantSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ConversationParticipant
        fields = ['id', 'user', 'last_read_at']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'content', 'is_important', 'read', 'created_at']
        read_only_fields = ['sender']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    participant_info = ConversationParticipantSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'messages', 'participant_info', 'is_pinned', 'created_at', 'updated_at', 'last_message', 'unread_count']
    
    def get_last_message(self, obj):
        last_msg = obj.messages.last()
        if last_msg:
            return MessageSerializer(last_msg).data
        return None
    
    def get_unread_count(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return 0
        
        participant_info = obj.participant_info.filter(user=request.user).first()
        if not participant_info or not participant_info.last_read_at:
            return obj.messages.filter(read=False).exclude(sender=request.user).count()
        
        return obj.messages.filter(
            read=False,
            created_at__gt=participant_info.last_read_at
        ).exclude(sender=request.user).count()

class CreateConversationSerializer(serializers.Serializer):
    participant_id = serializers.IntegerField()
    initial_message = serializers.CharField(required=False, allow_blank=True)

class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['content', 'is_important']
