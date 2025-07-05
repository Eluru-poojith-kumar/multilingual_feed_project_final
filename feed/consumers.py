from channels.generic.websocket import AsyncWebsocketConsumer
import json

def is_spam(message):
    bad_words = ['spam', 'buy now', 'click here']
    return any(word in message.lower() for word in bad_words)

def sentiment(message):
    if any(word in message.lower() for word in ['good', 'great', 'happy']):
        return 'positive'
    elif any(word in message.lower() for word in ['bad', 'sad', 'angry']):
        return 'negative'
    return 'neutral'

class FeedConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("feed_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("feed_group", self.channel_name)

    async def receive(self, text_data):
        message = text_data.strip()
        if is_spam(message):
            return
        feedback = {
            "original": message,
            "sentiment": sentiment(message)
        }
        await self.channel_layer.group_send(
            "feed_group",
            {
                "type": "broadcast_message",
                "message": feedback,
            }
        )

    async def broadcast_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))

