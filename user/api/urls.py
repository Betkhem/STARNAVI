from django.urls import path
from .views import CreateUserAPIView, LogInAPIView, UserActivityEndpointAPIView

urlpatterns = [
    path("sign_up/", CreateUserAPIView.as_view()),
    path("sign_in/", LogInAPIView.as_view()),
    path("last_login/<int:pk>", UserActivityEndpointAPIView.as_view())
]
