from enum import Flag
from random import choice as random_choice

from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model

from django_summernote.fields import SummernoteTextField
from taggit.managers import TaggableManager


class CategoryTypes(Flag):
    DEVELOPMENT = (0, "Development")
    ADMINISTRATING = (1, "Administrating")
    DESIGN = (2, "Design")
    MANAGEMENT = (3, "Management")
    MARKETING = (4, "Marketing")
    POPULAR_SCIENCE = (5, "Popular Science")

    @classmethod
    def choices(cls):
        return [key.value for key in cls]

    @classmethod
    def get_random(cls):
        return random_choice(cls.choices())

    @classmethod
    def get_random_index(cls):
        return cls.get_random()[0]

    @classmethod
    def get_name(cls, index):
        return cls.choices()[index][1]


class Post(models.Model):

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT
        )
    publish = models.DateTimeField(default=timezone.now)
    category = models.IntegerField(choices=CategoryTypes.choices())
    title = models.CharField(max_length=200)
    text = SummernoteTextField()
    feed_cover = models.URLField(null=True, blank=True)
    feed_article_preview = SummernoteTextField(null=True, blank=True)
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'post_detail',
            kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = "Posts"
        ordering = ('-publish', )
