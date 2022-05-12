from rest_framework.serializers import ModelSerializer
from .models import (
    BodyHeader, header, Subscribe,
    Body, Languages
)


class HeaderSerializer(ModelSerializer):
    class Meta:
        model = header
        fields = ['title', 'description', 'sub_title', 'side_image']


class HeaderIdSerializer(ModelSerializer):
    class Meta:
        model = header
        fields = ('id', )


class SubscribeSerializer(ModelSerializer):
    class Meta:
        model = Subscribe
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class SubscribeIdSerializer(ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ['email']


class BodySerializer(ModelSerializer):
    class Meta:
        model = Body
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class BodyIdSerializer(ModelSerializer):
    class Meta:
        model = Body
        fields = ['id']


class LanguagesSerializer(ModelSerializer):
    class Meta:
        model = Languages
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', )


class LanguagesIdSerializer(ModelSerializer):
    class Meta:
        model = Languages
        fields = ['id', 'name']


class BodyHeaderSerializer(ModelSerializer):
    class Meta:
        model = BodyHeader
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
