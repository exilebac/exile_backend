from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Conversation, Message, ConversationParticipant
from .serializers import (
    ConversationSerializer, 
    MessageSerializer, 
    CreateConversationSerializer,
    CreateMessageSerializer
)

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(participants=user)
    
    def perform_create(self, serializer):
        # Add current user to participants
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
    
    @action(detail=False, methods=['post'])
    def start(self, request):
        """Start a new conversation with a user"""
        serializer = CreateConversationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        participant_id = serializer.validated_data['participant_id']
        initial_message = serializer.validated_data.get('initial_message', '')
        
        # Check if conversation already exists between these users
        existing = Conversation.objects.filter(participants=request.user).filter(
            participants__id=participant_id
        ).distinct().first()
        
        if existing:
            # Send initial message if provided
            if initial_message:
                Message.objects.create(
                    conversation=existing,
                    sender=request.user,
                    content=initial_message
                )
            return Response(ConversationSerializer(existing, context={'request': request}).data)
        
        # Create new conversation
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, participant_id)
        
        # Add participant info
        ConversationParticipant.objects.create(conversation=conversation, user=request.user)
        ConversationParticipant.objects.create(conversation=conversation, user_id=participant_id)
        
        # Send initial message if provided
        if initial_message:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=initial_message
            )
        
        return Response(
            ConversationSerializer(conversation, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark conversation as read for current user"""
        conversation = self.get_object()
        participant_info = conversation.participant_info.filter(user=request.user).first()
        
        if participant_info:
            from django.utils import timezone
            participant_info.last_read_at = timezone.now()
            participant_info.save()
        
        # Mark all messages as read
        conversation.messages.filter(sender__ne=request.user).update(read=True)
        
        return Response({'status': 'marked as read'})
    
    @action(detail=True, methods=['post'])
    def toggle_pin(self, request, pk=None):
        """Toggle conversation pin status"""
        conversation = self.get_object()
        conversation.is_pinned = not conversation.is_pinned
        conversation.save()
        return Response({'is_pinned': conversation.is_pinned})

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        conversation_id = self.request.query_params.get('conversation')
        if conversation_id:
            return Message.objects.filter(conversation_id=conversation_id)
        return Message.objects.filter(conversation__participants=self.request.user)
    
    def perform_create(self, serializer):
        conversation = serializer.validated_data['conversation']
        
        # Check if user is participant
        if not conversation.participants.filter(id=self.request.user.id).exists():
            return Response(
                {'error': 'You are not a participant in this conversation'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer.save(sender=self.request.user)
        
        # Update conversation timestamp
        conversation.save()
    
    @action(detail=True, methods=['post'])
    def mark_important(self, request, pk=None):
        """Toggle message importance"""
        message = self.get_object()
        if message.sender != request.user:
            return Response(
                {'error': 'You can only mark your own messages'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        message.is_important = not message.is_important
        message.save()
        return Response({'is_important': message.is_important})

