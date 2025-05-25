from channel.services.channel_services import ChannelServices
from message.export_types.message import ExportMessageList, ExportMessage
from message.models.message import Message


class MessageServices:
    """
    This class provides services related to messages in the application.
    """

    def fetch_messages(self, channel_id: str, user_id: str):
        """
        Fetch messages for a specific channel.
        :param channel_id: The ID of the channel to fetch messages from.
        :param user_id: The ID of the user requesting the messages.
        :return: A list of messages for the specified channel.
        """
        channel = ChannelServices().fetch_channel_by_id(
            channel_id=channel_id, user_id=user_id
        )
        if not channel:
            raise ValueError("Channel not found or user does not have access.")
        messages = Message.objects.filter(channel_id=channel_id).order_by("-created_at")
        return (
            ExportMessageList(
                messages=[
                    ExportMessage(**message.model_to_dict()) for message in messages
                ]
            )
            .model_dump()
            .get("messages", [])
        )
