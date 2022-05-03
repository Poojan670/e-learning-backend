from django.urls import path, include

urlpatterns = [
    path('v1/', include('src.user.urls', namespace="user")),

    path('v2/', include('src.home.urls', namespace="home")),

    path('v3/', include('src.tutorials.urls', namespace="tutorials")),

    path('v4/', include('src.examples.urls', namespace="examples")),

    path('v5/', include('src.references.urls', namespace="references")),

    path('v6/', include('src.blog.urls', namespace="blogs")),

    path('v7/', include('src.billing.urls', namespace="billing")),

    path('v8/', include('src.payment.urls', namespace="payment")),
]
