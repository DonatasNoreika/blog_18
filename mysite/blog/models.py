# from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.utils.translation import gettext_lazy as _

# Create your models here.

class CustomUser(AbstractUser):
    photo = models.ImageField(verbose_name = _("Photo"),
                              upload_to='profile_pics',
                              null=True, blank=True)

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
    title = models.CharField(verbose_name=_("Title"))
    content = models.TextField(verbose_name=_("Content"))
    date = models.DateTimeField(verbose_name=_("Date"), auto_now_add=True)
    author = models.ForeignKey(verbose_name=_("Author"),
                               to='blog.CustomUser',
                               on_delete=models.CASCADE)
    photo = models.ImageField(verbose_name=_("Photo"),
                              upload_to='post_photos',
                              null=True, blank=True)

    def comments_count(self):
        return self.comments.count()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ['-pk']


class Comment(models.Model):
    post = models.ForeignKey(verbose_name = _("Post"),
                             to="Post",
                             on_delete=models.CASCADE,
                             related_name="comments")
    content = models.TextField(verbose_name = _("Content"))
    date = models.DateTimeField(verbose_name = _("Date"), auto_now_add=True)
    author = models.ForeignKey(verbose_name = _("Author"),
                               to='blog.CustomUser',
                               on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")