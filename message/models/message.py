from django.db import models

from auth_api.models.base_models.base_model import GenericBaseModel
from auth_api.models.user_models.user import User
from channel.models.channel import Channel


class Message(GenericBaseModel):
    content = models.TextField(null=False, blank=False)  # Message content
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )  # Who sent the message
    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        related_name="messages",
        null=True,
        blank=True,
    )  # Belongs to a channel (optional)

    def __str__(self):
        return f"Message by {self.sender.username}: {self.content[:20]}"
