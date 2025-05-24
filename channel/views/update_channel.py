from rest_framework.response import Response
from rest_framework.views import APIView

from auth_api.services.handlers.exeption_handler_decorator import handle_exceptions
from auth_api.services.utils.auth_decorators import is_logged_in
from channel.services.channel_services import ChannelServices


class UpdateChannelView(APIView):
    """
    Update Channel View
    """

    @handle_exceptions
    @is_logged_in
    def put(self, request, channel_id: str):
        """
        Handle PUT requests to update a channel.
        :param request: The HTTP request object.
        :param channel_id: The ID of the channel to update.
        :return: A JSON response with the updated channel data.
        """
        channel = ChannelServices().update_channel(
            user_id=request.user.id,
            channel_id=channel_id,
            data=request.data,
        )
        return Response(
            data={"data": channel, "message": "Channel updated successfully."},
            status=200,
            content_type="application/json",
        )
