from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django_summernote import models as summer_model
from django_summernote import fields as summer_fields

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="writer", default="")
    hashtag_field = models.CharField(max_length=200, blank=True)
    hashtags = models.ManyToManyField('Hashtag', blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="likes")
    post_date=models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.content


class SummerNote(summer_model.Attachment):
    summer_field = summer_fields.SummernoteTextField(default='')


class CustomUser(AbstractUser):
    def __str__(self):
        return self.username

    nickname = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    profile_image = models.ImageField(upload_to='images/', blank=True)



class SocialPlatform(models.Model):
    platform = models.CharField(max_length=20, default=0)

    class Meta:
        db_table = "social_platform"


class User(models.Model):
    social = models.ForeignKey(SocialPlatform, on_delete=models.CASCADE, max_length=20, blank=True, default=1)
    social_login_id = models.CharField(max_length=50, blank=True)
    


class Comment(models.Model):
    def __str__(self):
        return self.text

    c_writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="c_writer", default="")
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.CharField('댓글',max_length=50)

class ReComment(models.Model):
    def __str__(self):
        return self.text

    rc_writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="rc_writer", default="")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='recoms')
    text = models.CharField('대댓글',max_length=150)
    created_at = models.DateTimeField(auto_now=True)

class Hashtag(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=50)
