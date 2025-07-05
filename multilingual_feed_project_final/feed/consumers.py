from channels.generic.websocket import AsyncWebsocketConsumer
import json

class FeedConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("feed_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("feed_group", self.channel_name)

    async def receive(self, text_data):
        await self.channel_layer.group_send(
            "feed_group",
            {
                "type": "broadcast_message",
                "message": text_data,
            }
        )

    async def broadcast_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"]
        }))
