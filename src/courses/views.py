from .models import (
    Announcement, InstructorProfile, Category, Course,
    VideoSections, VideoCourses, Overview,
    CourseNumbers, Certificates
)
from src.courses.instructor_serializer import (
    InstructionSerializer, InstructorListSerializer
)
from .courses_serializer import (
    CategorySerializer, CourseSaveSerializer, CourseSerializer, VideoSectionSerializer, VideoCoursesSaveSerializer,
    VideoCoursesSerializer, OverViewSerializer, VideoSectionListSerializer,
    CourseNumbersSerializer, CertificatesSerializer, AnnouncementSerializer
)
from rest_framework import status, viewsets
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .custom_filters import InstructorFilter
from rest_framework.permissions import IsAuthenticated
from .permissions import AnnouncementObjectPermission


class InstructorView(viewsets.GenericViewSet):
    queryset = InstructorProfile.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = (SearchFilter, InstructorFilter, DjangoFilterBackend)
    search_fields = ['user', 'user__email', 'user__full_name']
    filter_fields = ['profession', 'user__full_name', 'user__email']
    ordering_fields = ['created_at', 'id']
    http_method_names = ['get', 'head', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == "GET":
            return InstructorListSerializer
        return InstructionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        item = self.get_object()
        serializer = InstructorListSerializer(item)
        return Response(serializer.data)

    def destroy(self, request):
        item = self.get_object()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('created')
    serializer_class = CategorySerializer
    http_method_names = ['get', 'head', 'post', 'patch', 'delete']
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    ordering_fields = ['created_at']
    search_fields = ['name']
    filter_fields = ['name']


class CourseView(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('created')
    http_method_names = ['get', 'head', 'post', 'patch', 'delete']
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    ordering_fields = ['created']
    search_fields = ['seller__profession', 'seller__user__full_name']
    filter_fields = ['category', 'title', 'price', 'views']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CourseSerializer
        return CourseSaveSerializer

    def create(self, request, *args, **kwrags):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(seller=self.request.user.instructorprofile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.views = obj.views + 1
        obj.save(update_fields=("views", ))
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        for obj in queryset:
            obj.views = obj.views + 1
            obj.save(update_fields=("views", ))
        return super().list(request, *args, **kwargs)


class VideoSetionView(viewsets.ModelViewSet):
    queryset = VideoSections.objects.all().order_by('id')
    http_method_names = ['get', 'head', 'post', 'patch', 'delete']
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    ordering_fields = ['id']
    search_fields = ['section_title']
    filter_fields = ['section_title']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return VideoSectionListSerializer
        return VideoSectionSerializer


class VideoCoursesView(viewsets.ModelViewSet):
    queryset = VideoCourses.objects.all()
    http_method_names = ['get', 'head', 'post', 'patch', 'delete']
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    ordering_fields = ['date_uploaded']
    search_fields = ['video_title', 'section']
    filter_fields = ['video_title']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return VideoCoursesSerializer
        return VideoCoursesSaveSerializer

    def list(self, request, *args, **kwargs):
        serializer = VideoCoursesSerializer(self.get_queryset(), many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))


class OverViewset(viewsets.ModelViewSet):
    queryset = Overview.objects.all()
    serializer_class = OverViewSerializer
    http_method_names = ['get', 'head', 'post', 'patch', 'delete']
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    ordering_fields = ['id']
    search_fields = ['title']
    filter_fields = ['title']


class CourseNumbersView(viewsets.ModelViewSet):
    queryset = CourseNumbers.objects.all()
    serializer_class = CourseNumbersSerializer
    http_method_names = ['get', 'head', 'post', 'patch', 'delete']
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    ordering_fields = ['id']
    search_fields = ['languages', 'video_length']
    filter_fields = ['skill_level', 'languages']

    def create(self, request, *args, **kwargs):
        serializer = CourseNumbersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        overview_obj = serializer.validated_data['overview']
        overview = Overview.objects.get(pk=overview_obj.pk)
        course = Course.objects.get(pk=overview.pk)
        sections = VideoSections.objects.filter(course=course).first()
        course_title = sections.course.title
        videos_no = VideoCourses.objects.filter(
            section__course__title=course_title).count()

        serializer.save(lectures=videos_no)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CertificateView(viewsets.ModelViewSet):
    queryset = Certificates.objects.all()
    serializer_class = CertificatesSerializer


class AnnouncementView(viewsets.ModelViewSet):
    serializer_class = AnnouncementSerializer
    queryset = Announcement.objects.all().order_by('id')

    def get_permissions(self):
        if self.request.method == 'POST':
            return self.permission_classes == [IsAuthenticated]
        elif self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return self.permission_classes == [AnnouncementObjectPermission]
        return super().get_permissions()
