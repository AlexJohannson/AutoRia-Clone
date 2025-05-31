from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer import model_observer

from .models import JoinRequestModel
from .serializers import JoinRequestSerializer


class JoinRequestConsumer(GenericAsyncAPIConsumer):
    async def connect(self):
        user = self.scope['user']
        if not user or not user.is_authenticated:
            return await self.close()
        await self.accept()

    @model_observer(JoinRequestModel, serializer_class=JoinRequestSerializer)
    async def join_request_activity(self, message, action, subscribing_request_ids, **kwargs):
        for request_id in subscribing_request_ids:
            await self.reply(data=message, action=action, request_id=request_id)

    @action()
    async def subscribe_to_join_requests(self, request_id, **kwargs):
        await self.join_request_activity.subscribe(request_id=request_id)
