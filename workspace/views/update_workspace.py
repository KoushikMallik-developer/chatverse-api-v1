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


class UpdateWorkspaceView(APIView):
    renderer_classes = [JSONRenderer]

    @handle_exceptions
    @is_logged_in
    def post(self, request, workspace_id: str):
        """
        Update workspace details.
        """
        workspace = WorkspaceServices().update_workspace(
            data=CreateWorkspaceRequest(**request.data),
            workspace_id=workspace_id,
            user_id=request.user.id,
        )
        return Response(
            data=workspace,
            status=status.HTTP_200_OK,
            content_type="application/json",
        )
