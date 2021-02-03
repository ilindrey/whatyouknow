from random import randint, randrange

from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now

import factory
from decouple import config

from whatyouknow.blog.models import CategoryTypes
from whatyouknow.comments.models import Comment
from .reference import ReferenceModel as rm
from .lazy_functions import get_image_url, get_post_text, get_tags, current_tz


class SuperUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = rm.USER
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
        model = rm.USER
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
        model = 'blog.Post'
        django_get_or_create = ('user', 'category', 'title')

    user = factory.Iterator(rm.USER.objects.filter(is_superuser=False))
    category = factory.LazyFunction(CategoryTypes.get_random_index)
    publish = factory.Faker('date_time_between', start_date='-2y', end_date='now', tzinfo=current_tz)
    title = factory.Faker('sentence')
    feed_cover = factory.LazyAttribute(lambda o: get_image_url(410, 250, 1200, 250))
    feed_article_preview = factory.Faker('text', max_nb_chars=randint(500, 1500))
    text = factory.LazyFunction(get_post_text)

    @factory.post_generation
    def post_tags(self, create, extracted, **kwargs):
        if create:
            self.tags.add(*get_tags(self.category))


class PostCommentsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'comments.Comment'
        django_get_or_create = ('content_type', 'object_id', 'user', 'posted')

    class Params:
        is_reply = randrange(10) != 0  # for 9 out of 10 cases
        # is_edited = randrange(4) == 0  # for 1 out of 4 cases

    content_object = factory.Iterator(rm.POST.objects.all())
    content_type = factory.LazyAttribute(lambda o: ContentType.objects.get_for_model(o.content_object))
    object_id = factory.SelfAttribute('content_object.pk')
    user = factory.Iterator(rm.USER.objects.filter(is_superuser=False))
    posted = factory.Faker('date_time_between_dates',
                           datetime_start=factory.SelfAttribute('..content_object.publish'),
                           datetime_end=now(),
                           tzinfo=current_tz)
    text = factory.Faker('text', max_nb_chars=randint(500, 1500))

    # @factory.lazy_attribute
    # def edited(self):
    #     if self.is_edited:
    #         return factory.Faker('date_time_between_dates',
    #                              datetime_start=self.posted,
    #                              datetime_end=now(),
    #                              tzinfo=current_tz)
    #     return self.posted

    @factory.lazy_attribute
    def parent(self):
        if self.is_reply:
            qs = rm.COMMENT.objects.filter(
                content_type=self.content_type,
                object_id=self.object_id,
                posted__lt=self.posted
                ).order_by('posted')
            count = qs.count()
            if count != 0:
                return qs[randint(0, count - 1)]
            return None
        return None
