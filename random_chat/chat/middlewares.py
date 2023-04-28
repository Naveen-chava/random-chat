from rest_framework.exceptions import AuthenticationFailed
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async

from common.auth_class import CustomTokenAuthentication


@database_sync_to_async
def get_user(token):
    user, _ = CustomTokenAuthentication().authenticate_credentials(token)
    return user or AnonymousUser()


class CustomAuthMiddleware:
    """
    Custom middleware that authenticates WebSocket connections using token authentication.
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        try:
            authorization = None
            for header in scope["headers"]:
                if (
                    header[0].decode() == "authorization"
                ):  # the values in header are bytes type, so using decode() to convert them to a regular string
                    authorization = header[1].decode().split()[1]
                    break
            scope["user"] = await get_user(authorization)
        except (IndexError, TypeError, AuthenticationFailed):
            scope["user"] = SimpleLazyObject(lambda: AnonymousUser())

        return await self.app(scope, receive, send)
