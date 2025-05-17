from django.urls import path

from .views import (
    AddPhotoToListingView,
    DeleteInactiveListingsView,
    ListInactiveListingView,
    ListingListCreateView,
    ListingRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('', ListingListCreateView.as_view(), name='listing_list'),
    path('/<int:pk>', ListingRetrieveUpdateDestroyView.as_view(), name='listing_detail'),
    path('/photo/<int:pk>', AddPhotoToListingView.as_view(), name='add_photo'),
    path('/inactive', ListInactiveListingView.as_view(), name='listing_inactive'),
    path('/inactive/delete/<int:pk>', DeleteInactiveListingsView.as_view(), name='listing_inactive_delete'),
]
