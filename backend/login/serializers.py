# serializers.py

from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import UserProfile
from django.core.validators import validate_email


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'first_name', 'last_name')


class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField(validators=[validate_email])
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
