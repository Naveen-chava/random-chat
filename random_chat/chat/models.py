from django.db import models
from django.contrib.auth.models import User

from account.models import UserProfile
from common.abstract_models import AbstractDateTimeStamp, AbstractExternalID



class Conversation(AbstractDateTimeStamp, AbstractExternalID):
    user1 = models.ForeignKey(UserProfile, related_name='user_conversation_1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(UserProfile, related_name='user_conversation_2', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"{self.user1} and {self.user2} conversation"


class Message(AbstractDateTimeStamp):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(UserProfile, related_name='sender_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(UserProfile, related_name='recipient_messages', on_delete=models.CASCADE)
    content = models.TextField()

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f"{self.sender} to {self.recipient} --> {self.content}"



"""
Creating Message object:
from django.shortcuts import get_object_or_404

user1_profile = get_object_or_404(UserProfile, id=1)
user2_profile = get_object_or_404(UserProfile, id=2)
conversation = Conversation.objects.get_or_create(user1=user1_profile, user2=user2_profile)

message = Message(
    conversation=conversation,
    sender=user1_profile,
    recipient=user2_profile,
    content='Hello!',
)
message.save()



Retreieving conversations:
conversation = Conversation.objects.get(id=1)
messages = conversation.messages.all()

"""