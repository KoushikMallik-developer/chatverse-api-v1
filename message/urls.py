from django.urls import path

from message.views.get_messages import GetMessagesView


urlpatterns = [
    path(
        "get-messages/<str:channel_id>", GetMessagesView.as_view(), name="get-messages"
    ),
]
