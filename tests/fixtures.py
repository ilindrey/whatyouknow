from .factories import PostFactory


def make_objects():
    # CategoryFactory.create_batch(size=8)
    # UserProfileFactory.create_batch(size=20)
    PostFactory.create_batch(size=16)
