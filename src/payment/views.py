from jsonschema import ValidationError
from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import PaymentModel, ShippingModel, DeliveryModel
from .serializers import (
    UserPaymentSerailizer,
    ShippingSerializer,
    DeliverySerializer
)


class PaymentView(viewsets.GenericViewSet):
    queryset = PaymentModel.objects.all().order_by('issued_at')
    serializer_class = UserPaymentSerailizer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(user=self.request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))

    def retrieve(self, request, pk):
        item = self.get_object()
        serializer = self.get_serializer(item)
        return Response(serializer.data)

    def destroy(self, request):
        item = self.get_object()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShippingView(viewsets.ModelViewSet):
    serializer_class = ShippingSerializer
    queryset = ShippingModel.objects.all().order_by('created_at')

    def create(self, request, pk, *args, **kwargs):
        try:
            obj = PaymentModel.objects.get(pk=pk)
        except PaymentModel.DoesNotExist:
            return ValidationError({"error": "Please provide correct Payment pk"})
        serializer = ShippingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(payment=obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeliveryView(viewsets.ModelViewSet):
    serializer_class = DeliverySerializer
    queryset = DeliveryModel.objects.all().order_by('created_at')

    def create(self, request, pk, *args, **kwargs):
        try:
            obj = PaymentModel.objects.get(pk=pk)
        except PaymentModel.DoesNotExist:
            return ValidationError({"error": "Please provide correct Payment pk"})
        serializer = ShippingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(payment=obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
