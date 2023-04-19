import json
from chat.consumers import ChatConsumer



async def svc_chat_connect_to_room(consumer_obj: ChatConsumer):
    consumer_obj.room_name = consumer_obj.scope["url_route"]["kwargs"]["room_name"]
    consumer_obj.room_group_name = "chat_%s" % consumer_obj.room_name

    consumer_obj.user = consumer_obj.scope['user']
   

    if not consumer_obj.user.is_authenticated:
        print("\n\nNot Authentcated")
        print(consumer_obj.user)
        await consumer_obj.close()
        return

    print("\n\nhere2")
    # Add the user to the queue
    # self.queue.append(self)
    consumer_obj.queue.append([consumer_obj, consumer_obj.user]) # adding user's consumer object and user object to the queue

    print("\n\nhere3")
    
    print("\n\nhere4")
    await consumer_obj.accept()

    if len(consumer_obj.queue) >= 2:
        print("\n\nhere5")
        await consumer_obj.start_chat()
    else:
        print("\n\nhere6")
        await consumer_obj.send(text_data=json.dumps({
            'message': 'You are in the queue. Please wait for another user to join.'
        }))


async def svc_chat_disconnect_from_room(consumer_obj: ChatConsumer):
    # Remove the user from the queue if they are in it
    if consumer_obj in consumer_obj.queue:
        consumer_obj.queue.remove(consumer_obj)

    # Leave room group
    await consumer_obj.channel_layer.group_discard(consumer_obj.room_group_name, consumer_obj.channel_name)


async def svc_chat_receive_message(consumer_obj: ChatConsumer, message_data: dict):
    message = message_data["message"]
    sender = message_data["sender"]
    recepient = message_data["recepient"]

    # Send message to room group
    await consumer_obj.channel_layer.group_send(
        consumer_obj.room_group_name, {"type": "chat_message", "message": message}
    )

    # Store the message in the database
    await consumer_obj.store_message(sender, recepient, message)



# async def svc_chat_start_chat(consumer_obj: ChatConsumer):