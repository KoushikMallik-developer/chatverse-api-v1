from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_api.services.handlers.exeption_handler_decorator import handle_exceptions
from auth_api.services.utils.auth_decorators import is_logged_in
from workspace.services.workspace_services import WorkspaceServices


class FetchWorkspacesView(APIView):
    renderer_classes = [JSONRenderer]

    @handle_exceptions
    @is_logged_in
    def get(self, request):
        """
        Fetch workspaces for the user
        :param request:
        :return: List of workspaces
        """
        workspaces = WorkspaceServices().fetch_workspaces(user_id=request.user.id)
        return Response(
            data=workspaces,
            status=status.HTTP_200_OK,
            content_type="application/json",
        )
