# from django.shortcuts import render
from .serializers import PostSerializer, LikeSerializer
from post.models import Post, Like
from user.models import User

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError

# Create your views here.

def check_jwt(request):
    token = request.COOKIES.get("jwt")
    if not token:
        raise AuthenticationFailed("Unauthenticated!")


class CreatePost(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        check_jwt(self.request)
        serializer.save()


class CreateLikeAPIView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def perform_create(self, serializer):
        username = self.kwargs["username"]
        post_pk = self.kwargs["post_pk"]
        user = User.objects.filter(username=username).first()
        post = Post.objects.filter(pk=post_pk).first()
        if user is None or post is None:
            raise ValidationError("Username and post must be valid")
        like_queryset = Like.objects.filter(post=post, user=user)
        if like_queryset.exists():
            raise ValidationError("You have already liked this post!")

        serializer.save(post=post, user=user)

# class CreateLikeAPIView(generics.CreateAPIView):
#     serializer_class = LikeSerializer
#     queryset = Like.objects.all()

#     def perform_create(self, serializer):
#         check_jwt(self.request)
        
#         post = get_object_or_404(Post, **self.kwargs)
#         user = get_object_or_404(User, **self.kwargs)
#         print(user, post)
#         if post is None or user is None:
#             return Response({"response": "Both username and post must be valid"})
#         # if not Like.objects.filter(author=self.request.username, post=post).exists():
#         serializer.save(author=user, post=post)


class DestroyLikeAPIView(generics.DestroyAPIView):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def perform_destroy(self, instance):
        check_jwt(self.request)
        # like_obj = get_object_or_404(Like, post_pk=self.kwargs["post_pk"], author=self.kwargs["username"])
        # print(like_obj)
        # username = self.kwargs["username"]
        # post_pk = self.kwargs["post_pk"]
        # user = User.objects.filter(username=username).first()
        # post = Post.objects.filter(pk=post_pk).first()
        # if user is None or post is None:
        #     raise ValidationError("Username and post must be valid")
        # like_queryset = Like.objects.filter(post=post, user=user)
        # if like_queryset.exists():
        #     raise ValidationError("You have already disliked this post!")

        return super().perform_destroy(instance)


class PostAnaliticsLikesView(generics.ListAPIView):
    serializer_class = LikeSerializer

    def get(self, request, *args, **kwargs):
        likes_during_period = Like.objects.filter(published_at__range=[kwargs['date_from'], kwargs['date_to']])
        response = Response()
        response.data = {
            'response': []
        }
        if len(likes_during_period) > 0:
            response.data = {
                'likes_made_by_period': len(likes_during_period)
            }
        return response
