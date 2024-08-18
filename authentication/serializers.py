
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

User = get_user_model()

class RegisterUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "username",
            "password",
        ]

        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_password(self, value):
        validate_password(value)
        return value
