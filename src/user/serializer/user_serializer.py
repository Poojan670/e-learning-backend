from rest_framework import serializers
from src.user.models import User


class RegisterSerializer(serializers.ModelSerializer):

    def validate_email(self, value):
        object = self.Meta.model
        if object.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "User with this email already exists!")
        return value

    class Meta:
        model = User
        fields = ['email', 'password']
        read_only_fields = ('id', 'created_at', 'updated_at',
                            'otp', 'activation_key', 'is_active', )


class RegisteredUsersIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email']


class UpdateUserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['full_name', 'profile_pic', 'gender']


class UserProfile(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'gender', 'full_name', 'is_active']


class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
            user.save()
        return user

    def patch(self, instance, validated_data):
        user = super().update(instance, validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
            user.save()
        return user


class VerifyUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['otp']


class ForgotPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['otp', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class DeleteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']
