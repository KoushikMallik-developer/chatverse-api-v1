from __future__ import annotations
import datetime
import typing
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class ExportUser(BaseModel):
    id: Optional[UUID]
    email: str
    name: str
    account_type: Optional[str]
    dob: Optional[datetime.datetime]
    phone: Optional[str]
    image: Optional[str]
    is_active: bool
    is_deleted: bool
    is_admin: bool
    is_staff: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime

    def __init__(self, with_id: bool = True, **kwargs):
        if not with_id:
            kwargs["id"] = None
        super().__init__(**kwargs)


class ExportUserList(BaseModel):
    user_list: typing.List[ExportUser]
