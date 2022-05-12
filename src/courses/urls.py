from django.urls import path, include
from . import views
from rest_framework import routers
from .comments_views import (
    ReplyList, ReplyDetail, CommentLike,
    CommentList, CommentDetail, CommentDislike
)
from .review_views import (
    ReviewReplyList, ReviewsReplyDetail, ReviewsList, ReviewDetail,
    ReviewLike, ReviewDislike
)

app_name = "courses"


router = routers.DefaultRouter(trailing_slash=False)
router.register("instructor", views.InstructorView)
router.register("category", views.CategoryView)
router.register("course", views.CourseView)
router.register("video-section", views.VideoSetionView)
router.register("video-courses", views.VideoCoursesView)
router.register("order", views.OverViewset)
router.register("course-numbers", views.CourseNumbersView)
router.register("certificate", views.CertificateView)
router.register("announcement", views.AnnouncementView)


comment_urls = [
    path('comments/', CommentList.as_view()),
    path('comments-id/<str:comment_id>/', CommentDetail.as_view()),
    path('comments/<int:pk>/<str:comment_id>/', CommentLike.as_view()),
    path('comments/<str:comment_id>/<int:pk>/', CommentDislike.as_view()),
    path('comments-reply/', ReplyList.as_view()),
    path('comments-reply/<int:comment>/', ReplyDetail.as_view()),
]

reviews_urls = [
    path('reviews/', ReviewsList.as_view()),
    path('reviews-id/<str:review_id>/', ReviewDetail.as_view()),
    path('reviews/<int:pk>/<str:review_id>/', ReviewLike.as_view()),
    path('reviews/<str:review_id>/<int:pk>/', ReviewDislike.as_view()),
    path('reviews-reply/', ReviewReplyList.as_view()),
    path('reviews-reply/<int:review>/', ReviewsReplyDetail.as_view()),
]

urlpatterns = [
    path("", include(router.urls))

] + comment_urls + reviews_urls
