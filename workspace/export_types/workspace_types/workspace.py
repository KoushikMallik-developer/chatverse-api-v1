from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from auth_api.export_types.user_types.export_user import ExportUser


class ExportWorkspace(BaseModel):
    """
    Export workspace model
    """

    id: Optional[UUID]
    name: str
    description: str
    owner: ExportUser
    members: List[ExportUser]
    created_at: datetime
    updated_at: datetime

    def __init__(self, **kwargs):
        """
        Initialize ExportWorkspace with optional id
        :param with_id: If True, include id in the model
        :param kwargs:
        """
        if "owner" in kwargs:
            kwargs["owner"] = ExportUser(**kwargs["owner"].model_to_dict())
        if "members" in kwargs:
            kwargs["members"] = [
                ExportUser(**member.model_to_dict())
                for member in kwargs["members"].all()
            ]
        super().__init__(**kwargs)


class ExportWorkspaceList(BaseModel):
    workspaces: List[ExportWorkspace]
