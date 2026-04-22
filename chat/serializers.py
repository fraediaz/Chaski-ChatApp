from django.utils.text import slugify
from rest_framework import serializers

from .models import Channel, Message


class ChannelSerializer(serializers.ModelSerializer):
    owner_username = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Channel
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'is_public',
            'created_by_name',
            'owner_username',
            'created_at',
        ]
        read_only_fields = ['id', 'owner_username', 'created_at']
        extra_kwargs = {
            'slug': {'required': False},
            'created_by_name': {'required': False},
        }

    def get_owner_username(self, obj):
        return obj.owner.get_username() if obj.owner else None

    def validate(self, attrs):
        request = self.context.get('request')
        if request and not request.user.is_authenticated and not attrs.get('created_by_name'):
            raise serializers.ValidationError(
                {'created_by_name': 'Es obligatorio para usuarios anonimos.'}
            )
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['owner'] = request.user
            validated_data['created_by_name'] = request.user.get_username()

        if not validated_data.get('slug'):
            base_slug = slugify(validated_data['name']) or 'canal'
            slug_candidate = base_slug
            index = 2

            while Channel.objects.filter(slug=slug_candidate).exists():
                slug_candidate = f'{base_slug}-{index}'
                index += 1

            validated_data['slug'] = slug_candidate

        return super().create(validated_data)


class MessageSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(read_only=True)

    class Meta:
        model = Message
        fields = [
            'id',
            'channel',
            'user',
            'nickname',
            'author_name',
            'content',
            'created_at',
        ]
        read_only_fields = ['id', 'user', 'author_name', 'created_at']

    def validate(self, attrs):
        request = self.context.get('request')
        if request and not request.user.is_authenticated and not attrs.get('nickname'):
            raise serializers.ValidationError(
                {'nickname': 'Para usuarios anonimos debes enviar nickname.'}
            )
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
            validated_data['nickname'] = ''
        return super().create(validated_data)
