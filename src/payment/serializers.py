from rest_framework import serializers
from .models import (
    PaymentModel,
    ShippingModel, DeliveryModel
)


class UserPaymentSerailizer(serializers.ModelSerializer):
    class Meta:
        model = PaymentModel
        fields = '__all__'
        read_only_fields = ('user', 'issued_at', 'expiry_date', 'is_paid', )


class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingModel
        fields = '__all__'
        read_only_fields = ('created_at', )


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryModel
        fields = '__all__'
        read_only_fields = ('created_at', )
