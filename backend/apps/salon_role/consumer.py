from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer import model_observer

from apps.salon_role.models import SalonRoleModels
from apps.salon_role.serializers import SalonRoleSerializer


class SalonRoleConsumer(GenericAsyncAPIConsumer):
    async def connect(self):
        user = self.scope['user']
        if not user or not user.is_authenticated:
            return await self.close()
        await self.accept()

    @model_observer(SalonRoleModels, serializer_class=SalonRoleSerializer)
    async def salon_role_activity(self, message, action, subscribing_request_ids, **kwargs):
        for request_id in subscribing_request_ids:
            await self.reply(data=message, action=action, request_id=request_id)

    @action()
    async def subscribe_to_salon_roles(self, request_id, **kwargs):
        await self.salon_role_activity.subscribe(request_id=request_id)
