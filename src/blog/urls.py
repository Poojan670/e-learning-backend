from django.urls import path, include
from . import views
from rest_framework import routers


app_name = "blog"

router = routers.DefaultRouter()
router.register(r'blogs', views.BlogView, basename='blogs')
router.register(r'sub-blogs', views.SubBlogView, basename='sub-blogs')

urlpatterns = [
    path('', include(router.urls)),
    path('published/', views.PublishedBlogsList.as_view(), name='published-blogs')
]
