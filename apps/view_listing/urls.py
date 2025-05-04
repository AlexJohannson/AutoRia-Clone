from django.urls import path

from .views import CreateViewListingApiView, ViewStatisticsApiView

urlpatterns = [
    path('/view-stats', ViewStatisticsApiView.as_view(), name='view-stats'),
    path('/view-save', CreateViewListingApiView.as_view(), name='create-view'),
]
