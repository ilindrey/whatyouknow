from django.db import models

# from ckeditor.fields import RichTextField
from tinymce.models import HTMLField
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
    category = models.IntegerField(null=False, blank=False, choices=CATEGORY_CHOICES)
    title = models.CharField(null=True, blank=False, max_length=200)
    text = HTMLField(null=True, blank=False)
    feed_cover = models.URLField(null=True, blank=True)
    feed_article_preview = HTMLField(null=True, blank=True)
    feed_read_more_button_name = models.CharField(null=True, blank=True, max_length=50, default='Read more')
    tags = TaggableManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Posts"