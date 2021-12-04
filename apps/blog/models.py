from enum import Enum
from random import choice as random_choice

from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

from django_summernote.fields import SummernoteTextField
from taggit.managers import TaggableManager
from easy_thumbnails.signals import saved_file
from easy_thumbnails.signal_handlers import generate_aliases_global

from apps_packages.summernote.validators import SummernoteMinValueValidator
from ..moderation.models import ModeratedObjectMixin


class CategoryTypes(Enum):
    DEVELOPMENT = {
        'index': 0,
        'short_name': 'Develop',
        'short_name_lower': 'develop',
        'full_name': 'Development'
    }
    ADMINISTRATING = {
        'index': 1,
        'short_name': 'Admin',
        'short_name_lower': 'admin',
        'full_name': 'Administrating'
    }
    DESIGN = {
        'index': 2,
        'short_name': 'Design',
        'short_name_lower': 'design',
        'full_name': 'Design'
    }
    MANAGEMENT = {
        'index': 3,
        'short_name': 'Management',
        'short_name_lower': 'management',
        'full_name': 'Management'
    }
    MARKETING = {
        'index': 4,
        'short_name': 'Marketing',
        'short_name_lower': 'marketing',
        'full_name': 'Marketing'
    }
    POPULAR_SCIENCE = {
        'index': 5,
        'short_name': 'PopSci',
        'short_name_lower': 'popsci',
        'full_name': 'Popular Science'
    }

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
    def get_value(cls, target, key=None):
        l = cls.get()
        if key is None:
            for d in l:
                for key in d:
                    if d[key] == target:
                        return d
        else:
            for d in l:
                if d[key] == target:
                    return d

    @classmethod
    def get_values(cls, *args, key=None):
        l = []
        for a in args:
            value = cls.get_value(a, key)
            if value is not None:
                l.append(value)
        return l if l else None

    @classmethod
    def choices(cls):
        return [(value['index'], value['full_name']) for value in cls.get('index', 'full_name')]

    @classmethod
    def get_random_choices(cls):
        return random_choice(cls.choices())


class Post(ModeratedObjectMixin, models.Model):

    slug = models.SlugField(null=False, blank=False)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.PROTECT, editable=False)
    category = models.IntegerField(_('Category'), choices=CategoryTypes.choices())
    title = models.CharField(_('Title'), max_length=200)
    feed_cover = models.ImageField(_('Feed cover'), upload_to='blog/feed_covers')
    feed_article_preview = SummernoteTextField(_('Feed article preview'), blank=True)
    text = SummernoteTextField(_('Text'), validators=[SummernoteMinValueValidator(500)])
    tags = TaggableManager()

    class Meta:
        ordering = ('-date_created', )

    def __str__(self):
        return self.title

    @property
    def url_kwargs(self):
        return {'pk': self.pk, 'slug': self.slug}

    def get_absolute_url(self):
        return reverse('post_detail', kwargs=self.url_kwargs)

    def get_edit_url(self):
        return reverse('post_edit', kwargs=self.url_kwargs)

    def get_admin_url(self):
        url = admin_urlname(self._meta, 'change')
        return reverse(url, args=(self.pk,))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


saved_file.connect(generate_aliases_global)
