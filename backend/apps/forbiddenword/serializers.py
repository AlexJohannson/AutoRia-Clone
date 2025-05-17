from rest_framework import serializers

from apps.forbiddenword.models import Forbiddenwords


class ForbiddenWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forbiddenwords
        fields = ('id', 'word')