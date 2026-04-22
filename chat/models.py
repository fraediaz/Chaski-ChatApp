from django.conf import settings
from django.db import models


class Channel(models.Model):
	name = models.CharField(max_length=100)
	slug = models.SlugField(unique=True)
	description = models.TextField(blank=True)
	owner = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='owned_channels',
	)
	created_by_name = models.CharField(max_length=60, default='anon')
	is_public = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['name']

	def __str__(self):
		return self.name


class Message(models.Model):
	channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='messages')
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='messages',
	)
	nickname = models.CharField(max_length=60, blank=True)
	content = models.TextField(max_length=1000)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['created_at']

	@property
	def author_name(self):
		if self.user:
			return self.user.get_username()
		return self.nickname or 'anon'

	def __str__(self):
		return f'{self.author_name}: {self.content[:40]}'
