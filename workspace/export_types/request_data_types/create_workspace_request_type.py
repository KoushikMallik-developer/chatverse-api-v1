from typing import Optional, List

from pydantic import BaseModel


class CreateWorkspaceRequest(BaseModel):
    """
    Request data type for creating a new workspace.
    """

    name: str
    description: str
    members: Optional[List[str]] = []
