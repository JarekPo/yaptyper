from django.db import models

from chats.models import Chat


class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    nick_name = models.CharField(max_length=120)
    text = models.TextField()
    message_time = models.DateTimeField(null=True, default=None)

    def __str__(self):
        return f"{self.chat.room_name}-{self.nick_name}"
