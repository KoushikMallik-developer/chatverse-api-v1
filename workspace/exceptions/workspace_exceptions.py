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
