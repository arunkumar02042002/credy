
from rest_framework_simplejwt.tokens import RefreshToken

class AuthHelper:

    @staticmethod
    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user=user)
        return {
            "access": str(refresh.access_token)
        }