from rest_framework import serializers

from auth_api.models.user_models.user import User
from channel.definitions import PUBLIC, DM
from channel.models.channel import Channel
from workspace.models.workspace import Workspace


class CreateChannelSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new channel.
    """

    class Meta:
        model = Channel  # Replace with the actual model class
        fields = "__all__"

    def validate(self, data):
        """
        Custom validation logic for the channel creation.
        """
        if not data.get("workspace_id"):
            raise ValueError("Workspace ID is required.")
        if not Workspace.objects.filter(id=data.get("workspace_id")).exists():
            raise ValueError("Workspace does not exist.")
        else:
            if (
                not Workspace.objects.get(id=data.get("workspace_id"))
                .members.filter(id=data.get("user_id"))
                .exists()
            ):
                raise ValueError("User is not a member of the workspace.")

        if not data.get("name"):
            raise ValueError("Channel name is required.")
        if Channel.objects.filter(
            name=data.get("name"), workspace_id=data.get("workspace_id")
        ).exists():
            raise ValueError(
                f"Channel with name {data.get('name')} already exists in the workspace"
            )
        if not data.get("description"):
            raise ValueError("Channel description is required.")
        if not data.get("type"):
            data["type"] = PUBLIC  # Default to PUBLIC if not provided
        if data.get("type") == PUBLIC:
            members = Workspace.objects.get(id=data.get("workspace_id")).members.all()
            data["members"] = members
        else:
            if data.get("type") == DM:
                if not data.get("members") or not isinstance(data.get("members"), list):
                    raise ValueError("Direct message requires one member.")
                if len(data.get("members")) != 1:
                    raise ValueError(
                        "Direct message can only be created between two users."
                    )
                if Channel.objects.filter(
                    type=DM,
                    members__id__in=[data.get("members")[0], data.get("user_id")],
                    workspace__id=data.get("workspace_id"),
                ).exists():
                    raise ValueError(
                        "A direct message channel already exists between the specified members."
                    )
                # If it's a DM channel, set the name and description
                data["name"] = f"DM with {data.get('members')[0], data.get('user_id')}"
                data["description"] = "Direct message channel"
            if (
                data.get("members")
                and isinstance(data.get("members"), list)
                and len(data.get("members")) > 0
            ):
                for member_id in data.get("members"):
                    if not User.objects.filter(id=member_id).exists():
                        raise ValueError(f"User with ID {member_id} does not exist.")
                    if (
                        not Workspace.objects.get(id=data.get("workspace_id"))
                        .members.filter(id=member_id)
                        .exists()
                    ):
                        raise ValueError(
                            f"User with ID {member_id} is not a member of the workspace."
                        )
                data["members"] = [
                    User.objects.get(id=member_id) for member_id in data.get("members")
                ]
        return data

    def create(self, data):
        data = self.validate(data)
        channel = Channel(
            name=data.get("name"),
            description=data.get("description"),
            type=data.get("type", PUBLIC),
            workspace_id=data.get("workspace_id"),
        )
        channel.save()
        channel.members.set(data.get("members", []))
        channel.members.add(User.objects.get(id=data.get("user_id")))
        return channel
