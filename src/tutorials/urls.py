from django.urls import path
from .views import *


app_name = "tutorials"


header_urls = [

    path('header/', TutorialsHeaderCreateView.as_view(), name="header"),
    path('header/all', TutorialsHeaderListView.as_view(), name="header_list"),
    path('header/<pk>', TutorialsHeaderDetailView.as_view(), name="header_detail"),

]

tutorials_urls = [

    path('tutorials/<pk>/',
         TutorialsCreateView.as_view(), name="create"),

    path('tutorials/list/all/',

         TutorialsListView.as_view(), name="list"),
    path('tutorials/detail/<pk>',
         TutorialsDetailView.as_view(), name="detail"),
]

sub_urls = [
    path('sub/<pk>/',
         SubTutorialsCreateView.as_view(), name="sub_create"),

    path('sub/list/all/',
         SubTutorialsListView.as_view(), name="sub_list"),

    path('sub/detail/<pk>',
         SubTutorialsDetailView.as_view(), name="sub_detail"),


]

subtopics_urls = [


    path('subtopics/<pk>/',
         SubTopicsCreateView.as_view(), name="topics_create"),

    path('subtopics/list/all/',
         SubTopicsListView.as_view(), name="topics_list"),

    path('subtopics/detail/<pk>/',
         SubTopicsDetailView.as_view(), name="topics_detail"),

]

subdetail_urls = [

    path('subdetail/<pk>/',
         SubDetailCreateView.as_view(), name="detail_create"),

    path('subdetail/list/all/',
         SubDetailListView.as_view(), name="detail_list"),

    path('subdetail/detail/<pk>',
         SubDetailDetailView.as_view(), name="detail_detail"),

]


urlpatterns = header_urls + tutorials_urls + \
    sub_urls + subtopics_urls + subdetail_urls
