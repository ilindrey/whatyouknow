from enum import Enum
from random import choice as random_choice

from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model

from django_summernote.fields import SummernoteTextField
from taggit.managers import TaggableManager
from easy_thumbnails.signals import saved_file
from easy_thumbnails.signal_handlers import generate_aliases_global


class CategoryTypes(Enum):
    DEVELOPMENT = {'index': 0, 'short_name': 'Develop', 'full_name': 'Development'}
    ADMINISTRATING = {'index': 1, 'short_name': 'Admin', 'full_name': 'Administrating'}
    DESIGN = {'index': 2, 'short_name': 'Design', 'full_name': 'Design'}
    MANAGEMENT = {'index': 3, 'short_name': 'Management', 'full_name': 'Management'}
    MARKETING = {'index': 4, 'short_name': 'Marketing', 'full_name': 'Marketing'}
    POPULAR_SCIENCE = {'index': 5, 'short_name': 'PopSci', 'full_name': 'Popular Science'}

    @classmethod
    def get(cls, *args):
        if args:
            l = []
            for key in cls:
                d = {}
                for a in args:
                    d[a] = key.value[a]
                l.append(d)
            return l
        else:
            return [key.value for key in cls]

    @classmethod
    def list(cls, key):
        return [value[key] for value in cls.get(key)]

    @classmethod
    def get_key_by_index(cls, index, key):
        l = cls.get('index', key)
        for value in l:
            if value['index'] == index:
                return value[key]

    @classmethod
    def choices(cls):
        return [(value['index'], value['full_name']) for value in cls.get('index', 'full_name')]

    @classmethod
    def get_random_choices(cls):
        return random_choice(cls.choices())


class Post(models.Model):

    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    category = models.IntegerField(choices=CategoryTypes.choices())
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
