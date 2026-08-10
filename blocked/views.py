from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import BlockedUser
from .serializers import BlockedUserSerializer, BlockUserSerializer

class BlockedUserViewSet(viewsets.ModelViewSet):
    serializer_class = BlockedUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return BlockedUser.objects.filter(blocker=user)
    
    def perform_create(self, serializer):
        serializer.save(blocker=self.request.user)
    
    @action(detail=False, methods=['post'])
    def block(self, request):
        """Block a user"""
        serializer = BlockUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        blocked_id = serializer.validated_data['blocked_id']
        
        # Prevent self-blocking
        if blocked_id == request.user.id:
            return Response(
                {'error': 'You cannot block yourself'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if already blocked
        if BlockedUser.objects.filter(blocker=request.user, blocked_id=blocked_id).exists():
            return Response(
                {'error': 'User is already blocked'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create block
        BlockedUser.objects.create(blocker=request.user, blocked_id=blocked_id)
        
        return Response({'status': 'user blocked'}, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def unblock(self, request):
        """Unblock a user"""
        blocked_id = request.data.get('blocked_id')
        
        if not blocked_id:
            return Response(
                {'error': 'blocked_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Delete block
        deleted, _ = BlockedUser.objects.filter(
            blocker=request.user,
            blocked_id=blocked_id
        ).delete()
        
        if deleted:
            return Response({'status': 'user unblocked'})
        else:
            return Response(
                {'error': 'Block not found'},
                status=status.HTTP_404_NOT_FOUND
            )

