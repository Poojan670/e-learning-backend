from django.urls import path
from src.user.views.userview import (
    RegisterUser, RegisteredUsersList,
    UserDetail, UpdateUserDetail
)

from src.user.views.otp import (
    OTPVerifyView, ReSendEmailOtpView
)

from src.user.views.auth import (
    LoginView, LogOutView,
    TokenRefreshView
)

from src.user.views.subscribe import SendEmailsView

app_name = 'user'


user_patterns = [

    path('register/', RegisterUser.as_view(), name="register"),
    path('register/all/', RegisteredUsersList.as_view(), name="register_list"),
    path('retrieve/<pk>/', UserDetail.as_view(), name="register_show"),
    path('update/<pk>/', UpdateUserDetail.as_view(), name="update"),

]

otp_patterns = [

    path('verify/<pk>/', OTPVerifyView.as_view(), name="verify"),
    path('resend/<pk>/', ReSendEmailOtpView.as_view(), name="resend"),
]


auth_patterns = [

    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogOutView.as_view(), name="logout"),
    path('refresh/', TokenRefreshView.as_view(), name="refresh"),

]

subscribe_patterns = [
    path('send/mail/', SendEmailsView.as_view(), name="send-email")
]

urlpatterns = user_patterns + otp_patterns + auth_patterns + subscribe_patterns
