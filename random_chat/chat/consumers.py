import json
import uuid

from collections import deque

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from account.models import UserProfile
from chat.models import Message, Conversation


class ChatConsumer(AsyncWebsocketConsumer):
    queue = deque()  # using a queue to store users waiting for a chat

    async def connect(self):
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close()
            return

        # adding user's consumer object and user object to the queue
        self.queue.append([self, self.user])

        await self.accept()

        # if there are two users in the queue, start the chat
        if len(self.queue) >= 2:
            await self.start_chat()
        else:
            await self.send(
                text_data=json.dumps({"message": "You are in the queue. Please wait for another user to join."})
            )

    async def disconnect(self, close_code):
        # Remove the user from the queue if they are in it
        if self in self.queue:
            self.queue.remove(self)

        # Leave room group
        try:
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        except AttributeError as e:
            pass

    async def receive(self, text_data: str):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender = text_data_json["sender"]
        recipient = text_data_json["recipient"]

        # Send message to room group
        await self.channel_layer.group_send(self.room_group_name, {"type": "chat_message", "message": message})

        # Store the message in the database
        await self.store_message(sender, recipient, message)

    async def chat_message(self, event):
        """
        This function is called when a message is sent to the room group associated with the chat.
        This function is not called directly by the ChatConsumer class. Instead, it is called by the Django Channels framework when a message is received by the group_send method in the receive function.
        """
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    async def start_chat(self):
        # Get the two users from the queue
        user1_consumer_obj, user1 = self.queue.popleft()
        user2_consumer_obj, user2 = self.queue.popleft()

        # Generate a unique room name for the chat
        self.room_group_name = f"chat_{uuid.uuid4()}"

        # Set the room group name attribute on both consumer objects
        user1_consumer_obj.room_group_name = self.room_group_name
        user2_consumer_obj.room_group_name = self.room_group_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, user1_consumer_obj.channel_name)
        await self.channel_layer.group_add(self.room_group_name, user2_consumer_obj.channel_name)

        # Send message to room group
        message = {
            "message": f"Users {str(user1.get_external_id())}, {str(user2.get_external_id())} have been connected.",
            "sender": str(user1.get_external_id()),
            "recipient": str(user2.get_external_id()),
        }

        await self.receive(json.dumps(message))

    async def store_message(self, sender: str, recipient: str, message: str):
        # Store the message in the database
        user_1 = await sync_to_async(UserProfile.objects.get)(user__external_id=sender)
        user_2 = await sync_to_async(UserProfile.objects.get)(user__external_id=recipient)

        conversation, _ = await sync_to_async(Conversation.objects.get_or_create)(user1=user_1, user2=user_2)

        await sync_to_async(Message.objects.create)(
            conversation=conversation, sender=user_1, recipient=user_2, content=message
        )
