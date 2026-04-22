from django.views.generic import TemplateView
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Channel, Message
from .serializers import ChannelSerializer, MessageSerializer


class HomeView(TemplateView):
	template_name = 'chat/index.html'


class ChannelViewSet(viewsets.ModelViewSet):
	queryset = Channel.objects.all()
	serializer_class = ChannelSerializer
	lookup_field = 'slug'

	@action(detail=True, methods=['get', 'post'])
	def messages(self, request, slug=None):
		channel = self.get_object()

		if request.method.lower() == 'get':
			queryset = channel.messages.select_related('user').all()
			serializer = MessageSerializer(queryset, many=True)
			return Response(serializer.data)

		payload = request.data.copy()
		payload['channel'] = channel.id
		serializer = MessageSerializer(data=payload, context={'request': request})
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data, status=201)


class MessageViewSet(
	mixins.ListModelMixin,
	mixins.RetrieveModelMixin,
	viewsets.GenericViewSet,
):
	queryset = Message.objects.select_related('channel', 'user').all()
	serializer_class = MessageSerializer
