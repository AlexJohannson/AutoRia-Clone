from django.contrib.auth import get_user_model

from rest_framework import serializers

UserModel = get_user_model()

class EmailSerializers(serializers.Serializer):
    email = serializers.EmailField()
    


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['password']