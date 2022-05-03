from django.urls import path, include, re_path
from . import views
from rest_framework import routers


app_name = 'payment'

router = routers.DefaultRouter()
router.register(r'payment', views.PaymentView, basename='payments')

router.register(r'shipping', views.ShippingView, basename='shippings')

router.register(r'delivery', views.DeliveryView, basename='deliveries')

router.register(r'contact', views.ContactView, basename='contacts')


urlpatterns = [
    path('', include(router.urls)),
    # re_path(r'^ paypal /$', views.Payment.as_view(),
    #         name='PayPal Payment API')

]
