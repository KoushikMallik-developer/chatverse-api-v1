from django.db import models

from auth_api.models.base_models.base_model import GenericBaseModel
from auth_api.models.user_models.user import User
from message.models.message import Message


class Reaction(GenericBaseModel):
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="reactions"
    )  # Message being reacted to
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reactions"
    )  # Who reacted
    emoji = models.CharField(
        max_length=10, null=False, blank=False
    )  # The reaction (e.g., 👍, ❤️)

    def __str__(self):
        return f"{self.user.username} reacted with {self.emoji}"
