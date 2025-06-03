from django.urls import path

from .views import ChatRoomDeleteView, ChatRoomDetailView, ChatRoomListView, MessageDeleteView

urlpatterns = [
    path('', ChatRoomListView.as_view(), name='chat-room-list'),
    path('/<int:pk>', ChatRoomDetailView.as_view(), name='chat-room-detail'),
    path('/delete/<int:pk>', ChatRoomDeleteView.as_view(), name='chat-room-delete'),
    path('/messages/delete/<int:pk>', MessageDeleteView.as_view(), name='message-delete'),
]
