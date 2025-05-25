from auth_api.models.user_models.user import User
from channel.definitions import PUBLIC
from channel.export_types.channel_types.channel import ExportChannelList, ExportChannel
from channel.export_types.request_data_types.create_channel_request_type import (
    CreateChannelRequestType,
)
from channel.models.channel import Channel
from channel.serializers.create_channel_serializer import CreateChannelSerializer
from workspace.exceptions.workspace_exceptions import PermissionDeniedError
from workspace.models.workspace import Workspace


class ChannelServices:
    def fetch_all_channels(self, workspace_id: str, user_id: str) -> dict:
        """
        Fetch all channels.
        """
        workspace = (
            Workspace.objects.get(id=workspace_id)
            if Workspace.objects.filter(id=workspace_id).exists()
            else None
        )
        if not workspace:
            raise ValueError("Workspace does not exist.")
        else:
            if not workspace.members.filter(id=user_id).exists():
                raise ValueError("User is not a member of the workspace.")
        channels = Channel.objects.filter(
            workspace__id=workspace_id, members__id=user_id
        )
        return (
            ExportChannelList(
                channels=[
                    ExportChannel(**channel.model_to_dict()) for channel in channels
                ]
            )
            .model_dump()
            .get("channels", [])
        )

    def fetch_channel_by_id(self, channel_id: str, user_id: str) -> dict:
        """
        Fetch a channel by its ID.
        :param channel_id: The ID of the channel to fetch.
        """
        try:
            channel = (
                Channel.objects.get(id=channel_id, members__id=user_id)
                if Channel.objects.filter(id=channel_id, members__id=user_id).exists()
                else None
            )
            if not channel:
                raise ValueError("Channel does not exist or user is not a member.")
            return (
                ExportChannel(**channel.model_to_dict()).model_dump()
                if channel
                else None
            )
        except Channel.DoesNotExist:
            raise ValueError("Channel does not exist.")

    def create_channel(self, data: CreateChannelRequestType, user_id: str):
        """
        Create a new channel.
        :param channel_data: The data for the new channel.
        """
        channel = CreateChannelSerializer().create(
            data={**data.model_dump(), "user_id": user_id}
        )
        return ExportChannel(**channel.model_to_dict()).model_dump()

    def update_channel(self, user_id, channel_id, data) -> dict:
        """
        Update an existing channel.
        :param channel_id: The ID of the channel to update.
        :param user_id: The ID of the user making the update.
        :param channel_data: The updated data for the channel.
        """
        try:
            channel = Channel.objects.get(id=channel_id)
            if not channel:
                raise ValueError("Channel does not exist.")
            if not str(channel.workspace.owner.id) == str(user_id):
                raise PermissionDeniedError(
                    "User does not have permission to update this channel."
                )

            channel.name = data.get("name", channel.name)
            if Channel.objects.filter(name=channel.name).exists():
                raise ValueError(f"Channel with name {channel.name} already exists.")
            channel.description = data.get("description", channel.description)
            channel.save()
            return ExportChannel(**channel.model_to_dict()).model_dump()
        except Channel.DoesNotExist:
            raise ValueError("Channel does not exist or user is not a member.")

    def delete_channel(self, channel_id: str, user_id: str):
        """
        Delete a channel by its ID.
        :param channel_id: The ID of the channel to delete.
        """
        try:
            channel = (
                Channel.objects.get(id=channel_id, workspace__owner__id=user_id)
                if Channel.objects.filter(id=channel_id).exists()
                else None
            )
            if not channel:
                raise ValueError(
                    "Channel does not exist or User does not have permission to delete."
                )
            channel.delete()
        except Channel.DoesNotExist:
            raise ValueError("Channel does not exist.")

    def add_member_to_channel(self, channel_id: str, user_id: str, member_id: str):
        """
        Add a member to a channel.
        :param channel_id: The ID of the channel.
        :param user_id: The ID of the user making the request.
        :param member_id: The ID of the member to add.
        """
        try:
            channel = Channel.objects.get(id=channel_id)
            if channel.type == PUBLIC:
                raise ValueError("Cannot modify members in a public channel.")
            if not channel.members.filter(id=user_id).exists():
                raise PermissionDeniedError(
                    "User does not have permission to add members to this channel."
                )
            if not channel.members.filter(id=member_id).exists():
                if not User.objects.filter(id=member_id).exists():
                    raise ValueError("User does not exist.")
                member = User.objects.get(id=member_id)
                channel.members.add(member)
                channel.save()
                return ExportChannel(**channel.model_to_dict()).model_dump()
            else:
                raise ValueError("Member is already in the channel.")
        except Channel.DoesNotExist:
            raise ValueError("Channel does not exist.")

    def remove_member_from_channel(self, channel_id: str, user_id: str, member_id: str):
        """
        Remove a member from a channel.
        :param channel_id: The ID of the channel.
        :param user_id: The ID of the user making the request.
        :param member_id: The ID of the member to remove.
        """
        try:
            channel = Channel.objects.get(id=channel_id)
            if channel.type == PUBLIC:
                raise ValueError("Cannot remove members from a public channel.")
            if not channel.members.filter(id=user_id).exists():
                raise PermissionDeniedError(
                    "User does not have permission to remove members from this channel."
                )
            if channel.members.filter(id=member_id).exists():
                member = User.objects.get(id=member_id)
                channel.members.remove(member)
                channel.save()
                return ExportChannel(**channel.model_to_dict()).model_dump()
            else:
                raise ValueError("Member is not in the channel.")
        except Channel.DoesNotExist:
            raise ValueError("Channel does not exist.")
