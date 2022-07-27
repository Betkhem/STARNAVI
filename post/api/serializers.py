from rest_framework import serializers
from post.models import Post, Like
from user.models import User

class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False, 
        queryset=User.objects.all(),
        slug_field='username'
    )
    class Meta:
        model = Post
        fields = "__all__"


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Like
        exclude = ("post",)

