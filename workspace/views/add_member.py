from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_api.services.handlers.exeption_handler_decorator import handle_exceptions
from auth_api.services.utils.auth_decorators import is_logged_in
from workspace.services.workspace_services import WorkspaceServices


class AddMemberView(APIView):
    renderer_classes = [JSONRenderer]

    @handle_exceptions
    @is_logged_in
    def post(self, request, workspace_id: str):
        """
        Add a member to the workspace.
        :param request: The HTTP request object.
        :param workspace_id: The ID of the workspace.
        :return: A JSON response with the added member data.
        """
        workspace = WorkspaceServices().add_member_to_workspace(
            user_id=request.user.id,
            workspace_id=workspace_id,
            members=request.data.get("members", []),
        )
        return Response(
            data={
                "data": workspace,
                "message": "Member(s) added to workspace successfully.",
            },
            status=status.HTTP_200_OK,
            content_type="application/json",
        )
