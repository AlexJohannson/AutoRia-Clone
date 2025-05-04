from datetime import timedelta

from django.utils.timezone import now

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.listings.models import ListingSellersModel

from .models import ViewListingModel
from .serializers import ViewListingSerializer


class CreateViewListingApiView(GenericAPIView):
    serializer_class = ViewListingSerializer

    def post(self, request, *args, **kwargs):
        listings_id = request.data.get('listings_id')

        try:
            listings_id = int(listings_id)
            listing = ListingSellersModel.objects.get(pk=listings_id)
        except (TypeError, ValueError):
            return Response({'error': 'Invalid listings_id'}, status=status.HTTP_400_BAD_REQUEST)
        except ListingSellersModel.DoesNotExist:

            return Response({'error': 'Listing not found'}, status=status.HTTP_404_NOT_FOUND)


        view_instance = ViewListingModel.objects.create(listings=listing, view=1, created_at=now())
        serializer = self.get_serializer(view_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ViewStatisticsApiView(GenericAPIView):
    serializer_class = ViewListingSerializer

    def get(self, request, *args, **kwargs):
        listings_id = request.query_params.get('listings_id')

        try:
            listings_id = int(listings_id)
        except (TypeError, ValueError):
            return Response({'error': 'Invalid listings_id'}, status=status.HTTP_400_BAD_REQUEST)

        today = now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)


        views = ViewListingModel.objects.filter(listings_id=listings_id)


        daily_views = views.filter(created_at__date=today).count()
        weekly_views = views.filter(created_at__date__gte=week_ago).count()
        monthly_views = views.filter(created_at__date__gte=month_ago).count()

        return Response({
            'Daily_views': daily_views,
            'Weekly_views': weekly_views,
            'Monthly_views': monthly_views,
        }, status=status.HTTP_200_OK)
