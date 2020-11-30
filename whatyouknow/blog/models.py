from django.db import models

from django_summernote.fields import SummernoteTextField
from taggit.managers import TaggableManager

from whatyouknow.profiles.models import UserProfile


# class Category(models.Model):
#     name = models.CharField(null=True, blank=False, max_length=100)
#     order = models.IntegerField(null=False, blank=False)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name_plural = "Categories"

CATEGORY_CHOICES = (
    (1, "Development"),
    (2, "Administrating"),
    (3, "Design"),
    (4, "Business"),
    (5, "Management"),
    (6, "Marketing"),
    (7, "Popular science"),)


class Post(models.Model):

    user = models.ForeignKey(
        UserProfile,
        on_delete=models.PROTECT
        )
    date = models.DateTimeField()
    category = models.IntegerField(choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=200)
    text = SummernoteTextField()
    feed_cover = models.URLField(null=True, blank=True)
    feed_article_preview = SummernoteTextField(null=True, blank=True)
    feed_read_more_button_name = models.CharField(max_length=50, default='Read more', null=True, blank=True)
    tags = TaggableManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Posts"