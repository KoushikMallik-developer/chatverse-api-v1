from django.contrib import admin

from message.models.message import Message
from message.models.reaction import Reaction

admin.site.register(Message)
admin.site.register(Reaction)
