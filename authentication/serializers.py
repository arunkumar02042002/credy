from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

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
    
    def validate(self, attrs):
        attrs = super().validate(attrs)
        username = attrs['username']
        attrs['user'] = User.objects.create_user(**attrs)
        return attrs

    
class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, validators = [UnicodeUsernameValidator()])
    password = serializers.CharField(max_length=128)

    class Meta:
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        attrs = super().validate(attrs)
        username = attrs['username']
        password = attrs['password']

        user = authenticate(request=self.context.get('request'),
                            username=username, password=password)
        
        if not user:
            msg = _('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
