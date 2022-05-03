from django.urls import path, include

from . import views
from rest_framework import routers

app_name = 'billing'

router = routers.DefaultRouter()
router.register(r'billings', views.BillingView, basename="billings")

urlpatterns = [
    path('', include(router.urls))
]
