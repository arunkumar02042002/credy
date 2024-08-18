from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterUserSerializer, LoginUserSerializer
from .tokens import AuthHelper

class RegisterUserView(GenericAPIView):
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        return Response({
            **AuthHelper.get_tokens_for_user(user=user)
        }, status=status.HTTP_201_CREATED)

class LoginUserView(GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        return Response({
            **AuthHelper.get_tokens_for_user(user=user)
        }, status=status.HTTP_200_OK)
