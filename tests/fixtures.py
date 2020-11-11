from .factories import *


def make_objects():
    CategoryFactory.create_batch(size=8)
    PostFactory.create_batch(size=10)
