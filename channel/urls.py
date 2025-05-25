from django.urls import path

from channel.views.add_member_to_channel import AddMemberToChannelView
from channel.views.create_channel import CreateChannelView
from channel.views.delete_channel import DeleteChannelView
from channel.views.fetch_channels import FetchAllChannelsView
from channel.views.get_channel_by_id import GetChannelByIDView
from channel.views.remove_member_from_channel import RemoveMemberFromChannelView
from channel.views.update_channel import UpdateChannelView

urlpatterns = [
    path(
        "get-all-channels/<str:workspace_id>",
        FetchAllChannelsView.as_view(),
        name="get-all-channels",
    ),
    path(
        "<str:channel_id>",
        UpdateChannelView.as_view(),
        name="update-channel",
    ),
    path(
        "add-member-to-channel/<str:channel_id>",
        AddMemberToChannelView.as_view(),
        name="add-member-to-channel",
    ),
    path(
        "remove-member-from-channel/<str:channel_id>",
        RemoveMemberFromChannelView.as_view(),
        name="remove-member-from-channel",
    ),
    path(
        "delete-channel/<str:channel_id>",
        DeleteChannelView.as_view(),
        name="delete-channel",
    ),
    path(
        "get-channel/<str:channel_id>",
        GetChannelByIDView.as_view(),
        name="get-channel-by-id",
    ),
    path("", CreateChannelView.as_view(), name="create-channel"),
]
