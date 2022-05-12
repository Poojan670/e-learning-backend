from django.contrib import admin
from .models import PaymentModel, ShippingModel, DeliveryModel, CardModel

admin.site.register(PaymentModel)
admin.site.register(CardModel)
admin.site.register(ShippingModel)
admin.site.register(DeliveryModel)
