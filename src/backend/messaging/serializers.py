from authentication.serializers import UserSerializer
from rest_framework import serializers

from authentication.models import Notification
from .models import TopicChatChannel, TopicChatMessage


class TopicChatChannelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicChatChannel
        fields = ("topic", "name", "description")


class TopicChatChannelSerializer(TopicChatChannelCreateSerializer):
    class Meta(TopicChatChannelCreateSerializer.Meta):
        fields = ("id", "name", "description", "created_at")


class TopicChatMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicChatMessage
        fields = ("author", "content")
        extra_kwargs = {"author": {"allow_null": False}} 


class TopicChatMessageSerializer(TopicChatMessageCreateSerializer):
    author = UserSerializer()

    class Meta(TopicChatMessageCreateSerializer.Meta):
        fields = ("id", "author", "channel", "content", "created_at", "edited_at")
        extra_kwargs = {"author": {"allow_null": True}} 


class NotificationSerializer(serializers.ModelSerializer):
    referenced_message = TopicChatMessageSerializer()

    class Meta:
        model = Notification
        fields = ('id', 'type', 'created_at', 'notification_content', 'referenced_message')
