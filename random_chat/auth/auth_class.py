from rest_framework.authentication import TokenAuthentication
from auth.models import AuthToken


class CustomTokenAuthentication(TokenAuthentication):
    keyword = 'Token'
    model = AuthToken