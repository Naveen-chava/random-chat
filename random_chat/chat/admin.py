from django.contrib import admin

from chat.models import Message, Conversation


models = [Message, Conversation]
admin.site.register(models)
