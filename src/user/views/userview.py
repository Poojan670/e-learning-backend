from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
import uuid
from rest_framework.response import Response
from django.contrib.auth.password_validation import validate_password
from src.user.models import User
from src.user.views.otp import OtpKey
from src.user.tasks.tasks import register_mail
from src.user.serializer.user_serializer import (
    RegisterSerializer, RegisteredUsersIdSerializer,
    UpdateUserDetailsSerializer, DeleteUserSerializer,
    ChangePasswordSerializer
)
from src.user.permissions.permissions import (
    IsAdminUser,
    UserObjectPermission,
    AdminAllUserObjectAllOrReadOnly
)


class RegisterUser(generics.CreateAPIView):

    serializer_class = RegisterSerializer

    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            key = OtpKey.returnValue()

            user = User(id=uuid.uuid4(),
                        email=serializer.data['email'],
                        otp=key['OTP'],
                        activation_key=key['totp']
                        )

            try:
                validate_password(serializer.data['password'])
            except ValidationError as e:
                raise ValidationError(str(e))

            user.set_password(serializer.data['password'])
            user.is_active = False

            register_mail.delay(user.email, user.otp)

            user.save()

            return Response({"user_id": user.id,
                             "email": user.email,
                             "otp_code": user.otp}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisteredUsersList(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all().order_by('created_at')
    serializer_class = RegisteredUsersIdSerializer


class UserDetail(generics.RetrieveAPIView):
    permission_classes = [UserObjectPermission]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class UpdateUserDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [AdminAllUserObjectAllOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UpdateUserDetailsSerializer


class DeleteUserView(generics.DestroyAPIView):
    permission_classes = [UserObjectPermission]
    queryset = User.objects.all()
    serializer_class = DeleteUserSerializer


class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = [UserObjectPermission]
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
