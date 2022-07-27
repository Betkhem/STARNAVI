from django.urls import path
from .views import CreatePost, CreateLikeAPIView, PostAnaliticsLikesView, DestroyLikeAPIView

urlpatterns = [
    path("create_post/", CreatePost.as_view()),
    path("like_post/username=<str:username>&post_pk=<int:post_pk>/", CreateLikeAPIView.as_view()),
    path("dislike_post/<int:pk>", DestroyLikeAPIView.as_view()),
    path("analitics/date_from=<date_from>&date_to=<date_to>/", PostAnaliticsLikesView.as_view()),
]
