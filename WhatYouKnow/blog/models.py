from django.db import models

from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager

from whatyouknow.profiles.models import UserProfile


class Category(models.Model):
    name = models.CharField(null=True, blank=False, max_length=100)
    order = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Post(models.Model):

    user = models.ForeignKey(
        UserProfile,
        on_delete=models.PROTECT
    )
    category = models.ForeignKey(Category, models.PROTECT)
    name = models.CharField(null=True, blank=False, max_length=200)
    date = models.DateTimeField()
    image = models.ImageField(upload_to="posts/")
    description = RichTextUploadingField(null=True, blank=False)
    tags = TaggableManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Posts"