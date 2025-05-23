from django.urls import path

from workspace.views.fetch_workspaces_view import FetchWorkspacesView

urlpatterns = [
    path(
        "get-all-workspaces", FetchWorkspacesView.as_view(), name="get-all-workspaces"
    ),
]
