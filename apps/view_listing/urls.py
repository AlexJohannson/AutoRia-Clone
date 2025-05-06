from django.urls import path

from .views import CreateViewListingApiView, ViewStatisticsApiView

urlpatterns = [
    path('/view-stats', ViewStatisticsApiView.as_view(), name='view_statistic'),
    path('/view-save', CreateViewListingApiView.as_view(), name='view_statistic_save'),
]
