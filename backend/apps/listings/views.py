from datetime import timedelta

from django.utils.timezone import now

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from core.services.exchange_servise import get_exchange_rates
from core.tasks import avg_price_task, update_exchange_rates

from apps.sellers.models import SellersModel

from .models import ListingSellersModel
from .permissions import IsOwnerOrAdmin
from .serializer import ListingPhotoSerializer, ListingSerializer


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


        try:
            price = float(self.request.data.get('price'))
        except (TypeError, ValueError):
            raise ValidationError("Invalid or missing price.")

        currency = self.request.data.get('currency')
        if currency not in ['USD', 'EUR', 'UAH']:
            raise ValidationError("Invalid or missing currency.")

        rates = get_exchange_rates()


        if currency == 'USD':
            price_usd = price
            price_uah = round(price * rates['USD_UAH'], 2)
            price_eur = round(price * rates['USD_EUR'], 2)
        elif currency == 'EUR':
            price_eur = price
            price_uah = round(price * rates['EUR_UAH'], 2)
            price_usd = round(price * rates['EUR_USD'], 2)
        elif currency == 'UAH':
            price_uah = price
            price_usd = round(price / rates['USD_UAH'], 2)
            price_eur = round(price / rates['EUR_UAH'], 2)


        serializer.save(
            seller=seller,
            currency=currency,
            price_uah=price_uah,
            price_usd=price_usd,
            price_eur=price_eur,
            exchange_rate_used=rates['updated']
        )

        update_exchange_rates.apply_async()
        avg_price_task.apply_async()

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


        is_premium = hasattr(instance.seller, 'premium_account')

        if is_premium:

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
            instance.save(update_fields=['views', 'daily_views', 'weekly_views', 'monthly_views', 'last_view_date'])


        serializer = self.get_serializer(instance, context={'request': request})
        data = serializer.data

        return Response(data)




class AddPhotoToListingView(UpdateAPIView):
    serializer_class = ListingPhotoSerializer
    queryset = ListingSellersModel.objects.all()
    permission_classes = [IsOwnerOrAdmin, IsAuthenticated]
    http_method_names = ['put']

    def perform_update(self, serializer):
        listing = self.get_object()
        listing.photo.delete()
        super().perform_update(serializer)


