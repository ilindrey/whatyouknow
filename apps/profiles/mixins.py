from .models import Profile


class ProfileMixin:
    model = Profile
    slug_field = 'username'
    slug_url_kwarg = 'username'

