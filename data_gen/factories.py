from random import randint, randrange, choice as randchoice

from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now

import factory

from apps.blog.models import CategoryTypes

from .reference import ReferenceModel as rm
from .utils import get_image_file_data, get_post_text, get_tags, CUR_TZ, FAKER


class ModerationObjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True

    date_created = factory.Faker('date_time_between_dates',
                                 datetime_start='-2y',
                                 datetime_end=now(),
                                 tzinfo=CUR_TZ)
    date_updated = factory.Faker('date_time_between_dates',
                                 datetime_start=factory.SelfAttribute(
                                     '..date_created'),
                                 datetime_end=now(),
                                 tzinfo=CUR_TZ)

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        if create:
            as_published = randrange(10) > 2
            if as_published:
                l = ['published']
            else:
                l = ['draft', 'pending', 'rejected', 'not_published']
            choice = randchoice(l)
            match choice:
                case 'draft':
                    instance.save_as_draft()
                case 'pending':
                    instance.save_as_pending()
                case 'rejected':
                    instance.save_as_rejected(reason=FAKER.sentence())
                case 'not_published':
                    instance.save_as_not_published(reason=FAKER.sentence())
                case 'published':
                    edited_by_user = randrange(10) >= 4
                    date_published = FAKER.date_time_between_dates(datetime_start=instance.date_created,
                                                                   datetime_end=now(),
                                                                   tzinfo=CUR_TZ)
                    instance.save_as_published(date_published=date_published, edited_by_user=edited_by_user)
        super()._after_postgeneration(instance, create, results)


class SuperUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = rm.USER
        django_get_or_create = ('username',)

    username = 'admin'
    name = 'Administrator'
    password = factory.PostGenerationMethodCall('set_password', '1234')
    email = factory.LazyAttribute(lambda o: '%s@whatyouknow.com' % o.username)
    is_active = True
    is_staff = True
    is_superuser = True
    avatar = factory.django.FileField(
        filename=factory.LazyAttribute(
            lambda o: 'admin_' + rm.USER.avatar.field.name + '.jpg'),
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
    is_staff = factory.LazyAttribute(lambda o: randrange(10) == 0)
    is_superuser = False
    specialization = factory.Faker('job')
    description = factory.Faker('paragraph', nb_sentences=randint(10, 25))
    avatar = factory.django.FileField(
        filename=factory.LazyAttribute(
            lambda o: rm.USER.avatar.field.name + '_' + str(randint(1000000, 9999999)) + '.jpg'),
        data=factory.LazyAttribute(lambda o: get_image_file_data(min_width=300, min_height=300)))


class PostFactory(ModerationObjectFactory):
    class Meta:
        model = 'blog.Post'
        django_get_or_create = ('user', 'category', 'title')

    user = factory.Faker('random_element', elements=rm.USER.objects.filter(is_superuser=False))
    category = factory.LazyAttribute(lambda o: CategoryTypes.get_random_choices()[0])
    title = factory.Faker('sentence')
    feed_cover = factory.django.FileField(
        filename=factory.LazyAttribute(
            lambda o: rm.POST.feed_cover.field.name + '_' + str(randint(1000000, 9999999)) + '.jpg'),
        data=factory.LazyAttribute(
            lambda o: get_image_file_data(min_width=360, min_height=250)))
    feed_article_preview = factory.Maybe(
        factory.LazyFunction(lambda: randrange(10) > 0),
        yes_declaration=factory.Faker('text', max_nb_chars=factory.LazyAttribute(lambda o: randint(200, 500))),
        no_declaration=None)
    text = factory.LazyFunction(get_post_text)

    @factory.post_generation
    def post_tags(self, create, extracted, **kwargs):
        if create:
            self.tags.add(*get_tags(self.category))


class PostCommentsFactory(ModerationObjectFactory):
    class Meta:
        model = 'comments.Comment'
        django_get_or_create = ('content_type', 'object_id', 'user')

    class Params:
        is_comment_edited = factory.LazyAttribute(lambda o: randrange(3) == 0)  # for 1 out of 3 cases
        is_comment_reply = factory.LazyAttribute(lambda o: randrange(10) < 5)  # for 5 out of 10 cases

    content_object = factory.Faker('random_element',
                                   elements=rm.POST.objects.published())
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content_object))
    object_id = factory.SelfAttribute('content_object.pk')
    user = factory.Faker('random_element', elements=rm.USER.objects.filter(is_superuser=False))
    text = factory.Faker('text', max_nb_chars=factory.LazyAttribute(lambda o: randint(100, 1500)))

    @factory.lazy_attribute
    def parent(self):
        if self.is_comment_reply:
            qs = rm.COMMENT.objects.filter(
                content_type=self.content_type,
                object_id=self.object_id,
                date_created__gte=self.date_created
            )
            count = qs.count()
            if count > 0:
                return qs[randint(0, count - 1)]
            return None
        return None
