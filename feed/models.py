from django.db import models
from django.conf import settings
from django.urls import reverse
# Create your models here.

class Post(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    image = models.ImageField(upload_to="post_images", default='default.png')
    caption = models.CharField(max_length=255, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.id})
    
    def serialize(self):
        return {
            'creator': self.creator.username,
            'image': self.image.url,
            'caption': self.caption,
            'date_posted': self.date_posted
        }


class Comment(models.Model):
    onPost = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", null=True)
    content = models.TextField(max_length=512)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    createdOn = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            'onPost': self.onPost.id,
            'content': self.content,
            'profileURL': self.createdBy.profile.get_absolute_url(),
            'profileName': self.createdBy.username,
            'profileImage': self.createdBy.profile.image.url,
            'createdOn': self.createdOn
        }

class Like(models.Model):
    byProfile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes")
    onPost = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

