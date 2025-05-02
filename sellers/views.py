from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from sellers.models import SellersModel
from django.forms import model_to_dict

from sellers.serializers import SellerSerializer





class SellersListCreateView(APIView):
    def get(self, *args, **kwargs):
        sellers = SellersModel.objects.all()
        serializer = SellerSerializer(instance=sellers, many=True)
        return Response(serializer.data, status.HTTP_200_OK)



    def post(self, *args, **kwargs):
        data = self.request.data

        serializer = SellerSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)








class SellersRetrieveUpdateDestroyView(APIView):
    def get(self, *args, **kwargs):
        pk = kwargs['pk']

        try:
            seller = SellersModel.objects.get(pk=pk)
        except SellersModel.DoesNotExist:
            return Response(f'Seller with ID {pk} not found')

        serializer = SellerSerializer(seller)

        return Response(serializer.data, status.HTTP_200_OK)





    def put(self, *args, **kwargs):
        pk = kwargs['pk']

        try:
            seller = SellersModel.objects.get(pk=pk)
        except SellersModel.DoesNotExist:
            return Response(f'Seller with ID {pk} not found')

        data = self.request.data
        serializer = SellerSerializer(instance=seller, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)






    def patch(self, *args, **kwargs):
        pk = kwargs['pk']

        try:
            seller = SellersModel.objects.get(pk=pk)
        except SellersModel.DoesNotExist:
            return Response(f'Seller with ID {pk} not found')

        data = self.request.data
        serializer = SellerSerializer(instance=seller, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)






    def delete(self, *args, **kwargs):
        pk = kwargs['pk']
        try:
            SellersModel.objects.get(pk=pk).delete()
        except SellersModel.DoesNotExist:
            return Response(f'Seller with ID {pk} not found')

        return Response(status=status.HTTP_204_NO_CONTENT)


