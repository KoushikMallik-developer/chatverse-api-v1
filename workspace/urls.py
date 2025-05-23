from django.urls import path

from workspace.views.create_workspace import CreateWorkspaceView
from workspace.views.fetch_workspaces_view import FetchWorkspacesView

urlpatterns = [
    path(
        "get-all-workspaces", FetchWorkspacesView.as_view(), name="get-all-workspaces"
    ),
    path("create-workspace", CreateWorkspaceView.as_view(), name="create-workspace"),
]
