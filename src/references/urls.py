from django.urls import path
from .views import *


app_name = "references"


header_urls = [
    path('header/', ReferencesHeaderCreateView.as_view(), name="header"),
    path('header/all/', ReferencesHeaderListView.as_view(), name="header_list"),
    path('header/<pk>', ReferencesHeaderDetailView.as_view(), name="header_detail"),
]

references_urls = [
    path('references/<pk>/',
         ReferencesTitleCreateView.as_view(), name="create"),

    path('references/list/all/',

         ReferencesTitleListView.as_view(), name="list"),
    path('references/detail/<pk>',
         ReferencesTitleDetailView.as_view(), name="detail"),

]

sub_urls = [

    path('sub/<pk>/',
         SubReferencesCreateView.as_view(), name="sub_create"),

    path('sub/list/all/',
         SubReferencesListView.as_view(), name="sub_list"),

    path('sub/detail/<pk>',
         SubReferencesDetailView.as_view(), name="sub_detail"),

]

subdetail_urls = [

    path('subdetail/<pk>/',
         ReferencesDetailCreateView.as_view(), name="detail_create"),

    path('subdetail/list/all/',
         ReferencesDetailListView.as_view(), name="detail_list"),

    path('subdetail/detail/<pk>',
         ReferencesDetailDetailView.as_view(), name="detail_detail"),

]


urlpatterns = header_urls + references_urls + sub_urls + subdetail_urls
