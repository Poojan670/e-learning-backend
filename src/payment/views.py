from rest_framework import serializers, status, viewsets
from rest_framework.response import Response
from .models import ContactInfo, PaymentModel, ShippingModel, DeliveryModel
from .serializers import (
    ContactInfoSerializer, UserPaymentSerailizer,
    AnonymousPaymentSerializer, ShippingSerializer,
    DeliverySerializer
)
from rest_framework.views import APIView


class PaymentView(viewsets.GenericViewSet):
    queryset = PaymentModel.objects.all().order_by('issued_at')
    serializer_class = UserPaymentSerailizer

    def post(self, request, *args, **kwargs):
        if request.user:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            serializer.save(user=self.request.user)

            ContactInfo.objects.create(
                email=request.user.email,
                name=request.user.full_name
            )
        serializer = AnonymousPaymentSerializer(data=request.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))

    def retrieve(self, request, pk):
        item = self.get_object()
        if request.user:
            serializer = self.get_serializer(item)
        serializer = AnonymousPaymentSerializer(item)
        return Response(serializer.data)

    def destroy(self, request):
        item = self.get_object()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShippingView(viewsets.ModelViewSet):
    serializer_class = ShippingSerializer
    queryset = ShippingModel.objects.all().order_by('created_at')

    def perform_create(self, serializer):
        serializer.save(payment=self.request.user.payment)


class DeliveryView(viewsets.ModelViewSet):
    serializer_class = DeliverySerializer
    queryset = DeliveryModel.objects.all().order_by('created_at')

    def perform_create(self, serializer):
        serializer.save(payment=self.request.user.payment)


class ContactView(viewsets.ModelViewSet):
    serializer_class = ContactInfoSerializer
    queryset = ContactInfo.objects.all().order_by('id')
