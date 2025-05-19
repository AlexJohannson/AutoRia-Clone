from django.core.cache import cache

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from core.services.exchange_servise import get_exchange_rates
from core.services.listing_service import calculate_prices, check_seller_listing_limit, update_listing_views
from core.services.listing_validation_service import contains_forbidden_word
from core.tasks import (
    avg_price_task,
    send_blocked_listing_due_bad_words_email_task,
    send_listing_deleted_email_task,
    send_listing_publication_email_task,
    update_exchange_rates,
)

from apps.sellers.models import SellersModel

from .models import ListingSellersModel
from .permissions import IsAdminOrSuperUser, IsOwnerOrAdmin
from .serializer import ListingPhotoSerializer, ListingSerializer


class ListingListCreateView(ListCreateAPIView):
    serializer_class = ListingSerializer

    def get_queryset(self):
        return ListingSellersModel.objects.filter(is_active=True)



    def get_permissions(self):
        return [IsAuthenticated()] if self.request.method == 'POST' else [AllowAny()]



    def perform_create(self, serializer):
        seller = SellersModel.objects.get(user=self.request.user)

        can_create, error_message = check_seller_listing_limit(seller)
        if not can_create:
            raise ValidationError(error_message, status.HTTP_400_BAD_REQUEST)

        try:
            price = float(self.request.data.get('price'))
        except (TypeError, ValueError):
            raise ValidationError("Invalid or missing price.")

        currency = self.request.data.get('currency')
        if currency not in ['USD', 'EUR', 'UAH']:
            raise ValidationError("Invalid or missing currency.")

        price_usd, price_eur, price_uah = calculate_prices(price, currency)

        description = self.request.data.get('description', '')
        seller_key = f'bad_word_attempts_{seller.id}'


        if contains_forbidden_word(description):
            attempts = cache.get(seller_key, 0) + 1
            cache.set(seller_key, attempts, timeout=3600)

            if attempts >= 3:

                listing = serializer.save(
                    seller=seller,
                    currency=currency,
                    price=price,
                    price_usd=price_usd,
                    price_eur=price_eur,
                    price_uah=price_uah,
                    exchange_rate_used=get_exchange_rates()['updated'],
                    is_active=False,
                    bad_word_attempts=3,
                )

                send_blocked_listing_due_bad_words_email_task.delay(listing.id)

                cache.delete(seller_key)
                raise ValidationError("Listing is now inactive due to forbidden words. Manager notified.")
            else:
                attempts_left = 3 - attempts
                raise ValidationError(f"Listing contains forbidden words. You have {attempts_left} attempts left.")


        listings = serializer.save(
            seller=seller,
            currency=currency,
            price=price,
            price_usd=price_usd,
            price_eur=price_eur,
            price_uah=price_uah,
            exchange_rate_used=get_exchange_rates()['updated'],
            is_active=True,
            bad_word_attempts=0,
        )

        update_exchange_rates.apply_async()
        avg_price_task.apply_async()
        send_listing_publication_email_task.delay(
            seller.user.email,
            seller.user.profile.name,
            listings.brand.brand,
            listings.car_model.car_model,
            price=str(listings.price),
        )



class ListingRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ListingSerializer
    http_method_names = ['get', 'put', 'delete']

    def get_permissions(self):
        return [AllowAny()] if self.request.method == 'GET' else [IsAuthenticated(), IsOwnerOrAdmin()]

    def get_queryset(self):
        return ListingSellersModel.objects.filter(is_active=True)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        update_listing_views(instance)

        serializer = self.get_serializer(instance, context={'request': request})
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        listing = self.get_object()
        send_listing_deleted_email_task.delay(
            listing.seller.user.email,
            listing.seller.user.profile.name,
            listing.brand.brand,
            listing.car_model.car_model,
            price=str(listing.price),
        )
        self.perform_destroy(listing)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddPhotoToListingView(UpdateAPIView):
    serializer_class = ListingPhotoSerializer
    queryset = ListingSellersModel.objects.all()
    permission_classes = [IsOwnerOrAdmin, IsAuthenticated]
    http_method_names = ['put']

    def perform_update(self, serializer):
        listing = self.get_object()
        listing.photo.delete()
        super().perform_update(serializer)



class ListInactiveListingView(ListAPIView):
    serializer_class = ListingSerializer
    permission_classes = [IsAdminOrSuperUser]
    queryset = ListingSellersModel.objects.filter(is_active=False)
    http_method_names = ['get']


class DeleteInactiveListingsView(RetrieveUpdateDestroyAPIView):
    serializer_class = ListingSerializer
    queryset = ListingSellersModel.objects.filter(is_active=False)
    permission_classes = [IsAdminOrSuperUser]
    http_method_names = ['delete']

