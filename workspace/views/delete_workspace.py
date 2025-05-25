from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_api.services.handlers.exeption_handler_decorator import handle_exceptions
from auth_api.services.utils.auth_decorators import is_logged_in
from workspace.services.workspace_services import WorkspaceServices


class DeleteWorkspaceView(APIView):
    renderer_classes = [JSONRenderer]

    @handle_exceptions
    @is_logged_in
    def delete(self, request, workspace_id: str) -> Response:
        """
        Delete a workspace.
        :param request: The HTTP request object.
        :param workspace_id: The ID of the workspace to delete.
        :return: A JSON response indicating success or failure.
        """
        WorkspaceServices().delete_workspace(
            user_id=request.user.id, workspace_id=workspace_id
        )
        return Response(
            data={
                "message": "Workspace deleted successfully.",
            },
            status=status.HTTP_200_OK,
            content_type="application/json",
        )
