from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Channel, Message


class ChatApiTests(APITestCase):
	def test_anonymous_can_create_channel(self):
		response = self.client.post(
			reverse('channel-list'),
			{'name': 'General', 'created_by_name': 'visitante'},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Channel.objects.count(), 1)

	def test_anonymous_can_post_message_with_nickname(self):
		channel = Channel.objects.create(name='General', slug='general', created_by_name='admin')
		response = self.client.post(
			reverse('channel-messages', kwargs={'slug': channel.slug}),
			{'content': 'Hola mundo', 'nickname': 'visitante'},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Message.objects.count(), 1)
