from rest_framework import serializers

from .models import ViewListingModel


class ViewListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewListingModel
        fields = ('listings', 'created_at')