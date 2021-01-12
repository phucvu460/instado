from django.shortcuts import get_object_or_404
from chat.models import Message
from accounts.models import User
from rest_framework import serializers 


class MessageSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    recipient = serializers.CharField(source='recipient.username')

    class Meta:
        model = Message
        fields = ['id', 'owner', 'recipient', 'timestamp', 'body']

    def create(self, validated_data):
        user = self.context['request'].user
        recipient = get_object_or_404(User, username=validated_data['recipient']['username'])
        msg = Message(recipient=recipient,
                           body=validated_data['body'],
                           owner=user)
        msg.save()
        return msg
