import logging
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.utils.translation import ugettext_lazy as _

from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
)
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied, NotAcceptable
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets

from .models import Category, Course, CourseViews
from .serializers import (
    CategoryListSerializer,
    CourseSerializer,
    SerpyCourseSerializer,
    CreateCourseSerializer,
    CourseViewsSerializer,
    CourseDetailSerializer,
    CategorySerializer
)
from .permissions import IsOwnerAuth, ModelViewSetsPermission

from googletrans import Translator
from time import time
from datetime import timedelta
from rest_framework.permissions import IsAdminUser


def time_calculator(func):
    def wrapper(*args, **kwargs):
        time1 = time()
        func(*args, **kwargs)
        time2 = time()
        print("Run Time : ", timedelta(time2 - time1).total_seconds())

    return wrapper


translator = Translator()
logger = logging.getLogger(__name__)


class CategoryCreateView(CreateAPIView):
    permission_class = [IsAdminUser]
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('created')


class CategoryListAPIView(ListAPIView):
    serializer_class = CategoryListSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    search_fields = ("name",)
    ordering_fields = ("created",)
    filter_fields = ("created",)

    @time_calculator
    def time(self):
        return 0

    def get_queryset(self):
        queryset = Category.objects.all()
        self.time()
        return queryset


class CategoryAPIView(RetrieveAPIView):
    serializer_class = CategoryListSerializer
    queryset = Category.objects.all()


class CreateCourseAPIView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateCourseSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(seller=user)
        logger.info(
            "Course ( "
            + str(serializer.data.get("title"))
            + " ) created"
            + " by ( "
            + str(user.email)
            + " )"
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SerpyListCourseAPIView(ListAPIView):
    serializer_class = SerpyCourseSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    search_fields = ("title",)
    ordering_fields = ("created",)
    filter_fields = ("views",)
    queryset = Course.objects.all()


class ListCourseView(viewsets.ModelViewSet):
    permission_classes = (ModelViewSetsPermission,)
    serializer_class = CreateCourseSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    search_fields = ("title",)
    ordering_fields = ("created",)
    filter_fields = ("views",)
    queryset = Course.objects.all()

    def update(self, request, *args, **kwargs):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        if User.objects.get(email="po0janhunt@gmail.com") != self.get_object().seller:
            raise NotAcceptable(_("you don't own Course"))
        return super(ListCourseView, self).update(request, *args, **kwargs)


class ListCourseAPIView(ListAPIView):
    serializer_class = CourseSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    search_fields = ("title",)
    ordering_fields = ("created",)
    filter_fields = ("views",)
    queryset = Course.objects.all()

    @time_calculator
    def time(self):
        return 0

    # Cache requested url for each user for 2 hours
    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        self.time()
        return Response(serializer.data)


class ListUserCourseAPIView(ListAPIView):
    serializer_class = CourseSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    search_fields = (
        "title",
        "user__email",
    )
    ordering_fields = ("created",)
    filter_fields = ("views",)

    def get_queryset(self):
        user = self.request.user
        queryset = Course.objects.filter(user=user)
        return queryset


class DestroyCourseAPIView(DestroyAPIView):
    permission_classes = [IsOwnerAuth]
    serializer_class = CourseDetailSerializer
    queryset = Course.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response({"detail": "Course deleted"})


class CourseViewsAPIView(ListAPIView):
    serializer_class = CourseViewsSerializer
    queryset = CourseViews.objects.all()


class CourseDetailView(APIView):
    def get(self, request, uuid):
        Course = Course.objects.get(uuid=uuid)
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")

        if not CourseViews.objects.filter(Course=Course, ip=ip).exists():
            CourseViews.objects.create(Course=Course, ip=ip)

            Course.views += 1
            Course.save()
        serializer = CourseDetailSerializer(
            Course, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        user = request.user
        Course = get_object_or_404(Course, pk=pk)
        if Course.user != user:
            raise PermissionDenied("this Course don't belong to you.")

        serializer = CourseDetailSerializer(
            Course, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
