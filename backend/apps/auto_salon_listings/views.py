from django.core.cache import cache
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.services.exchange_servise import get_exchange_rates
from core.services.listing_service import calculate_prices, update_listing_views
from core.services.listing_validation_service import contains_forbidden_word
from core.tasks import (
    avg_price_task,
    send_auto_salon_listing_publication_email_task,
    send_blocked_auto_salon_listing_email_task,
    send_deleted_auto_salon_listing_email_task,
    update_exchange_rates,
)
from drf_yasg.utils import swagger_auto_schema

from apps.auto_salon.models import AutoSalonModel
from apps.auto_salon_listings.filter import ListingAutoSalonFilter
from apps.auto_salon_listings.models import AutoSalonListingModel
from apps.auto_salon_listings.permissions import IsAdminOrSuperuser, IsSalonStaffOrAdmin
from apps.auto_salon_listings.serializers import AutoSalonListingPhotoSerializer, AutoSalonListingSerializer
from apps.salon_role.models import SalonRoleModels


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        security=[]
    )
)
class AutoSalonListingCreateApiView(ListCreateAPIView):
    """
        get:
            get all auto salon listings
        post:
            create new auto salon listing
    """

    serializer_class = AutoSalonListingSerializer
    filterset_class = ListingAutoSalonFilter

    def get_queryset(self):
        return AutoSalonListingModel.objects.filter(is_active=True)

    def get_permissions(self):
        return [IsSalonStaffOrAdmin()] if self.request.method == 'POST' else [AllowAny()]


    def perform_create(self, serializer):
        user = self.request.user


        try:
            auto_salon = AutoSalonModel.objects.get(user=user)
        except AutoSalonModel.DoesNotExist:
            try:
                salon_role = SalonRoleModels.objects.get(user=user)
                auto_salon = salon_role.auto_salon
            except SalonRoleModels.DoesNotExist:
                raise ValidationError("You are not assigned to any AutoSalon.")


        try:
            price = float(self.request.data.get('price'))
        except (TypeError, ValueError):
            raise ValidationError('Invalid or missing price')

        currency = self.request.data.get('currency')
        if currency not in ['USD', 'EUR', 'UAH']:
            raise ValidationError('Invalid or missing currency')

        price_usd, price_eur, price_uah = calculate_prices(price, currency)
        description = self.request.data.get('description', '')
        auto_salon_key = f'bad_word_attempts_{auto_salon.id}'

        if contains_forbidden_word(description):
            attempts = cache.get(auto_salon_key, 0) + 1
            cache.set(auto_salon_key, attempts, timeout=3600)

            if attempts >= 3:
                listing = serializer.save(
                    auto_salon=auto_salon,
                    currency=currency,
                    price=price,
                    price_usd=price_usd,
                    price_eur=price_eur,
                    price_uah=price_uah,
                    exchange_rate_used=get_exchange_rates()['updated'],
                    is_active=False,
                    bad_word_attempts=3,
                )

                send_blocked_auto_salon_listing_email_task.delay(listing.id)

                cache.delete(auto_salon_key)
                raise ValidationError('Listing is now inactive due to forbidden words. Manager notified.')
            else:
                attempts_left = 3 - attempts
                raise ValidationError(f'Listing contains forbidden words. You have {attempts_left} attempts left.')

        listing = serializer.save(
            auto_salon=auto_salon,
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
        send_auto_salon_listing_publication_email_task.delay(
            auto_salon.user.email,
            auto_salon.user.profile.name,
            listing.brand.brand,
            listing.car_model.car_model,
            price=str(listing.price),
        )

@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        security=[]
    )
)
class AutoSalonListingRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    """
        get:
            get auto salon listing by Id
        put:
            full upgrade auto salon listing by Id
        delete:
            delete auto salon listing by Id
    """

    serializer_class = AutoSalonListingSerializer
    http_method_names = ['get', 'put', 'delete']
    
    
    def get_permissions(self):
        return [AllowAny()] if self.request.method == 'GET' else [IsSalonStaffOrAdmin()]

    def get_queryset(self):
        return AutoSalonListingModel.objects.filter(is_active=True)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        update_listing_views(instance)

        serializer = self.get_serializer(instance, context={'request': request})
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        listing = self.get_object()
        send_deleted_auto_salon_listing_email_task.delay(
            listing.auto_salon.user.email,
            listing.auto_salon.user.profile.name,
            listing.brand.brand,
            listing.car_model.car_model,
            price=str(listing.price),
        )
        self.perform_destroy(listing)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddPhotoToListingView(UpdateAPIView):
    """
        put:
            put photo to auto salon listing
    """

    serializer_class = AutoSalonListingPhotoSerializer
    queryset = AutoSalonListingModel.objects.all()
    permission_classes = [IsSalonStaffOrAdmin]
    http_method_names = ['put']


    def perform_update(self, serializer):
        listing = self.get_object()
        listing.photo.delete()
        super().perform_update(serializer)

class AutoSalonListingInactiveList(ListAPIView):
    """
        get:
            get inactive auto salon listing list
    """

    serializer_class = AutoSalonListingSerializer
    permission_classes = (IsAdminOrSuperuser, )
    queryset = AutoSalonListingModel.objects.filter(is_active=False)
    http_method_names = ['get']

class DeleteInactiveAutoSalonListing(RetrieveUpdateDestroyAPIView):
    """
        delete:
            delete inactive auto salon listing by Id
    """

    serializer_class = AutoSalonListingSerializer
    queryset = AutoSalonListingModel.objects.filter(is_active=False)
    permission_classes = (IsAdminOrSuperuser, )
    http_method_names = ['delete']













