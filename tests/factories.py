from random import randint, randrange

from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now, datetime

import factory
from decouple import config

from whatyouknow.blog.models import CategoryTypes
from .reference import ReferenceModel as rm
from .utils import get_image_file_data, get_post_text, get_tags, CURRENT_TZ


DATETIME_NOW = now()


class SuperUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = rm.USER
        django_get_or_create = ('username',)

    username = config('SUPERUSER_NAME')
    name = 'Administrator'
    password = factory.PostGenerationMethodCall('set_password', config('SUPERUSER_PASSWORD'))
    email = config('SUPERUSER_NAME') + '@whatyouknow.com'
    is_active = True
    is_staff = True
    is_superuser = True
    avatar = factory.django.FileField(
        filename='admin_' + rm.USER.avatar.field.name + '.jpg',
        data=factory.LazyAttribute(
            lambda o: get_image_file_data(min_width=300, min_height=300)))


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = rm.USER
        django_get_or_create = ('username',)

    username = factory.Faker('user_name')
    password = factory.PostGenerationMethodCall('set_password', '1234')
    email = factory.Faker('email')
    name = factory.Faker('name')
    is_active = True
    is_staff = False
    is_superuser = False
    specialization = factory.Faker('job')
    description = factory.Faker('paragraph', nb_sentences=randint(10, 25))
    avatar = factory.django.FileField(filename=rm.USER.avatar.field.name + '.jpg',
                                      data=factory.LazyAttribute(
                                          lambda o: get_image_file_data(min_width=300, min_height=300)))


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'blog.Post'
        django_get_or_create = ('user', 'category', 'title')

    user = factory.Iterator(rm.USER.objects.filter(is_superuser=False))
    category = factory.LazyFunction(CategoryTypes.get_random_index)
    publish = factory.Faker('date_time_between_dates',
                            datetime_start=datetime(2019, 1, 1),
                            datetime_end=DATETIME_NOW,
                            tzinfo=CURRENT_TZ)
    title = factory.Faker('sentence')
    feed_cover = factory.django.FileField(filename=rm.POST.feed_cover.field.name + '.jpg',
                                          data=factory.LazyAttribute(
                                              lambda o: get_image_file_data(min_width=360, min_height=250)))
    feed_article_preview = factory.Faker('text', max_nb_chars=factory.LazyAttribute(lambda o: randint(200, 500)))
    text = factory.LazyFunction(get_post_text)

    @factory.post_generation
    def post_tags(self, create, extracted, **kwargs):
        if create:
            self.tags.add(*get_tags(self.category))


class PostCommentsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'comments.Comment'
        django_get_or_create = ('content_type', 'object_id', 'user', 'date_posted')

    class Params:
        is_comment_edited = factory.LazyAttribute(lambda o: randrange(3) == 0)  # for 1 out of 3 cases
        is_comment_reply = factory.LazyAttribute(lambda o: randrange(10) < 5)  # for 5 out of 10 cases

    content_object = factory.Iterator(rm.POST.objects.all())
    content_type = factory.LazyAttribute(lambda o: ContentType.objects.get_for_model(o.content_object))
    object_id = factory.SelfAttribute('content_object.pk')
    user = factory.Iterator(rm.USER.objects.filter(is_superuser=False))
    text = factory.Faker('text', max_nb_chars=factory.LazyAttribute(lambda o: randint(100, 1500)))
    date_posted = factory.Faker('date_time_between_dates',
                                datetime_start=factory.SelfAttribute('..content_object.publish'),
                                datetime_end=DATETIME_NOW,
                                tzinfo=CURRENT_TZ)
    date_edited = factory.Maybe('is_comment_edited',
                                yes_declaration=factory.Faker('date_time_between_dates',
                                                              datetime_start=factory.SelfAttribute('..date_posted'),
                                                              datetime_end=DATETIME_NOW,
                                                              tzinfo=CURRENT_TZ),
                                no_declaration=factory.SelfAttribute('date_posted'))

    @factory.lazy_attribute
    def parent(self):
        if self.is_comment_reply:
            qs = rm.COMMENT.objects.filter(
                content_type=self.content_type,
                object_id=self.object_id,
                date_posted__lt=self.date_posted
                ).order_by('date_posted')
            count = qs.count()
            if count != 0:
                return qs[randint(0, count - 1)]
            return None
        return None
