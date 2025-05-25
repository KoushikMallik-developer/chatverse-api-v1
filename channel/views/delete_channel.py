from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_api.services.handlers.exeption_handler_decorator import handle_exceptions
from auth_api.services.utils.auth_decorators import is_logged_in
from channel.services.channel_services import ChannelServices


class DeleteChannelView(APIView):
    """
    View to delete a channel.
    """

    @handle_exceptions
    @is_logged_in
    def delete(self, request, channel_id: str):
        """
        Handle DELETE request to delete a channel.
        :param request: The request object.
        :param channel_id: The ID of the channel to be deleted.
        :return: A JSON response indicating success or failure.
        """
        ChannelServices().delete_channel(channel_id=channel_id, user_id=request.user.id)
        return Response(
            data={"message": "Channel deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
            content_type="application/json",
        )
