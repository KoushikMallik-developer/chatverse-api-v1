from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_api.services.handlers.exeption_handler_decorator import handle_exceptions
from auth_api.services.utils.auth_decorators import is_logged_in
from message.services.message_services import MessageServices


class GetMessagesView(APIView):
    """
    View to get messages.
    """

    @handle_exceptions
    @is_logged_in
    def get(self, request, channel_id: str):
        """
        Handle GET request to fetch messages for a specific channel.
        :param request: The request object.
        :param channel_id: The ID of the channel to fetch messages from.
        :return: A JSON response with the list of messages.
        """
        messages = MessageServices().fetch_messages(
            channel_id=channel_id, user_id=request.user.id
        )
        return Response(
            data={"data": messages, "message": "Messages fetched successfully"},
            status=status.HTTP_200_OK,
            content_type="application/json",
        )
