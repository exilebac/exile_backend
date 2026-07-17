from rest_framework import serializers
from .models import Demande

class DemandeSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username', read_only=True)
    receiver = serializers.CharField(source='receiver.username', read_only=True)

    class Meta:
        model = Demande
        fields = ['id', 'sender', 'receiver', 'message', 'status', 'created_at']
