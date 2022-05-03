from django.urls import path, include
from rest_framework import routers
from src.home.views import (
    header, subscribe, bodyheader,
    body, languages, email
)

router = routers.DefaultRouter()

router.register(r'header', header.HeaderView, basename='headers')

router.register(r'subscribe', subscribe.SubscribeView, basename='subscribe')

router.register(r'bodyheader', bodyheader.BodyHeaderView,
                basename='bodyheader')

router.register(r'body', body.BodyView, basename='body')

router.register(r'langugaes', languages.LanguagesView, basename='langugaes')

app_name = 'home'

urlpatterns = [
    path('', include(router.urls)),
    path('send/email/', email.SendEmailView.as_view(), name='email')
]
