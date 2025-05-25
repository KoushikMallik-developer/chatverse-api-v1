from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_api.services.handlers.exeption_handler_decorator import handle_exceptions
from auth_api.services.utils.auth_decorators import is_logged_in
from channel.services.channel_services import ChannelServices


class AddMemberToChannelView(APIView):
    """
    View to add a member to a channel.
    """

    @handle_exceptions
    @is_logged_in
    def post(self, request, channel_id: str) -> Response:
        """
        Handle POST request to add a member to a channel.
        """
        channel = ChannelServices().add_member_to_channel(
            channel_id=channel_id,
            user_id=request.user.id,
            member_id=request.data.get("member_id"),
        )
        return Response(
            data={
                "data": channel,
                "message": "Member added to channel successfully.",
            },
            status=status.HTTP_200_OK,
            content_type="application/json",
        )
