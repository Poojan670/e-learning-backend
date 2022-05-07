from django.urls import path, include
from . import views

app_name = "courses"

urlpatterns = [
    path("category/all/", views.CategoryListAPIView.as_view()),
    path("category/<int:pk>/", views.CategoryAPIView.as_view()),

    path("create/course/", views.CreateCourseAPIView.as_view()),
    path("list/course/", views.ListCourseAPIView.as_view()),

    path("course/<str:uuid>/", views.CourseDetailView.as_view()),
    path("course/<int:pk>/delete/", views.DestroyCourseAPIView.as_view()),

    path("serpy/course/", views.SerpyListCourseAPIView.as_view()),
    path("list-course/user/", views.ListUserCourseAPIView.as_view()),

    path("course/views/", views.CourseViewsAPIView.as_view()),
]
