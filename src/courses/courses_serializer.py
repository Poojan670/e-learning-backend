from rest_framework import serializers
from .models import (
    Category, Course,
    VideoSections, VideoCourses,
    Overview, CourseNumbers, Certificates, Announcement
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('created', 'modified', )


class CourseSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

        read_only_fields = ('created', 'modified', 'seller',
                            'views', 'reviews_no')


class CourseSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.name')
    seller = serializers.ReadOnlyField(source='seller.user.full_name')
    seller_email = serializers.ReadOnlyField(source='seller.user.email')

    class Meta:
        model = Course
        fields = '__all__'


class VideoSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoSections
        fields = '__all__'
        read_only_fields = ('video_ref', )


class VideoSectionListSerializer(serializers.ModelSerializer):
    course = serializers.ReadOnlyField(source='course.title', allow_null=True)

    class Meta:
        model = VideoSections
        fields = '__all__'


class VideoCoursesSaveSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoCourses
        fields = '__all__'
        read_only_fields = ('date_uploaded',)


class VideoCoursesSerializer(serializers.ModelSerializer):

    video_section = serializers.ReadOnlyField(source='section.section_title')
    video_section_no = serializers.ReadOnlyField(source='section.section_no')
    course = serializers.ReadOnlyField(source='section.course.title')
    course_category = serializers.ReadOnlyField(
        source='section.course.category.name')

    class Meta:
        model = VideoCourses
        fields = '__all__'


class OverViewSerializer(serializers.ModelSerializer):
    course_name = serializers.ReadOnlyField(source='course.title')
    course_category = serializers.ReadOnlyField(source='course.category.name')

    class Meta:
        model = Overview
        fields = '__all__'


class CourseNumbersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseNumbers
        fields = '__all__'
        read_only_fields = ('students', 'lectures', 'video_length')


class CertificatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificates
        fields = '__all__'
        read_only_fields = ('certificate_user', )


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'
        read_only_fields = ['instructor']
