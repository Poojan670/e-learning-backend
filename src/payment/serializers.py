from rest_framework import serializers
from .models import (
    ContactInfo, PaymentModel,
    ShippingModel, DeliveryModel
)


class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = '__all__'


class UserPaymentSerailizer(serializers.ModelSerializer):
    class Meta:
        model = PaymentModel
        fields = '__all__'
        read_only_fields = ('user', 'issued_at', 'expiry_date', 'is_paid')


class AnonymousPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentModel
        exclude = ('user')
        read_only_fields = ('issued_at', 'expiry_date', 'is_paid')


class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingModel
        fields = '__all__'
        read_only_fields = ('created_at')


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryModel
        fields = '__all__'
        read_only_fields = ('created_at')
