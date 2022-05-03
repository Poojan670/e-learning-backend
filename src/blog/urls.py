from django.urls import path, include
from . import views
from rest_framework import routers


app_name = "blog"

router = routers.DefaultRouter()
router.register(r'blogs', views.BlogView, basename='blogs')

urlpatterns = [
    path('', include(router.urls)),
]
