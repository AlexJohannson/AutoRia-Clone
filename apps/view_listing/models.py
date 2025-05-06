from django.db import models

from core.models import BaseModel

from apps.listings.models import ListingSellersModel


class ViewListingModel(BaseModel):
    class Meta:
        db_table = 'view_listing'



    listings = models.ForeignKey(ListingSellersModel, on_delete=models.CASCADE, related_name='view_listing')
    view = models.IntegerField()



        

