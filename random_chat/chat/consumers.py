# chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer


"""
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        self.user = self.scope['user'] 

        print("\n\n####################################")
        print(self.room_name)
        print(self.room_group_name)
        print(self.user.is_authenticated)
        print(self.user)
        print("\n\n####################################")

        if not self.user.is_authenticated:
            await self.close() # await self.close(code=4401, reason="User is not authenticated") -  4401 indicates that the client lacks sufficient credentials to access the resource.
            return
            # await self.send(
            #     text_data=json.dumps({
            #         'type': 'authentication_error',
            #         'message': 'User is not authenticated'
            #     })
            # )
            # return

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
"""







from collections import deque
from asgiref.sync import async_to_sync, sync_to_async
from account.models import UserProfile, User
from .models import Message, Conversation
import asyncio



class ChatConsumer(AsyncWebsocketConsumer):
    queue = deque()

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        self.user = self.scope['user']

        if not self.user.is_authenticated:
            await self.close()
            return

        self.queue.append([self, self.user]) # adding user's consumer object and user object to the queue

        
        await self.accept()

        if len(self.queue) >= 2:
            await self.start_chat()
        else:
            await self.send(text_data=json.dumps({
                'message': 'You are in the queue. Please wait for another user to join.'
            }))
        

    async def disconnect(self, close_code):
        # Remove the user from the queue if they are in it
        if self in self.queue:
            self.queue.remove(self)

        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender = text_data_json["sender"]
        recepient = text_data_json["recepient"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

        # Store the message in the database
        await self.store_message(sender, recepient, message)

    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    async def start_chat(self):
        # Get the two users from the queue
        user1_consumer_obj, user1 = self.queue.popleft()
        user2_consumer_obj, user2 = self.queue.popleft()

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, user1_consumer_obj.channel_name)
        await self.channel_layer.group_add(self.room_group_name, user2_consumer_obj.channel_name)

        # Send message to room group
        message = {"message": f"Users {str(user1.get_external_id())}, {str(user2.get_external_id())} have been connected.",
                   "sender": str(user1.get_external_id()),
                   "recepient": str(user2.get_external_id()),
        }
        
        await self.receive(json.dumps(message))


    async def store_message(self, sender, recepient, message):
        # Store the message in the database
        user_1 = await sync_to_async(UserProfile.objects.get)(user__external_id=sender)
        user_2 = await sync_to_async(UserProfile.objects.get)(user__external_id=recepient)

        conversation, _ = await sync_to_async(Conversation.objects.get_or_create)(user1=user_1, user2=user_2)

        await sync_to_async(Message.objects.create)(
            conversation=conversation,
            sender=user_1,
            recipient=user_2,
            content=message
        )

    # @classmethod
    # async def check_queue(cls):
    #     while True:
    #         # Wait for 10 seconds
    #         await asyncio.sleep(10)

    #         # If there are two users in the queue, start a chat
    #         if len(cls.queue) == 2:
    #             await cls.start_chat()
    #         elif len(cls.queue) == 1:
    #             # Notify the user that there are no users available for chat
    #             user = cls.queue.popleft()
    #             await user.send(text_data=json.dumps({
    #                 'message': 'There are no users available for chat. Please try again later.'
    #             }))









# from services.chat import svc_chat_connect_to_room, svc_chat_disconnect_from_room, svc_chat_receive_message

# class ChatConsumer(AsyncWebsocketConsumer):
#     queue = deque()

#     async def connect(self):
#         await svc_chat_connect_to_room(self)


#     async def disconnect(self, close_code):
#         await svc_chat_disconnect_from_room(self)

#     async def receive(self, text_data):
#         await svc_chat_receive_message(self, json.loads(text_data))

#     async def chat_message(self, event):
#         message = event["message"]

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({"message": message}))

#     async def start_chat(self):
#         # Get the two users from the queue
#         user1_consumer_obj, user1 = self.queue.popleft()
#         user2_consumer_obj, user2 = self.queue.popleft()

#         # Join room group
#         # await self.channel_layer.group_add(self.room_group_name, user1.channel_name)
#         # await self.channel_layer.group_add(self.room_group_name, user2.channel_name)

#         # channel_name = user1.username + "_" + user2.username

#         await self.channel_layer.group_add(self.room_group_name, user1_consumer_obj.channel_name)
#         await self.channel_layer.group_add(self.room_group_name, user2_consumer_obj.channel_name)

#         # Send message to room group
#         # await self.channel_layer.group_send(
#         #     self.room_group_name, {"type": "chat_message", "message": "You have been connected to a user. You can start chatting now.'"}
#         # )

#         message = {"message": f"Users {str(user1.get_external_id())}, {str(user2.get_external_id())} have been connected.",
#                    "sender": str(user1.get_external_id()),
#                    "recepient": str(user2.get_external_id()),
#         }
        
#         # Here the ideal message format should be:
#         # message = {"message": "You have been connected to a user. You can start chatting now",
#         #            "user_1": str(user1.get_external_id()),
#         #            "user_2": str(user2.get_external_id()),
#         #            }

#         await self.receive(json.dumps(message))

#         # Notify the users that they have been connected
#         # await user1.send(text_data=json.dumps({
#         #     'message': 'You have been connected to a user. You can start chatting now.'
#         # }))
#         # await user2.send(text_data=json.dumps({
#         #     'message': 'You have been connected to a user. You can start chatting now.'
#         # }))

#     async def store_message(self, sender, recepient, message):
#         # Store the message in the database
#         # await async_to_sync(Message.objects.create)(
#         #     room_name=self.room_name,
#         #     user=self.user,
#         #     message=message
#         # )
#         # await Message.objects.create(
#         #     room_name=self.room_name,
#         #     user=self.user,
#         #     message=message
#         # )

#         user_1 = await sync_to_async(UserProfile.objects.get)(user__external_id=sender)
#         user_2 = await sync_to_async(UserProfile.objects.get)(user__external_id=recepient)

#         conversation, _ = await sync_to_async(Conversation.objects.get_or_create)(user1=user_1, user2=user_2)

#         await sync_to_async(Message.objects.create)(
#             conversation=conversation,
#             sender=user_1,
#             recipient=user_2,
#             content=message
#         )

#     @classmethod
#     async def check_queue(cls):
#         while True:
#             # Wait for 10 seconds
#             await asyncio.sleep(10)

#             # If there are two users in the queue, start a chat
#             if len(cls.queue) == 2:
#                 await cls.start_chat()
#             elif len(cls.queue) == 1:
#                 # Notify the user that there are no users available for chat
#                 user = cls.queue.popleft()
#                 await user.send(text_data=json.dumps({
#                     'message': 'There are no users available for chat. Please try again later.'
#                 }))



