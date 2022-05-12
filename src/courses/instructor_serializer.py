from rest_framework import serializers
from .models import InstructorProfile


class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorProfile
        fields = '__all__'
        read_only_fields = ('user',)


class InstructorListSerializer(serializers.ModelSerializer):

    user_name = serializers.ReadOnlyField(source='user.full_name')
    profile_pic = serializers.URLField(source='user.profile_pic')

    class Meta:
        model = InstructorProfile
        fields = '__all__'
