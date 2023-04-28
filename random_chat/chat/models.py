from django.db import models

from account.models import UserProfile
from common.abstract_models import AbstractDateTimeStamp, AbstractExternalID


class Conversation(AbstractDateTimeStamp, AbstractExternalID):
    user1 = models.ForeignKey(UserProfile, related_name="user_conversation_1", on_delete=models.CASCADE)
    user2 = models.ForeignKey(UserProfile, related_name="user_conversation_2", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user1", "user2")

    def __str__(self):
        return f"{self.user1} and {self.user2} conversation"


class Message(AbstractDateTimeStamp):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(UserProfile, related_name="sender_messages", on_delete=models.CASCADE)
    recipient = models.ForeignKey(UserProfile, related_name="recipient_messages", on_delete=models.CASCADE)
    content = models.TextField()

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return f"{self.sender} to {self.recipient} --> {self.content}"
