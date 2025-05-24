from typing import List

from auth_api.models.user_models.user import User
from workspace.exceptions.workspace_exceptions import PermissionDeniedError
from workspace.export_types.request_data_types.create_workspace_request_type import (
    CreateWorkspaceRequest,
)
from workspace.export_types.workspace_types.workspace import (
    ExportWorkspace,
    ExportWorkspaceList,
)
from workspace.models.workspace import Workspace
from workspace.serializers.create_workspace_serializer import CreateWorkspaceSerializer


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
            workspace = (
                ExportWorkspace(**workspace.model_to_dict()) if workspace else None
            )
            return workspace
        except Workspace.DoesNotExist:
            raise ValueError("Workspace does not exist")

    def create_workspace(self, data, user_id: str):
        """
        Create a new workspace
        :param data: CreateWorkshopRequest
        :param user_id: str
        :return: ExportWorkspace
        """
        workspace = CreateWorkspaceSerializer().create(
            data={
                "name": data.name,
                "description": data.description,
                "owner": user_id,
                "members": (
                    data.members
                    if data.members and isinstance(data.members, list)
                    else [user_id]
                ),
            }
        )
        workspace.members.add(user_id)
        workspace = ExportWorkspace(**workspace.model_to_dict())
        return workspace.model_dump()

    def update_workspace(
        self, data: CreateWorkspaceRequest, workspace_id: str, user_id: str
    ):
        """
        Update a workspace
        :param data: CreateWorkspaceRequest
        :param workspace_id: str
        :param user_id: str
        :return: ExportWorkspace
        """
        try:
            workspace = Workspace.objects.get(id=workspace_id, members__id=user_id)
            workspace.name = (
                data.name
                if data.name and isinstance(data.name, str)
                else workspace.name
            )
            workspace.description = (
                data.description
                if data.description and isinstance(data.description, str)
                else workspace.description
            )
            workspace.save()
            workspace = ExportWorkspace(**workspace.model_to_dict())
            return workspace.model_dump()
        except Workspace.DoesNotExist:
            raise ValueError("Workspace does not exist")

    def add_member_to_workspace(
        self, user_id: str, workspace_id: str, members: List[str]
    ) -> dict:
        """
        Add members to a workspace
        :param user_id: str
        :param workspace_id: str
        :param members: list of member IDs
        :return: dict
        """
        try:
            workspace = Workspace.objects.get(id=workspace_id)
            if str(user_id) != str(workspace.owner.id):
                raise PermissionDeniedError(
                    "Only Owner can add members to the workspace"
                )
            for member in members:
                if member in workspace.members.values_list("id", flat=True):
                    raise ValueError("User is already a member of the workspace")
                if not User.objects.filter(id=member).exists():
                    raise ValueError("User does not exist")
            for member in members:
                member = User.objects.get(id=member)
                workspace.members.add(member)
            workspace.save()
            return ExportWorkspace(**workspace.model_to_dict()).model_dump()
        except Workspace.DoesNotExist:
            raise ValueError("Workspace does not exist")

    def remove_member_from_workspace(
        self, user_id: str, workspace_id: str, members: List[str]
    ) -> dict:
        """
        Remove members from a workspace
        :param user_id: str
        :param workspace_id: str
        :param members: list of member IDs
        :return: dict
        """
        try:
            workspace = Workspace.objects.get(id=workspace_id)
            if str(user_id) != str(workspace.owner.id):
                raise PermissionDeniedError(
                    "Only Owner can remove members from the workspace"
                )
            for member in members:
                if not workspace.members.filter(id=member).exists():
                    raise ValueError("User is not a member of the workspace")
            for member in members:
                member = User.objects.get(id=member)
                workspace.members.remove(member)
            workspace.save()
            return ExportWorkspace(**workspace.model_to_dict()).model_dump()
        except Workspace.DoesNotExist:
            raise ValueError("Workspace does not exist")

    def delete_workspace(self, user_id: str, workspace_id: str):
        """
        Delete a workspace
        :param user_id: str
        :param workspace_id: str
        :return: dict
        """
        try:
            workspace = Workspace.objects.get(id=workspace_id)
            if str(user_id) != str(workspace.owner.id):
                raise PermissionDeniedError("Only Owner can delete the workspace")
            workspace.delete()
        except Workspace.DoesNotExist:
            raise ValueError("Workspace does not exist")
