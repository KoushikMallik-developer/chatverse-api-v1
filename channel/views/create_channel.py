from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_api.services.handlers.exeption_handler_decorator import handle_exceptions
from auth_api.services.utils.auth_decorators import is_logged_in
from channel.export_types.request_data_types.create_channel_request_type import (
    CreateChannelRequestType,
)
from channel.services.channel_services import ChannelServices


class CreateChannelView(APIView):
    """
    View for creating a new channel.
    """

    @handle_exceptions
    @is_logged_in
    def post(self, request):
        """
        Handle POST requests to create a new channel.
        """
        channel = ChannelServices().create_channel(
            data=CreateChannelRequestType(**self.request.data), user_id=request.user.id
        )
        return Response(
            data={"data": channel, "message": "Channel created successfully."},
            status=status.HTTP_201_CREATED,
            content_type="application/json",
        )
