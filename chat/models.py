from django.db import models
from accounts.models import User

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


# Create your models here.
class Message(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mess_from')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mess_to')
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


    def notify_ws_clients(self):
        """
        Inform client there is a new message.
        """
        notification = {
            'type': 'chat_message',
            'message': '{}'.format(self.id)
        }

        channel_layer = get_channel_layer()
        print("user.id {}".format(self.owner.id))
        print("user.id {}".format(self.recipient.id))

        async_to_sync(channel_layer.group_send)("{}".format(self.owner.id), notification)
        async_to_sync(channel_layer.group_send)("{}".format(self.recipient.id), notification)

    def save(self, *args, **kwargs):
        """
        Trims white spaces, saves the message and notifies the recipient via WS
        if the message is new.
        """
        new = self.id
        self.body = self.body.strip()  # Trimming whitespaces from the body
        super(Message, self).save(*args, **kwargs)
        if new is None:
            self.notify_ws_clients()

    class Meta:
        ordering = ('-timestamp',)
