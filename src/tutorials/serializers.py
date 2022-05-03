from rest_framework import serializers
from .models import *
from rest_framework.serializers import ModelSerializer


class TutorialsHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorialsHeader
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class TutorialsPageSerializer(ModelSerializer):
    class Meta:
        model = Tutorial
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'language')


class SubTutorialsSerializer(ModelSerializer):
    class Meta:
        model = SubTutorial
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'tutorials_title')


class SubTutorialsNameSerializer(ModelSerializer):
    class Meta:
        model = SubTutorial
        fields = ['sub_tutorial']


class TutorialsPageIdSerializer(ModelSerializer):
    sub_tutorials = SubTutorialsNameSerializer(many=True)
    language = serializers.CharField(source='language.name')

    class Meta:
        model = Tutorial
        fields = ['id', 'title', 'language', 'sub_tutorials']


class SubTopicsSerializer(ModelSerializer):
    class Meta:
        model = SubTopic
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'topic')


class SubTopicsNameSerializer(ModelSerializer):

    class Meta:
        model = SubTopic
        exclude = ('id', 'created_at', 'updated_at', 'topic')


class SubTutorialsIdSerializer(ModelSerializer):
    tutorial_title = serializers.CharField(source='tutorials_title.title')
    subtopics = SubTopicsNameSerializer(many=True)

    class Meta:
        model = SubTutorial
        fields = ['id', 'sub_tutorial', 'tutorial_title', 'subtopics']


class SubDetailSerializer(ModelSerializer):
    class Meta:
        model = SubDetail
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'relation')


class SubDetailIdSerializer(ModelSerializer):
    sub_topic = serializers.CharField(source="relation.title")

    class Meta:
        model = SubDetail
        fields = ['id', 'title', 'sub_topic']


class SubDetailNameSerializer(ModelSerializer):

    class Meta:
        model = SubDetail
        fields = ['title', 'description', 'video_title',
                  'video_URL', 'video_description']


class SubTopicsIdSerializer(ModelSerializer):
    subs_tutorial = serializers.CharField(source='topic.sub_tutorial')
    sub_desc = SubDetailSerializer(many=True)

    class Meta:
        model = SubTopic
        fields = ['id', 'title', 'subs_tutorial', 'sub_desc']
