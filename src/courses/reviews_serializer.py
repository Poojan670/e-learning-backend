from .models import Reviews, ReviewsReply
from rest_framework import serializers


class ReviewsSerializer(serializers.ModelSerializer):

    review_user = serializers.ReadOnlyField(
        source='user.full_name', allow_null=True)
    course_name = serializers.ReadOnlyField(
        source='course.title', allow_null=True)

    class Meta:
        model = Reviews
        fields = ['user', 'course', 'body',
                  'review_id',
                  'rating',
                  'reviewed_at', 'modified_at']
        read_only_fields = ['user', 'review_id', 'reviewed_at', 'modified_at']


class ReviewsReplySerializer(serializers.ModelSerializer):

    reply_user = serializers.ReadOnlyField(
        source='user.full_name', allow_null=True)

    class Meta:
        model = ReviewsReply
        fields = '__all__'

        read_only_fields = ['user', 'reply_at', 'modified_at']
