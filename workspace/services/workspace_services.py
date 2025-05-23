from workspace.models.workspace import Workspace


class WorkspaceServices:

    def fetch_workspaces(self, user_id: str):
        """
        Fetch workspaces for the user
        :param user_id: str
        :return: List[Workspace]
        """
        workspaces = Workspace.objects.filter(members__id=user_id).values(
            "id", "name", "description", "owner__username"
        )
        return workspaces

    def fetch_workspace(self, workspace_id: str, user_id: str):
        """
        Fetch workspaces for the user
        :param user_id: str
        :param workspace_id: str
        :return: Workspace
        """
        workspace = Workspace.objects.filter(
            id=workspace_id, members__id=user_id
        ).values("id", "name", "description", "owner__username")
        return workspace
