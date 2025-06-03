from rest_framework import serializers

from apps.chat.models import ChatRoomModel, MessageModel


class MessageSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(read_only=True)
    user_role = serializers.CharField(read_only=True)

    class Meta:
        model = MessageModel
        fields = ['id', 'text', 'user_name', 'user_role', 'room']


class ChatRoomSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoomModel
        fields = ['id', 'name', 'participants']

    def get_participants(self, obj):
        users = obj.messages.values_list('user__profile__name', 'user_role').distinct()
        return [{'name': name, 'role': role} for name, role in users]
