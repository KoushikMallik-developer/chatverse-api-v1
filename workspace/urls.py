from django.urls import path

from workspace.views.add_member import AddMemberView
from workspace.views.create_workspace import CreateWorkspaceView
from workspace.views.delete_workspace import DeleteWorkspaceView
from workspace.views.fetch_workspaces_view import FetchWorkspacesView
from workspace.views.remove_member import RemoveMemberFromWorkspaceView
from workspace.views.update_workspace import UpdateWorkspaceView

urlpatterns = [
    path(
        "get-all-workspaces", FetchWorkspacesView.as_view(), name="get-all-workspaces"
    ),
    path("create-workspace", CreateWorkspaceView.as_view(), name="create-workspace"),
    path(
        "update-workspace/<str:workspace_id>",
        UpdateWorkspaceView.as_view(),
        name="update-workspace",
    ),
    path(
        "add-member-to-workspace/<str:workspace_id>",
        AddMemberView.as_view(),
        name="add-member-to-workspace",
    ),
    path(
        "remove-member-from-workspace/<str:workspace_id>",
        RemoveMemberFromWorkspaceView.as_view(),
        name="remove-member-from-workspace",
    ),
    path(
        "delete-workspace/<str:workspace_id>",
        DeleteWorkspaceView.as_view(),
        name="delete-workspace",
    ),
]
