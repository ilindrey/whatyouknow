from .models import Profile


class CurrentAuthUserMixin:

    @property
    def is_auth_user(self):
        return self.request.user.is_authenticated and self.request.user.username == self.kwargs['username']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_auth_user'] = self.is_auth_user
        return context


class ProfileAuthMixin(CurrentAuthUserMixin):
    model = Profile
    slug_field = 'username'
    slug_url_kwarg = 'username'


