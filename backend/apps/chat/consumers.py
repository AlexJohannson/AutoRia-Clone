import datetime

from django.contrib.auth import get_user_model
from django.db.models import F

from channels.db import database_sync_to_async
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer

from apps.chat.models import ChatRoomModel, MessageModel
from apps.salon_role.models import SalonRoleModels
from apps.sellers.models import SellersModel

UserModel = get_user_model()


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

        await self.channel_layer.group_add(f"user_{self.scope['user'].id}", self.channel_name)
        await self.channel_layer.group_add(self.room.name, self.channel_name)

        messages = await self.get_last_seven_messages()
        for name, text, role, is_private in messages:
            await self.sender({
                'user': name,
                'message': f"Private: {text}" if is_private else text,
                'user_role': role,
                'id': str(datetime.datetime.now()),
                'is_private': is_private
            })

        await self.channel_layer.group_send(
            self.room.name,
            {
                'type': 'sender',
                'message': f'{self.scope["user"].id}_{self.user_name} connected to chat',
                'user': f'{self.scope["user"].id}_{self.user_name}',
                'user_role': user_role
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
            text=data['text'],
            user_role=user_role
        )

        await self.channel_layer.group_send(
            self.room.name,
            {
                'type': 'sender',
                'message': data['text'],
                'user': f'{self.scope["user"].id}_{self.user_name}',
                'user_role': user_role,
                'id': request_id
            }
        )

    @action()
    async def send_private_message(self, data, request_id, action):
        user_role = await self.get_user_role()
        target_user_id = data.get('userId')
        if not target_user_id:
            return

        target_user_id = int(target_user_id)
        sender_id = self.scope['user'].id

        private_room_name = f'private_{min(sender_id, target_user_id)}_{max(sender_id, target_user_id)}'
        private_room, _ = await ChatRoomModel.objects.aget_or_create(name=private_room_name, is_private=True)

        target_user = await UserModel.objects.aget(pk=target_user_id)
        await private_room.users.aadd(target_user)
        await private_room.users.aadd(self.scope['user'])

        original_text = data['text']
        await MessageModel.objects.acreate(
            room=private_room,
            user=self.scope['user'],
            text=original_text,
            user_role=user_role
        )

        display_text = f"Private: {original_text}"

        await self.channel_layer.group_add(private_room.name, self.channel_name)

        await self.channel_layer.group_send(
            private_room.name,
            {
                'type': 'sender',
                'message': display_text,
                'user': f'{self.scope["user"].id}_{self.user_name}',
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
        user = self.scope['user']

        public_messages = MessageModel.objects.filter(
            room=self.room,
            room__is_private=False
        ).annotate(
            name=F('user__profile__name'),
            pk=F('user__pk'),
            is_private=F('room__is_private')
        ).values('name', 'text', 'user_role', 'pk', 'is_private')


        private_messages = MessageModel.objects.filter(
            room__is_private=True,
            room__users=user
        ).annotate(
            name=F('user__profile__name'),
            pk=F('user__pk'),
            is_private=F('room__is_private')
        ).values('name', 'text', 'user_role', 'pk', 'is_private')


        combined = list(public_messages) + list(private_messages)

        sorted_combined = sorted(combined, key=lambda x: x.get('id', 0), reverse=True)[:7]

        return reversed([
            (f"{m['pk']}_{m['name']}", m['text'], m['user_role'], m['is_private']) for m in sorted_combined
        ])




























