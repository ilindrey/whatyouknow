from django.db import models
from django.utils import timezone
from django.urls import reverse

from django_summernote.fields import SummernoteTextField
from taggit.managers import TaggableManager

from whatyouknow.profiles.models import UserProfile


CATEGORY_CHOICES = (
    (0, "Development"),
    (1, "Administrating"),
    (2, "Design"),
    (3, "Management"),
    (4, "Marketing"),
    (5, "PopSci"),)


class Post(models.Model):

    user = models.ForeignKey(
        UserProfile,
        on_delete=models.PROTECT
        )
    publish = models.DateTimeField(default=timezone.now)
    category = models.IntegerField(choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=200)
    text = SummernoteTextField()
    feed_cover = models.URLField(null=True, blank=True)
    feed_article_preview = SummernoteTextField(null=True, blank=True)
    # allow_comments = models.BooleanField('allow comments', default=True)
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
