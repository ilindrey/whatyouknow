from random import randint, randrange
from datetime import datetime, timedelta

from django.utils.timezone import get_current_timezone

from mimesis_factory import MimesisField

from factory.django import DjangoModelFactory, ImageField
from factory import (
    LazyAttribute,
    LazyFunction,
    PostGenerationMethodCall,
    SubFactory, post_generation, lazy_attribute
    )

from .lazy_functions import get_category, get_post_params, get_tags

current_tz = get_current_timezone()


class UserProfileFactory(DjangoModelFactory):
    class Meta:
        model = "profiles.UserProfile"
        django_get_or_create = ("username",)

    username = MimesisField('username')
    password = PostGenerationMethodCall("set_password", "defaultpassword")
    first_name = MimesisField("first_name")
    last_name = MimesisField("last_name")
    email = MimesisField("email")
    is_staff = False
    is_active = True
    name = LazyAttribute(lambda obj: "{} {}".format(obj.first_name, obj.last_name))
    specialization = MimesisField("occupation")
    website = MimesisField("home_page")
    description = MimesisField("text", quantity=randint(1, 10))
    image = ImageField(color='gray', width=256, height=256)


class PostFactory(DjangoModelFactory):
    class Meta:
        model = "blog.Post"
        django_get_or_create = (
            "title",
            "user",
            "category",
            )

    class Params:
        param_list = LazyFunction(get_post_params)

    user = SubFactory(UserProfileFactory)

    @lazy_attribute
    def date(self):

        start_datetime = datetime(2020, 1, 1, tzinfo=current_tz)
        end_datetime = datetime.now(tz=current_tz)

        time_between_dates = end_datetime - start_datetime
        days_between_dates = time_between_dates.days

        random_number_of_days = randrange(days_between_dates)

        hours = randint(0, 23)
        minutes = randint(0, 59)
        seconds = randint(0, 59)
        microseconds = randint(0, 999)

        random_date = start_datetime + timedelta(days=random_number_of_days,
                                                 hours=hours,
                                                 minutes=minutes,
                                                 seconds=seconds,
                                                 microseconds=microseconds)
        return random_date

    category = LazyFunction(get_category)
    title = MimesisField("title")
    text = LazyAttribute(lambda o: o.param_list['text'])
    feed_cover = LazyAttribute(lambda o: o.param_list['feed_cover'])
    feed_cover_caption = LazyAttribute(lambda o: o.param_list['feed_cover_caption'])
    feed_article_preview = LazyAttribute(lambda o: o.param_list['feed_article_preview'])
    feed_read_more_button_name = LazyAttribute(lambda o: o.param_list['feed_read_more_button_name'])

    @post_generation
    def post_tags(self, create, extracted, **kwargs):
        self.tags.add(*get_tags(self.category))
