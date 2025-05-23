from workspace.export_types.workspace_types.workspace import (
    ExportWorkspace,
    ExportWorkspaceList,
)
from workspace.models.workspace import Workspace


class WorkspaceServices:

    def fetch_workspaces(self, user_id: str):
        """
        Fetch workspaces for the user
        :param user_id: str
        :return: List[ExportWorkspace]
        """
        workspaces = Workspace.objects.filter(members__id=user_id)
        workspaces = ExportWorkspaceList(
            workspaces=[
                ExportWorkspace(**workspace.model_to_dict()) for workspace in workspaces
            ]
        )
        return workspaces.model_dump().get("workspaces") if workspaces else []

    def fetch_workspace(self, workspace_id: str, user_id: str):
        """
        Fetch workspaces for the user
        :param user_id: str
        :param workspace_id: str
        :return: Workspace
        """
        try:
            workspace = Workspace.objects.get(id=workspace_id, members__id=user_id)
            workspace = ExportWorkspace(**workspace[0]) if workspace else None
            return workspace
        except Workspace.DoesNotExist:
            raise ValueError("Workspace does not exist")
