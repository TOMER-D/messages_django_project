from django.urls import path
from . import views


urlpatterns = [
    path('write_message', views.write_message, name='write_message_view'),
    path('read_message', views.read_message, name='read_message'),
    path('messages_per_receiver', views.get_messages_per_receiver, name='messages_per_receiver'),
    path('unread_per_receiver', views.get_unread_per_receiver, name='unread_per_receiver'),
    path('delete_message', views.delete_message, name='delete_message'),
]