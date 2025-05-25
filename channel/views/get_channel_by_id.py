from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_api.services.handlers.exeption_handler_decorator import handle_exceptions
from auth_api.services.utils.auth_decorators import is_logged_in
from channel.services.channel_services import ChannelServices


class GetChannelByIDView(APIView):
    """
    View to get a channel by its ID.
    """

    @handle_exceptions
    @is_logged_in
    def get(self, request, channel_id: str):
        """
        Handle GET request to retrieve a channel by its ID.
        :param request: The request object.
        :param channel_id: The ID of the channel to be retrieved.
        :return: A JSON response with the channel details.
        """
        channel = ChannelServices().fetch_channel_by_id(
            channel_id=channel_id, user_id=request.user.id
        )
        return Response(
            data={"data": channel, "message": "Channel fetched successfully."},
            status=status.HTTP_200_OK,
            content_type="application/json",
        )
