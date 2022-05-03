from django.urls import path
from .views import *


app_name = "examples"

header_urls = [
    path('header/', ExamplesHeaderCreateView.as_view(), name="header"),
    path('header/all', ExamplesHeaderListView.as_view(), name="header_list"),
    path('header/<pk>', ExamplesHeaderDetailView.as_view(), name="header_detail"),
]

example_urls = [
    path('examples/<pk>/',
         ExampleCategoryCreateView.as_view(), name="create"),

    path('examples/list/all/',

         ExampleCategoryListView.as_view(), name="list"),
    path('examples/detail/<pk>',
         ExampleCategoryDetailView.as_view(), name="detail"),
]

sub_urls = [
    path('sub/<pk>/',
         ExampleTitleCreateView.as_view(), name="sub_create"),

    path('sub/list/all/',
         ExampleTitleListView.as_view(), name="sub_list"),

    path('sub/detail/<pk>',
         ExampleTitleDetailView.as_view(), name="sub_detail"),

]

subdetail_urls = [

    path('subdetail/<pk>/',
         ExampleDetailCreateView.as_view(), name="detail_create"),

    path('subdetail/list/all/',
         ExampleDetailListView.as_view(), name="detail_list"),

    path('subdetail/detail/<pk>',
         ExampleDetailDetailView.as_view(), name="detail_detail"),

]

urlpatterns = header_urls + example_urls + sub_urls + subdetail_urls + [

    path('popular/all/',
         PopularExamples.as_view(), name="popular_examples"),

]
