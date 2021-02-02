from django.contrib.auth import get_user_model
from factory.django import get_model


class ReferenceModel:
    USER = get_user_model()
    POST = get_model('blog', 'Post')
    COMMENT = get_model('comments', 'Comment')
