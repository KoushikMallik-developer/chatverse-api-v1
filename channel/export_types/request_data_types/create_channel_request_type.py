from typing import List, Optional

from pydantic import BaseModel

from channel.definitions import PUBLIC


class CreateChannelRequestType(BaseModel):
    name: str
    description: str
    type: Optional[str] = PUBLIC  # e.g., 'public', 'private', 'direct'
    workspace_id: str  # ID of the workspace to which the channel belongs
    members: Optional[List[str]] = []  # List of member IDs in the channel.List[str]
