from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer import model_observer

from apps.auto_salon_listings.models import AutoSalonListingModel
from apps.auto_salon_listings.serializers import AutoSalonListingSerializer


class AutoSalonListingConsumer(GenericAsyncAPIConsumer):
    def __init__(self, *args, **kwargs):
        self.group_name = 'auto_salon_listings'
        super().__init__(*args, **kwargs)


    async def connect(self):
        if not self.scope['user'].is_authenticated:
            await self.close()
            return

        await self.accept()
        await self.channel_layer.group_add(self.group_name, self.channel_name)



    @model_observer(AutoSalonListingModel, serializer_class=AutoSalonListingSerializer)
    async def listing_activity(self, message, action, subscribing_request_ids, **kwargs):
        for request_id in subscribing_request_ids:
            await self.reply(data=message, action=action, request_id=request_id)


    @action()
    async def subscribe_to_listing_model_changes(self, request_id, **kwargs):
        await self.listing_activity.subscribe(request_id=request_id)