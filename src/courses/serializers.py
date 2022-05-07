import serpy
from rest_framework import serializers
from yaml import serialize
from src.user.models import User
from .models import Category, Course, CourseViews


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('created', 'modified', )


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ("modified",)


class CourseSerializer(serializers.ModelSerializer):
    seller = serializers.SlugRelatedField(
        slug_field="email", queryset=User.objects)
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.category.name

    class Meta:
        model = Course
        exclude = ("modified", )


class SerpyCourseSerializer(serpy.Serializer):
    seller = serpy.StrField()
    category = serpy.StrField()
    title = serpy.StrField()
    price = serpy.FloatField()
    image = serpy.StrField()
    description = serpy.StrField()
    quantity = serpy.IntField()
    views = serpy.IntField()


class CourseMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["title"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data = serializers.ModelSerializer.to_representation(self, instance)
        return data


class CreateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        exclude = ("modified",)
        # read_only_fields = ('id', 'seller', 'category', 'title', 'price', 'image', 'description', 'quantity', 'views',)


class CourseDetailSerializer(serializers.ModelSerializer):
    seller = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects)
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.category.name

    class Meta:
        model = Course
        exclude = ("modified",)


class CourseViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseViews
        exclude = ("modified",)
