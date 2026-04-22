from django.contrib import admin

from .models import Channel, Message


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', 'owner', 'created_by_name', 'is_public', 'created_at')
	search_fields = ('name', 'slug', 'created_by_name')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
	list_display = ('id', 'channel', 'user', 'nickname', 'created_at')
	list_filter = ('channel', 'created_at')
	search_fields = ('content', 'nickname', 'user__username')
