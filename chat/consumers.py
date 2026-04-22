import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Channel, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.channel_slug = self.scope['url_route']['kwargs']['slug']
        self.room_group_name = f'chat_{self.channel_slug}'

        channel_exists = await self._channel_exists(self.channel_slug)
        if not channel_exists:
            await self.close(code=4404)
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        payload = json.loads(text_data)
        content = (payload.get('content') or '').strip()
        nickname = (payload.get('nickname') or '').strip()

        if not content:
            return

        message_data = await self._save_message(content, nickname)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': message_data,
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['message']))

    @sync_to_async
    def _channel_exists(self, slug):
        return Channel.objects.filter(slug=slug).exists()

    @sync_to_async
    def _save_message(self, content, nickname):
        channel = Channel.objects.get(slug=self.channel_slug)
        user = self.scope.get('user')

        if user and user.is_authenticated:
            msg = Message.objects.create(channel=channel, user=user, content=content)
        else:
            msg = Message.objects.create(
                channel=channel,
                nickname=nickname or 'anon',
                content=content,
            )

        return {
            'id': msg.id,
            'channel': channel.id,
            'author_name': msg.author_name,
            'content': msg.content,
            'created_at': msg.created_at.isoformat(),
        }
