from django.urls import path

from .views import UserListCreateView, UserRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('/registration', UserListCreateView.as_view(), name='user_create'),
    path('', UserListCreateView.as_view(), name='users_list'),
    path('/<int:pk>', UserRetrieveUpdateDestroyAPIView.as_view(), name='user_detail_profile'),
]
