from typing import Optional

from rest_framework import serializers

from auth_api.models.user_models.user import User
from workspace.exceptions.workspace_exceptions import WorkspaceAlreadyExists
from workspace.models.workspace import Workspace


class CreateWorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace  # Replace with your actual model
        fields = "__all__"

    def validate(self, data: dict) -> Optional[bool]:
        if not (
            data.get("name")
            and data.get("description")
            and isinstance(data.get("name"), str)
            and isinstance(data.get("description"), str)
        ):
            raise ValueError(
                "Name and description should not be empty and should be strings."
            )
        else:
            if Workspace.objects.filter(
                name=data.get("name"), members__id=data.get("owner")
            ).exists():
                raise WorkspaceAlreadyExists(
                    f"Workspace with name {data.get('name')} already exists."
                )
        if data.get("owner") is None:
            raise ValueError("Owner should not be empty.")
        else:
            if not User.objects.filter(id=data.get("owner")).exists():
                raise ValueError("Owner does not exist.")
        if data.get("members") is not None:
            if not isinstance(data.get("members"), list):
                raise ValueError("Members should be a list.")
            for member in data.get("members"):
                if not User.objects.filter(id=member).exists():
                    raise ValueError(f"Member {member} does not exist.")
        else:
            data["members"] = [data["owner"]]
        return True

    def create(self, data: dict) -> dict:
        if self.validate(data):
            name = data.get("name")
            description = data.get("description")
            owner = User.objects.get(id=data.get("owner"))
            members = data.get("members")
            # Create the workspace instance
            workspace = Workspace.objects.create(
                name=name, description=description, owner=owner
            )
            # Add members to the workspace
            members = [User.objects.get(id=member) for member in members]
            workspace.members.set(members)
            return workspace
