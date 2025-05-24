from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_api.services.handlers.exeption_handler_decorator import handle_exceptions
from auth_api.services.utils.auth_decorators import is_logged_in
from workspace.export_types.request_data_types.create_workspace_request_type import (
    CreateWorkspaceRequest,
)
from workspace.services.workspace_services import WorkspaceServices


class CreateWorkspaceView(APIView):
    """
    View for creating a new workspace.
    """

    renderer_classes = [JSONRenderer]

    @handle_exceptions
    @is_logged_in
    def post(self, request):
        """
        Create a new workspace.
        :param request: The HTTP request object.
        :return: A JSON response with the created workspace data.
        """
        workspace = WorkspaceServices().create_workspace(
            data=CreateWorkspaceRequest(**request.data), user_id=request.user.id
        )
        return Response(
            data={
                "data": workspace,
                "message": "Workspace created successfully.",
            },
            status=status.HTTP_201_CREATED,
            content_type="application/json",
        )
