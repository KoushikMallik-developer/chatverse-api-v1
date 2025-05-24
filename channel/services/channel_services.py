from channel.export_types.channel_types.channel import ExportChannelList, ExportChannel
from channel.export_types.request_data_types.create_channel_request_type import (
    CreateChannelRequestType,
)
from channel.models.channel import Channel
from channel.serializers.create_channel_serializer import CreateChannelSerializer
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
        channel = (
            Channel.objects.get(id=channel_id, members__id=user_id)
            if Channel.objects.filter(id=channel_id, members__id=user_id).exists()
            else None
        )
        if not channel:
            raise ValueError(
                f"Channel with ID {channel_id} does not exist or user is not a member."
            )
        return (
            ExportChannel(**channel.model_to_dict()).model_dump() if channel else None
        )

    def create_channel(self, data: CreateChannelRequestType, user_id: str):
        """
        Create a new channel.
        :param channel_data: The data for the new channel.
        """
        channel = CreateChannelSerializer().create(
            data={**data.model_dump(), "user_id": user_id}
        )
        return ExportChannel(**channel.model_to_dict()).model_dump()

    def update_channel(self, channel_id, channel_data):
        """
        Update an existing channel.
        :param channel_id: The ID of the channel to update.
        :param channel_data: The updated data for the channel.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")

    def delete_channel(self, channel_id):
        """
        Delete a channel by its ID.
        :param channel_id: The ID of the channel to delete.
        """
        channel = (
            Channel.objects.get(id=channel_id)
            if Channel.objects.filter(id=channel_id).exists()
            else None
        )
        if not channel:
            raise ValueError(f"Channel with ID {channel_id} does not exist.")
        channel.delete()
