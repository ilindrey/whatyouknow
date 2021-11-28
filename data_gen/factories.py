from random import randint, randrange, choice as randchoice

from django.utils.timezone import now
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

import factory

from apps.blog.models import Post, CategoryTypes
from apps.comments.models import Comment

from .utils import get_image_file_data, get_post_text, get_tags, CUR_TZ, FAKER


USER_MODEL = get_user_model()


class ModerationObjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True

    date_created = factory.Faker('date_time_between_dates',
                                 datetime_start='-2y',
                                 datetime_end=now(),
                                 tzinfo=CUR_TZ)

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        if create:
            date_updated = FAKER.date_time_between_dates(datetime_start=instance.date_created,
                                                         datetime_end=now(),
                                                         tzinfo=CUR_TZ)
            kwargs = {'date_updated': date_updated}

            as_published = randrange(10) > 2
            if as_published:
                l = ['published']
            else:
                l = ['draft', 'pending', 'rejected', 'not_published']
            choice = randchoice(l)
            match choice:
                case 'draft':
                    instance.save_as_draft(**kwargs)
                case 'pending':
                    instance.save_as_pending(**kwargs)
                case 'rejected':
                    instance.save_as_rejected(reason=FAKER.sentence(), **kwargs)
                case 'not_published':
                    instance.save_as_not_published(reason=FAKER.sentence(), **kwargs)
                case 'published':
                    kwargs.update({
                        'date_published': FAKER.date_time_between_dates(datetime_start=date_updated, datetime_end=now(), tzinfo=CUR_TZ),
                        'edited_by_user': randrange(10) >= 4,
                    })
                    instance.save_as_published(**kwargs)
        super()._after_postgeneration(instance, create, results)


class StaffGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'auth.Group'
        django_get_or_create = ('name',)

    name = 'staff'

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        if create:
            permissions = {
                'blog.Post': ['add', 'change', 'delete', 'view'],
                'comments.Comment': ['add', 'change', 'delete', 'view'],
                get_user_model(): ['change', 'view'],
            }
            for key_model, model_list in permissions.items():

                if isinstance(key_model, str) and '.' in key_model:
                    app, model_name = key_model.split('.', 1)
                    model = factory.django.get_model(app, model_name)
                else:
                    model = key_model
                content_type = ContentType.objects.get_for_model(model)

                for key in model_list:
                    codename = key + '_' + model._meta.model_name
                    permission = Permission.objects.get(codename=codename, content_type=content_type)
                    instance.permissions.add(permission)

        super()._after_postgeneration(instance, create, results)


class SuperUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = USER_MODEL
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
            lambda o: 'admin_' + USER_MODEL.avatar.field.name + '.jpg'),
        data=factory.LazyAttribute(
            lambda o: get_image_file_data(min_width=300, min_height=300)))


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = USER_MODEL
        django_get_or_create = ('username',)

    name = factory.Faker('name')
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', '1234')
    is_active = True
    is_staff = factory.LazyAttribute(lambda o: randrange(10) == 0)
    is_superuser = False
    specialization = factory.Faker('job')
    description = factory.Faker('paragraph', nb_sentences=randint(10, 25))
    avatar = factory.django.FileField(
        filename=factory.LazyAttribute(
            lambda o: USER_MODEL.avatar.field.name + '_' + str(randint(1000000, 9999999)) + '.jpg'),
        data=factory.LazyAttribute(lambda o: get_image_file_data(min_width=300, min_height=300)))

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        if create:
            if instance.is_staff:
                staff_group = Group.objects.get(name=StaffGroupFactory.name)
                instance.groups.add(staff_group)
        super()._after_postgeneration(instance, create, results)


class PostFactory(ModerationObjectFactory):
    class Meta:
        model = 'blog.Post'
        django_get_or_create = ('user', 'category', 'title')

    user = factory.Faker('random_element', elements=USER_MODEL.objects.filter(is_superuser=False))
    category = factory.LazyAttribute(lambda o: CategoryTypes.get_random_choices()[0])
    title = factory.Faker('sentence')
    feed_cover = factory.django.FileField(
        filename=factory.LazyAttribute(
            lambda o: Post.feed_cover.field.name + '_' + str(randint(1000000, 9999999)) + '.jpg'),
        data=factory.LazyAttribute(
            lambda o: get_image_file_data(min_width=360, min_height=250)))
    feed_article_preview = factory.Maybe(
        factory.LazyFunction(lambda: randrange(10) > 0),
        yes_declaration=factory.Faker('text', max_nb_chars=factory.LazyAttribute(lambda o: randint(200, 500))),
        no_declaration=None)
    text = factory.LazyFunction(get_post_text)

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        if create:
            instance.tags.add(*get_tags(instance.category))
        super()._after_postgeneration(instance, create, results)


class PostCommentsFactory(ModerationObjectFactory):
    class Meta:
        model = 'comments.Comment'
        django_get_or_create = ('content_type', 'object_id', 'user', 'date_created')

    content_object = factory.Faker('random_element', elements=Post.objects.published())
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content_object))
    object_id = factory.SelfAttribute('content_object.pk')
    user = factory.Faker('random_element', elements=USER_MODEL.objects.filter(is_superuser=False))
    text = factory.Faker('text', max_nb_chars=factory.LazyAttribute(lambda o: randint(100, 1500)))
    date_created = factory.Faker('date_time_between_dates',
                                 datetime_start=factory.SelfAttribute('..content_object.date_published'),
                                 datetime_end=now(),
                                 tzinfo=CUR_TZ)

    @factory.lazy_attribute
    def parent(self):
        id_reply = randrange(10) < 5   # for 5 out of 10 cases
        if id_reply:
            qs = Comment.objects.filter(
                content_type=self.content_type,
                object_id=self.object_id,
                date_created__lte=self.date_created
            )
            count = qs.count()
            return qs[randint(0, count - 1)] if count > 0 else None
        return None
