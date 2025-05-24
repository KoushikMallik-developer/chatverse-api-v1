import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel

from auth_api.export_types.user_types.export_user import ExportUser
from workspace.export_types.workspace_types.workspace import ExportWorkspace


class ExportChannel(BaseModel):
    """
    Export Channel model.
    This model is used to export channel data.
    """

    id: UUID
    name: str
    description: Optional[str] = None
    type: str  # e.g., 'public', 'private', 'direct'
    workspace: Optional[ExportWorkspace]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    members: List[ExportUser] = []

    def __init__(self, **kwargs):
        if "workspace" in kwargs:
            kwargs["workspace"] = ExportWorkspace(**kwargs["workspace"].model_to_dict())
        if "members" in kwargs:
            kwargs["members"] = [
                ExportUser(**member.model_to_dict())
                for member in kwargs["members"].all()
            ]
        super().__init__(**kwargs)


class ExportChannelList(BaseModel):
    """
    Export Channel List model.
    This model is used to export a list of channels.
    """

    channels: List[ExportChannel]
