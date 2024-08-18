from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import RegisterUserSerializer
from .tokens import AuthHelper

class RegisterUserView(GenericAPIView):
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        return Response(
            data={
                **serializer.data,
                **AuthHelper.get_tokens_for_user(user=user)
            }
        )
        