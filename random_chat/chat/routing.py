# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]

"""
(?P<room_name>\w+) is a named group that matches one or more word characters (letters, digits, and underscores). The group is named room_name.

/$ matches the end of the string. The URL ends with a forward slash.
"""
