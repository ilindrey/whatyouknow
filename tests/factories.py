from random import randint

import faker
from django.utils import timezone

from factory.django import DjangoModelFactory, ImageField
from factory import (
    LazyAttribute,
    Faker,
    PostGenerationMethodCall,
    SubFactory,
    post_generation,
    Iterator,
)


fake = faker.Faker()


class UserProfileFactory(DjangoModelFactory):
    class Meta:
        model = "profiles.UserProfile"
        django_get_or_create = ("username",)

    username = Faker("user_name")
    password = PostGenerationMethodCall("set_password", "defaultpassword")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    email = Faker("email")
    is_staff = False
    is_active = True
    name = LazyAttribute(lambda obj: "{} {}".format(obj.first_name, obj.last_name))
    website = Faker("url")
    description = Faker("text")
    image = ImageField(color='gray', width=500, height=300)


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = "blog.Category"
        django_get_or_create = ("name",)

    name = Iterator(
        [
            "Technology",
            "Development",
            "Administration",
            "Design",
            "Business",
            "Management",
            "Marketing",
            "Popular science",
        ]
    )
    order = Iterator([1, 2, 3, 4, 5, 6, 7, 8])


class PostFactory(DjangoModelFactory):
    class Meta:
        model = "blog.Post"
        django_get_or_create = (
            "name",
            "user",
            "category",
        )

    user = SubFactory(UserProfileFactory)
    category = SubFactory(CategoryFactory)
    name = Faker("sentence")
    date = Faker(
        "date_time_between",
        start_date="-2y",
        end_date="now",
        tzinfo=timezone.get_current_timezone(),
    )
    image = ImageField(color='gray', width=4096, height=3072)
    description = Faker("text", max_nb_chars=randint(1000, 100000))

    @post_generation
    def post_tags(self, create, extracted, **kwargs):
        self.tags.add(*fake.words(nb=randint(1, 10)))
