import pyotp
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from src.user.models import User
from src.user.tasks.tasks import verify_mail, register_mail
from django.core.exceptions import ObjectDoesNotExist
from src.user.serializer.user_serializer import VerifyUser


class OtpKey():

    @staticmethod
    def returnValue():
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret, interval=300)
        OTP = totp.now()
        return {"totp": secret, "OTP": OTP}


class OTPVerifyView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = VerifyUser

    def post(self, request, pk, *args, **kwargs):
        # checks if user exists for the given pk and set's the user's object as users

        try:
            users = User.objects.get(pk=self.kwargs.get('pk'))
        except User.DoesNotExist:
            raise ValidationError({'error': 'User does not exist.'})

        serializer = VerifyUser(users, data=request.data)
        if serializer.is_valid():
            try:
                _otp_phone = serializer.validated_data['otp']
            except:
                # if otp is not given on POST request, throws this response
                return Response({"error": "Please Provide the  OTP"})
            if users.otp != _otp_phone:
                # if the user's otp that was generated during registration doesn't match with the given otp phone
                return Response({"Otp": "Invalid otp"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                activation_key = users.activation_key
                # TOTP is used for operation of time interval of py otp
                totp = pyotp.TOTP(activation_key, interval=300)
                # interval is set to 300 secs, i.e 5 mins exactly
                verify = totp.verify(users.otp)

                if verify:
                    users.is_active = True

                    verify_mail.delay(users.email)

                    users.save()
                    serializer.save()

                    return Response({"Verify success": "Your account has been successfully activated!!"},
                                    status=status.HTTP_202_ACCEPTED)
                else:
                    # if time interval crosses 5 mins threshold, otp is set to expired and this response is shown
                    return Response({"Time out": "Given otp is expired!!"}, status=status.HTTP_408_REQUEST_TIMEOUT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReSendEmailOtpView(APIView):
    """
    Re Send OTP to your email for verification
    """

    def get_object(self, pk):  # get user object function
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        response = {}
        users = self.get_object(pk)
        try:
            if users.is_active:   # if user is already email verified
                return Response({'msg': 'User is already verified'}, status=status.HTTP_200_OK)
            try:
                key = OtpKey.returnValue()
                users.activation_key = key['totp']
                users.otp = key['OTP']

                users.save()

                register_mail.delay(users.email, users.otp)

                response['data'] = users.data

                return Response(response, status=status.HTTP_201_CREATED)
            except:
                return Response({"msg": "New OTP has been sent to your email, "
                                        "Please use it for verification!"}, status=status.HTTP_200_OK)
        except:
            if ObjectDoesNotExist:
                return Response({'msg': 'No User found!'}, status=status.HTTP_400_BAD_REQUEST)
