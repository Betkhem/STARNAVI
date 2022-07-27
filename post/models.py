from django.db import models
from user.models import User

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, blank=False, null=False)
    content = models.TextField(max_length=1000, default="Default content")
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(User, related_name='user_like', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post_like', on_delete=models.CASCADE)
    published_at = models.DateField(format('%Y-%m-%d'), auto_now_add=True)
