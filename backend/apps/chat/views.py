from rest_framework.exceptions import NotFound
from rest_framework.generics import DestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.chat.models import ChatRoomModel, MessageModel

from .permissions import IsMessageOwnerOrAdmin, IsParticipantOrAdmin
from .serializers import ChatRoomSerializer, MessageSerializer


class ChatRoomListView(ListAPIView):
    """
        get:
            get chat rooms list
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ChatRoomSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return ChatRoomModel.objects.all()
        return ChatRoomModel.objects.filter(messages__user=user).distinct()


class ChatRoomDetailView(RetrieveAPIView):
    """
        get:
            get chat room detail by id
    """

    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOrAdmin]

    def get_queryset(self):
        return ChatRoomModel.objects.all()

    def get_object(self):
        room_id = self.kwargs['pk']
        try:
            return ChatRoomModel.objects.get(pk=room_id)
        except ChatRoomModel.DoesNotExist:
            raise NotFound('Chat room not found')

    def retrieve(self, request, *args, **kwargs):
        room = self.get_object()
        self.check_object_permissions(request, room)
        messages = room.messages.select_related('user__profile').all()
        serializer = MessageSerializer(messages, many=True)
        return Response({
            'room_id': room.id,
            'room_name': room.name,
            'messages': serializer.data
        })


class ChatRoomDeleteView(DestroyAPIView):
    """
        delete:
            delete chat room by id
    """

    queryset = ChatRoomModel.objects.all()
    permission_classes = [IsAuthenticated, IsParticipantOrAdmin]

    def get_object(self):
        try:
            room = super().get_object()
        except ChatRoomModel.DoesNotExist:
            raise NotFound('Chat room not found')
        self.check_object_permissions(self.request, room)
        return room


class MessageDeleteView(DestroyAPIView):
    """
        delete:
            delete message by id
    """

    queryset = MessageModel.objects.select_related('user', 'room')
    permission_classes = [IsAuthenticated, IsMessageOwnerOrAdmin]

    def get_object(self):
        try:
            message = super().get_object()
        except MessageModel.DoesNotExist:
            raise NotFound('Message not found')
        self.check_object_permissions(self.request, message)
        return message


