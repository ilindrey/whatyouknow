
from ..core.mixins import BaseHasPermsMixin
from .models import Profile


class HasPermsMixin(BaseHasPermsMixin):

    @property
    def is_cur_auth_user(self):
        return self.request.user.username == self.kwargs.get('username')

    @property
    def has_perms(self):
        return self.is_cur_auth_user or super().has_perms


class ProfileMixin(HasPermsMixin):
    model = Profile
    slug_field = 'username'
    slug_url_kwarg = 'username'


class ProfileTabListMixin(ProfileMixin):
    paginate_by = 10
    ordering = '-date_updated'

    def get_queryset(self):
        if self.has_perms:
            self.queryset = self.model._default_manager.all()
        else:
            self.queryset = self.model._default_manager.published()
        return super().get_queryset().filter(user__username=self.kwargs[self.slug_url_kwarg])
