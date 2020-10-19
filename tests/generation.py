
from whatyouknow.blog.models import Category

from .data.categories import categories


def generation_data():

    Category.objects.all().delete()

    for category in categories:
        Category.objects.create(**category)
