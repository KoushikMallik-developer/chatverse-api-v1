from django.urls import path

from channel.views.create_channel import CreateChannelView
from channel.views.fetch_channels import FetchAllChannelsView


urlpatterns = [
    path(
        "get-all-channels/<str:workspace_id>",
        FetchAllChannelsView.as_view(),
        name="get-all-channels",
    ),
    path("", CreateChannelView.as_view(), name="create-channel"),
]
