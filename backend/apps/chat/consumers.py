from channels.db import database_sync_to_async
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer

from apps.salon_role.models import SalonRoleModels
from apps.sellers.models import SellersModel


class ChatConsumer(GenericAsyncAPIConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_name = None
        self.user_name = None

    async def connect(self):
        if not self.scope['user'].is_authenticated:
            return await self.close()

        await self.accept()
        self.room_name = self.scope['url_route']['kwargs']['room']
        self.user_name = await self.get_profile_name()
        roles = await self.get_user_roles()

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'sender',
                'message': f'{self.user_name} connected to chat',
                'user': self.user_name,
                **roles
            }
        )

    async def sender(self, data):
        await self.send_json(data)

    @action()
    async def send_message(self, data, request_id, action):
        roles = await self.get_user_roles()

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'sender',
                'message': data,
                'user': self.user_name,
                'id': request_id,
                **roles
            }
        )

    @database_sync_to_async
    def get_profile_name(self):
        user = self.scope['user']
        return user.profile.name

    @database_sync_to_async
    def get_user_roles(self):
        user = self.scope["user"]
        return {
            'is_user': user.is_active,
            "is_staff": user.is_staff,
            "is_seller": SellersModel.objects.filter(user=user).exists(),
            "is_auto_salon_member": SalonRoleModels.objects.filter(user=user).exists()
        }


