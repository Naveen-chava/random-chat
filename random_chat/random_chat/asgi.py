"""
ASGI config for chatapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

from django.conf import settings
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

import chat.routing

from chat.middlewares import CustomAuthMiddleware


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "random_chat.settings")

# django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        # Just HTTP for now. (We can add other protocols later.)
        "websocket": CustomAuthMiddleware(
            OriginValidator(AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns)), settings.ALLOWED_HOSTS)
        ),
    }
)
