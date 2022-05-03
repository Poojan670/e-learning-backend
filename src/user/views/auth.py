from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase
from src.user.serializer.token_serializer import MyTokenObtainPairSerializer
from rest_framework.response import Response


class LoginView(TokenObtainPairView):

    """
    User Login, generates Simple JWT Token upon successful login(valid for 5 minutes)
    User cant login until he/she is verified by either Phone OTP or Email OTP
    """

    serializer_class = MyTokenObtainPairSerializer


class LogOutView(generics.CreateAPIView):
    # logout by blacklisting user's access token
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response("Successful Logout", status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class TokenRefreshView(TokenViewBase):

    # view to refresh Simple JWT token seperately
    serializer_class = TokenRefreshSerializer
