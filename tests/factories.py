from random import randint
from datetime import datetime

from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.utils.timezone import now
from django.db.models import Subquery, Q

import factory
from decouple import config

from whatyouknow.profiles.models import UserProfile
from whatyouknow.blog.models import Post
from django_comments.models import Comment
from django_comments_xtd.models import XtdComment

from .lazy_functions import get_image_url, get_category, get_post_text, get_tags, current_tz


class SuperUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile
        django_get_or_create = ('username',)

    username = config('SUPERUSER_NAME')
    name = 'Administrator'
    password = factory.PostGenerationMethodCall('set_password', config('SUPERUSER_PASSWORD'))
    email = 'admin@whatyouknow.com'
    is_active = True
    is_staff = True
    is_superuser = True
    image = factory.django.ImageField(color='black', width=256, height=256)


class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile
        django_get_or_create = ('username',)

    username = factory.Faker('user_name')
    password = factory.PostGenerationMethodCall('set_password', 'defaultpassword')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    is_active = True
    is_staff = False
    is_superuser = False
    name = factory.LazyAttribute(lambda obj: '{} {}'.format(obj.first_name, obj.last_name))
    specialization = factory.Faker('job')
    website = factory.Faker('url')
    description = factory.Faker('paragraph', nb_sentences=randint(10, 25))
    image = factory.django.ImageField(color='gray', width=256, height=256)


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post
        django_get_or_create = ('user', 'category', 'title')

    user = factory.Iterator(UserProfile.objects.filter(is_superuser=False))
    # user = factory.SubFactory(UserProfileFactory)
    category = factory.LazyFunction(get_category)
    # category = factory.fuzzy.FuzzyChoice(CATEGORY_CHOICES, getter=lambda c: c[0])
    publish = factory.Faker('date_time_between', start_date='-2y', end_date='now', tzinfo=current_tz)
    title = factory.Faker('sentence')
    feed_cover = factory.LazyAttribute(lambda o: get_image_url(410, 250, 1200, 250))
    feed_article_preview = factory.Faker('text', max_nb_chars=randint(500, 1500))
    text = factory.LazyFunction(get_post_text)

    @factory.post_generation
    def post_tags(self, create, extracted, **kwargs):
        if create:
            self.tags.add(*get_tags(self.category))


class XtdCommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = XtdComment
        django_get_or_create = ('site', 'content_type', 'object_pk', 'user', 'submit_date',)

    class Params:
        is_reply = randint(0, 10) in [i for i in range(10)]  # for 9 out of 10 cases

    site = Site.objects.get_current()
    content_object = factory.Iterator(Post.objects.all())
    content_type = factory.LazyAttribute(lambda o: ContentType.objects.get_for_model(o.content_object))
    object_pk = factory.SelfAttribute('content_object.pk')
    user = factory.Iterator(UserProfile.objects.filter(is_superuser=False))
    # user = factory.SubFactory(UserProfileFactory)
    submit_date = factory.Faker('date_time_between_dates',
                                datetime_start=factory.SelfAttribute('..content_object.publish'),
                                datetime_end=now(),
                                tzinfo=current_tz)
    comment = factory.Faker('text', max_nb_chars=randint(500, 1500))
    is_public = True

    @factory.lazy_attribute
    def parent_id(self):
        if self.is_reply:
            qs = XtdComment.objects.filter(site=self.site,
                                           content_type=self.content_type,
                                           object_pk=self.object_pk)
            count = qs.count()
            if count != 0:
                return qs[randint(0, count-1)].pk
            return 0
        return 0

    @factory.lazy_attribute
    def thread_id(self):
        if self.is_reply:
            qs = XtdComment.objects.filter(site=self.site,
                                           content_type=self.content_type,
                                           object_pk=self.object_pk)
            count = qs.count()
            if count != 0:
                return qs.get(pk=self.parent_id).thread_id  # parent.thread_id
            return 0
        return 0
