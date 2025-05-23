from typing import Optional, List

from pydantic import BaseModel


class CreateWorkshopRequest(BaseModel):
    """
    Request data type for creating a new workspace.
    """

    name: str
    description: str
    members: Optional[List[str]] = []
