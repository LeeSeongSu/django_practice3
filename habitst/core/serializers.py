from django.contrib.auth.models import User
from appname.models import CustomUser
from shop.models import Item,Order
from django.conf import settings
from django.shortcuts import get_object_or_404
from core.models import MessageModel
from rest_framework.serializers import ModelSerializer, CharField
from core.views import RecipientView
from django.views.generic import TemplateView


class MessageModelSerializer(ModelSerializer):
    user = CharField(source='user.username', read_only=True)
    recipient = CharField(source='recipient.username')

    def create(self, validated_data):
        user = self.context['request'].user
        a = self.context['request'].GET('name')
        recipient = get_object_or_404(
            CustomUser, username=validated_data['recipient']['username'])
        msg = MessageModel(recipient=recipient,
                           body=validated_data['body'],
                           user=user)
        msg.save()
        return msg

    class Meta:
        model = MessageModel
        fields = ('id', 'user', 'recipient', 'timestamp', 'body')


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username',)

