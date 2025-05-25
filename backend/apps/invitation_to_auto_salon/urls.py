from django.urls import path

from apps.invitation_to_auto_salon.views import (
    JoinRequestApproveApiView,
    JoinRequestDeleteAPIView,
    JoinRequestListCreateView,
)

urlpatterns = [
    path('', JoinRequestListCreateView.as_view(), name='join_request_list_create'),
    path('/<int:pk>/approved', JoinRequestApproveApiView.as_view(), name='join_request_list_approve'),
    path('/delete/invitation/<int:pk>', JoinRequestDeleteAPIView.as_view(), name='join_request_list_delete'),
]