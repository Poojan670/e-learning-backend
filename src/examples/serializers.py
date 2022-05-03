from rest_framework import serializers
from .models import (
    ExamplesHeader, ExampleCategory,
    ExampleTitle, ExampleDetail
)
from rest_framework.serializers import ModelSerializer


class ExamplesHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamplesHeader
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class ExampleCategorySerializer(ModelSerializer):
    class Meta:
        model = ExampleCategory
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'language')


class ExampleTitleSerializer(ModelSerializer):
    class Meta:
        model = ExampleTitle
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at',
                            'example_category', 'is_popular')


class ExampleTitleNameSerializer(ModelSerializer):
    class Meta:
        model = ExampleTitle
        fields = ['title', 'is_popular']


class ExampleCategoryIdSerializer(ModelSerializer):
    example_title = ExampleTitleNameSerializer(many=True)
    language = serializers.CharField(source='language.name')

    class Meta:
        model = ExampleCategory
        fields = ['id', 'title', 'language', 'example_title']


class ExampleDetailSerializer(ModelSerializer):
    class Meta:
        model = ExampleDetail
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'relation')


class ExampleDetailIdSerializer(ModelSerializer):
    example_title = serializers.CharField(source="relation.title")

    class Meta:
        model = ExampleDetail
        fields = ['id', 'title', 'example_title']


class ExampleDetailNameSerializer(ModelSerializer):

    class Meta:
        model = ExampleDetail
        fields = ['title', 'description', 'image']


class ExampleTitleIdSerializer(ModelSerializer):
    example_category = serializers.CharField(source='example_category.title')
    example_detail = ExampleDetailNameSerializer(many=True)

    class Meta:
        model = ExampleTitle
        fields = ['id', 'title',
                  'example_category', 'example_detail']
