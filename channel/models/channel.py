from django.db import models

from auth_api.models.base_models.base_model import GenericBaseModel
from auth_api.models.user_models.user import User
from channel.definitions import CHANNEL_TYPES, PUBLIC
from message.models.message import Message
from workspace.models.workspace import Workspace


class Channel(GenericBaseModel):
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(
        max_length=10,
        choices=CHANNEL_TYPES,
        default=PUBLIC,
    )  # Public, Private, or Direct Message
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="channels",
    )  # Belongs to a workspace
    members = models.ManyToManyField(
        User, related_name="channels"
    )  # Users in the channel
    messages = models.ManyToManyField(
        Message, related_name="channels"
    )  # Messages in the channel

    def __str__(self):
        return self.name
