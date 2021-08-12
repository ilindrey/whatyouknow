from enum import Flag
from random import choice as random_choice

from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model

from django_summernote.fields import SummernoteTextField
from taggit.managers import TaggableManager
from easy_thumbnails.signals import saved_file
from easy_thumbnails.signal_handlers import generate_aliases_global


class CategoryTypes(Flag):
    DEVELOPMENT = (0, "Development")
    ADMINISTRATING = (1, "Administrating")
    DESIGN = (2, "Design")
    MANAGEMENT = (3, "Management")
    MARKETING = (4, "Marketing")
    POPULAR_SCIENCE = (5, "Popular Science")

    @classmethod
    def get_name(cls, index):
        return cls.get_list()[index][1]

    @classmethod
    def get_list(cls):
        return [key.value for key in cls]

    @classmethod
    def get_list_index(cls):
        return [key.value[0] for key in cls]

    @classmethod
    def get_list_name(cls):
        return [key.value[1] for key in cls]

    @classmethod
    def get_random(cls):
        return random_choice(cls.get_list())

    @classmethod
    def get_random_index(cls):
        return cls.get_random()[0]

    @classmethod
    def get_random_name(cls):
        return cls.get_random()[1]


class Post(models.Model):

    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    category = models.IntegerField(choices=CategoryTypes.get_list())
    title = models.CharField(max_length=200)
    feed_cover = models.ImageField(upload_to='blog/feed_covers')
    feed_article_preview = SummernoteTextField(blank=True)
    text = SummernoteTextField()
    draft = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    published = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    tags = TaggableManager()

    class Meta:
        verbose_name_plural = 'Posts'
        ordering = ('-published', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.approved and self.published is None:
            self.published = timezone.now()
        super().save(*args, **kwargs)


saved_file.connect(generate_aliases_global)
