from random import randint, choice

from django.utils.timezone import get_current_timezone_name

from mimesis_factory import MimesisField

from factory.django import DjangoModelFactory, ImageField
from factory import (
    LazyAttribute,
    LazyFunction,
    PostGenerationMethodCall,
    SubFactory, post_generation,
    )

from .lazy_functions_for_factories import get_category, get_post_params, get_tags

from whatyouknow.blog.models import CATEGORY_CHOICES

# from .mimesis.providers.post import Post


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
    website = MimesisField("home_page")
    description = MimesisField("text", quantity=randint(1, 10))
    image = ImageField(color='gray', width=500, height=300)


# class CategoryFactory(DjangoModelFactory):
#     class Meta:
#         model = "blog.Category"
#         django_get_or_create = ("name",)
#
#     name = Iterator(
#         [
#             "Technology",
#             "Development",
#             "Administration",
#             "Design",
#             "Business",
#             "Management",
#             "Marketing",
#             "Popular science",
#         ]
#     )
#     order = Iterator([1, 2, 3, 4, 5, 6, 7, 8])


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
    date = MimesisField(
        "datetime",
        start=2018,
        end=2021,
        timezone=get_current_timezone_name(),
    )
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
