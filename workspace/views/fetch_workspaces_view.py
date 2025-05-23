from requests import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from auth_api.services.handlers.exception_handlers import ExceptionHandler
from auth_api.services.utils.auth_decorators import is_logged_in
from workspace.services.workspace_services import WorkspaceServices


class FetchWorkspacesView(APIView):
    renderer_classes = [JSONRenderer]

    @is_logged_in
    def post(self, request):
        """
        Fetch workspaces for the user
        :param request:
        :return:
        """
        try:
            workspaces = WorkspaceServices().fetch_workspaces(user_id=request.user.id)
            return Response(
                data={
                    "workspaces": workspaces,
                },
                status=status.HTTP_200_OK,
                content_type="application/json",
            )
        except Exception as e:
            return ExceptionHandler().handle_exception(e)
