from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_api.services.handlers.exeption_handler_decorator import handle_exceptions
from auth_api.services.utils.auth_decorators import is_logged_in
from channel.services.channel_services import ChannelServices


class FetchAllChannelsView(APIView):
    """
    Fetch all channels.
    """

    @handle_exceptions
    @is_logged_in
    def get(self, request, workspace_id: str):
        """
        Fetch all channels.
        :param request: The request object.
        :param workspace_id: The ID of the workspace to fetch channels from.
        :return: A JSON response with the list of channels.
        """
        channels = ChannelServices().fetch_all_channels(
            workspace_id=workspace_id, user_id=request.user.id
        )
        return Response(
            data={"data": channels, "message": "Channels fetched successfully"},
            status=status.HTTP_200_OK,
            content_type="application/json",
        )
