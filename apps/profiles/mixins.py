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


class ProfileTabStructureMixin:

    @property
    def default_tab_params(self):
        return {
            'count': None,
            'is_lazy_load': False,
            'link_load_data': None,
            'link_lazy_load': None,
            'is_descendant_menu': False,
            'descendant_tab_list': None,
            'step_context': '.ui.items',
            }


class ProfileTabListMixin(ProfileAuthMixin):
    paginate_by = 10

    def get_queryset(self):
        if self.is_auth_user:
            self.queryset = self.model._default_manager.all()
        else:
            self.queryset = self.model._default_manager.approved()
        return super().get_queryset().filter(user__username=self.kwargs[self.slug_url_kwarg])
