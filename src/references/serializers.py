from rest_framework import serializers
from .models import *
from rest_framework.serializers import ModelSerializer


class ReferencesHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferencesHeader
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', )


class ReferencesTitleSerializer(ModelSerializer):
    class Meta:
        model = ReferencesTitle
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'language', )


class SubReferencesSerializer(ModelSerializer):
    class Meta:
        model = SubReferences
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'reference_title', )


class SubReferencesNameSerializer(ModelSerializer):
    class Meta:
        model = SubReferences
        fields = ['title', 'description']


class ReferencesTitleIdSerializer(ModelSerializer):
    sub_references = SubReferencesNameSerializer(many=True)
    language = serializers.CharField(source='language.name')

    class Meta:
        model = ReferencesTitle
        fields = ['id', 'title', 'language', 'sub_references']


class ReferencesDetailSerializer(ModelSerializer):
    class Meta:
        model = ReferencesDetail
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'sub_references', )


class ReferencesDetailIdSerializer(ModelSerializer):
    sub_topic = serializers.CharField(source="sub_references.title")

    class Meta:
        model = ReferencesDetail
        fields = ['id', 'title', 'sub_topic']


class ReferencesDetailNameSerializer(ModelSerializer):

    class Meta:
        model = ReferencesDetail
        fields = ['title', 'description']


class SubReferencesIdSerializer(ModelSerializer):
    references_title = serializers.CharField(source='reference_title.title')
    references_detail = ReferencesDetailNameSerializer(many=True)

    class Meta:
        model = SubReferences
        fields = ['id', 'title', 'description',
                  'references_title', 'references_detail']
