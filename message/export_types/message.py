from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ExportMessage(BaseModel):
    """
    Base class for export messages.
    This class is used to define the structure of messages that will be exported.
    """

    id: UUID
    content: str
    sender_id: UUID
    channel_id: UUID
    created_at: datetime
    updated_at: datetime

    def __init__(self, **kwargs):
        """
        Initialize the ExportMessage with the provided data.
        :param data: The data to initialize the ExportMessage.
        """
        if kwargs.get("sender"):
            kwargs["sender_id"] = kwargs.get("sender").id
        if kwargs.get("channel"):
            kwargs["channel_id"] = kwargs.get("channel").id
        super().__init__(**kwargs)


class ExportMessageList(BaseModel):
    """
    Base class for a list of export messages.
    This class is used to define the structure of a list of messages that will be exported.
    """

    messages: list[ExportMessage]
