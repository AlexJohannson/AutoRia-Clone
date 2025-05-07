from datetime import timedelta

from django.utils.timezone import now

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.sellers.models import SellersModel

from .models import ListingSellersModel
from .permissions import IsOwnerOrAdmin
from .serializer import ListingSerializer


class ListingListCreateView(ListCreateAPIView):
    serializer_class = ListingSerializer

    def get_queryset(self):
        return ListingSellersModel.objects.filter(is_active=True)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        seller = SellersModel.objects.get(user=self.request.user)


        if hasattr(seller, 'base_account'):
            listing_count = ListingSellersModel.objects.filter(seller=seller).count()
            if listing_count >= 1:
                raise ValidationError("Base account can only create one listing!", status.HTTP_400_BAD_REQUEST)

        serializer.save(seller=seller)


class ListingRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ListingSerializer
    http_method_names = ['get', 'put', 'delete']

    def get_permissions(self):

        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsOwnerOrAdmin()]

    def get_queryset(self):
        return ListingSellersModel.objects.filter(is_active=True)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        today = now().date()

        if hasattr(instance.seller, 'premium_account'):
            instance.views += 1

            if instance.last_view_date == today:
                instance.daily_views += 1
            else:
                instance.daily_views = 1

            if instance.last_view_date and instance.last_view_date >= today - timedelta(days=7):
                instance.weekly_views += 1
            else:
                instance.weekly_views = 1

            if instance.last_view_date and instance.last_view_date >= today - timedelta(days=30):
                instance.monthly_views += 1
            else:
                instance.monthly_views = 1

            instance.last_view_date = today
            instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

