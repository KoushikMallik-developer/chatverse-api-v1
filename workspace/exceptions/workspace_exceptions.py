import logging
from typing import Optional

from workspace.exceptions.base_exception import GenericBaseException


class WorkspaceAlreadyExists(GenericBaseException):
    def __init__(self, msg: Optional[str] = None):
        if not msg:
            self.msg = "Workspace with this name already exists."
        else:
            super().__init__(msg)
        logging.error(self.msg)


class PermissionDeniedError(GenericBaseException):
    def __init__(self, msg: Optional[str] = None):
        if not msg:
            self.msg = "You do not have permission to perform this action."
        else:
            super().__init__(msg)
        logging.error(self.msg)
