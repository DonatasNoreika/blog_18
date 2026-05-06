from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image

# Create your models here.

class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to='profile_pics', null=True, blank=True)

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        if self.photo:
            img = Image.open(self.photo.path)
            min_side = min(img.width, img.height)
            left = (img.width - min_side) // 2
            top = (img.height - min_side) // 2
            right = left + min_side
            bottom = top + min_side
            img = img.crop((left, top, right, bottom))
            img = img.resize((300, 300), Image.LANCZOS)
            img.save(self.photo.path)

class Post(models.Model):
    title = models.CharField()
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(to='blog.CustomUser', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='post_photos', null=True, blank=True)

    def comments_count(self):
        return self.comments.count()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pk']


class Comment(models.Model):
    post = models.ForeignKey(to="Post", on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(to='blog.CustomUser', on_delete=models.CASCADE)

