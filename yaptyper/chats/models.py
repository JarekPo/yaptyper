from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    room_name = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="chatrooms"
    )

    def __str__(self):
        return str(self.room_name)

    def get_messages(self):
        return self.messages.all()

    def save(self, *args, **kwargs):
        self.room_name = self.room_name.lower()
        super(Chat, self).save(*args, **kwargs)
