from django.urls import path, include

urlpatterns = [

    path('user-app/', include('src.user.urls', namespace="user")),

    path('home-app/', include('src.home.urls', namespace="home")),

    path('tutorials-app/', include('src.tutorials.urls', namespace="tutorials")),

    path('examples-app/', include('src.examples.urls', namespace="examples")),

    path('references-app/', include('src.references.urls', namespace="references")),

    path('blogs-app', include('src.blog.urls', namespace="blogs")),

    path('billing-app', include('src.billing.urls', namespace="billing")),

    path('payment-app/', include('src.payment.urls', namespace="payment")),

    path('courses-app/', include('src.courses.urls', namespace="courses")),

]
