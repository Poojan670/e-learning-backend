from .models import Comment, Reply
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):

    comment_user = serializers.ReadOnlyField(
        source='user.full_name', allow_null=True)
    course_name = serializers.ReadOnlyField(
        source='course.title', allow_null=True)

    class Meta:
        model = Comment
        fields = ['user', 'course', 'body',
                  'comment_id', 'comment_user', 'course_name', 'comment_at', 'modified_at']
        read_only_fields = ['user', 'comment_id', 'comment_at', 'modified_at']


class ReplySerializer(serializers.ModelSerializer):

    reply_user = serializers.ReadOnlyField(
        source='user.full_name', allow_null=True)

    class Meta:
        model = Reply
        fields = '__all__'

        read_only_fields = ['user', 'reply_at', 'modified_at']
