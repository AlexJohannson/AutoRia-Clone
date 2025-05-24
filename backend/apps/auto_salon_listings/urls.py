from django.urls import path

from apps.auto_salon_listings.views import (
    AddPhotoToListingView,
    AutoSalonListingCreateApiView,
    AutoSalonListingInactiveList,
    AutoSalonListingRetrieveUpdateDestroyApiView,
    DeleteInactiveAutoSalonListing,
)

urlpatterns = [
    path('', AutoSalonListingCreateApiView.as_view(), name='auto-salon-listing-create'),
    path('/<int:pk>', AutoSalonListingRetrieveUpdateDestroyApiView.as_view(), name='auto-salon-listing-retrieve'),
    path('/photo/<int:pk>', AddPhotoToListingView.as_view(), name='auto-salon-listing-add-photo-to-listing'),
    path('/inactive', AutoSalonListingInactiveList.as_view(), name='auto-salon-listing-inactive'),
    path('/inactive/delete/<int:pk>', DeleteInactiveAutoSalonListing.as_view(), name='auto-salon-listing-delete-inactive'),
]