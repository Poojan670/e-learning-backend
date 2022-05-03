from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from src.user.models import User
from src.user.views.otp import OtpKey
from src.user.tasks.tasks import forgot_mail, reset_mail
from src.user.serializer.user_serializer import ForgotPasswordSerializer
import pyotp
from rest_framework.exceptions import ValidationError


class ForgotPasswordPhoneView(APIView):
    """
    Forgot Password using email, GET Request, Sends OTP to User's Phone Numebr
    """

    def get_object(self, pk):  # get user object
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        response = {}
        users = self.get_object(pk)
        try:
            key = OtpKey.returnValue()
            users.activation_key = key['totp']
            users.otp = key['OTP']
            print(users.otp)
            users.save()

            forgot_mail.delay(users.email, users.otp)

            response['data'] = users.data

            return Response(response, status=status.HTTP_201_CREATED)
        except:
            return Response({"msg": "New OTP has been sent to your email, "
                                    "Please use it for resetting your password!"}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordEmailView(generics.CreateAPIView):

    """
    After OTP confirmation, User can reset their password
    """

    serializer_class = ForgotPasswordSerializer

    def get_object(self):
        try:
            self.user = User.objects.get(pk=self.kwargs.get('pk'))
        except User.DoesNotExist:
            raise ValidationError({'error': 'User does not exist.'})

    def post(self, request, pk, *args, **kwargs):
        response = {}
        users = self.get_object(pk)
        serializer = ForgotPasswordSerializer(users, data=request.data)
        if serializer.is_valid():
            _otp = serializer.validated_data['otp']
            if _otp != users.otp:
                return Response({"Otp": "Invalid otp"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                try:
                    activation_key = users.activation_key
                    totp = pyotp.TOTP(activation_key, interval=300)
                    verify = totp.verify(users.otp)

                    if verify:

                        reset_mail.delay(users.email)

                        users.save()
                        serializer.save()
                        response['data'] = users.data

                        return Response(users, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"Time out": "Given otp is expired!!"}, status=status.HTTP_408_REQUEST_TIMEOUT)
                except:
                    return Response({"msg": "Your Password has been successfully changed!"}, status=status.HTTP_200_OK)
