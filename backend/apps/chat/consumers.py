import datetime

from django.db.models import F

from channels.db import database_sync_to_async
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer

from apps.chat.models import ChatRoomModel, MessageModel
from apps.salon_role.models import SalonRoleModels
from apps.sellers.models import SellersModel


class ChatConsumer(GenericAsyncAPIConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room = None
        self.user_name = None

    async def connect(self):
        if not self.scope['user'].is_authenticated:
            return await self.close()

        await self.accept()

        room_name = self.scope['url_route']['kwargs']['room']
        self.room, _ = await ChatRoomModel.objects.aget_or_create(name=room_name)
        self.user_name = await self.get_profile_name()
        user_role = await self.get_user_role()

        await self.channel_layer.group_add(
            self.room.name,
            self.channel_name
        )


        messages = await self.get_last_seven_messages()
        for name, text, role in messages:
            await self.sender({
                'user': name,
                'message': text,
                'user_role': role,
                'id': str(datetime.datetime.now())
            })


        await self.channel_layer.group_send(
            self.room.name,
            {
                'type': 'sender',
                'message': f'{self.user_name} connected to chat',
                'user': self.user_name,
                'user_role': user_role,
                'id': str(datetime.datetime.now())
            }
        )

    async def sender(self, data):
        await self.send_json(data)

    @action()
    async def send_message(self, data, request_id, action):
        user_role = await self.get_user_role()

        await MessageModel.objects.acreate(
            room=self.room,
            user=self.scope['user'],
            text=data,
            user_role=user_role
        )

        await self.channel_layer.group_send(
            self.room.name,
            {
                'type': 'sender',
                'message': data,
                'user': self.user_name,
                'user_role': user_role,
                'id': request_id
            }
        )

    @database_sync_to_async
    def get_profile_name(self):
        return self.scope['user'].profile.name

    @database_sync_to_async
    def get_user_role(self):
        user = self.scope['user']
        if user.is_staff:
            return 'admin'
        elif SellersModel.objects.filter(user=user).exists():
            return 'seller'
        elif SalonRoleModels.objects.filter(user=user).exists():
            return 'salon_member'
        return 'user'

    @database_sync_to_async
    def get_last_seven_messages(self):
        res = self.room.messages.annotate(
            name=F('user__profile__name')
        ).values('name', 'text', 'user_role').order_by('-id')[:7]
        return reversed([(m['name'], m['text'], m['user_role']) for m in res])














