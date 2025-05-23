from django.db import models

from auth_api.models.base_models.base_model import GenericBaseModel
from auth_api.models.user_models.user import User
from channel.models.channel import Channel


class Workspace(GenericBaseModel):
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_workspaces"
    )  # Owner of the workspace
    members = models.ManyToManyField(
        User, related_name="workspaces"
    )  # Users in the workspace
    channels = models.ManyToManyField(
        Channel, related_name="workspaces"
    )  # Channels in the workspace
