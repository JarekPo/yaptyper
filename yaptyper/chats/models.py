from django.db import models


class Chat(models.Model):
    room_name = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return str(self.room_name)

    def get_messages(self):
        return self.messages.all()
