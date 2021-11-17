from django.contrib.auth import login
from django.http import HttpResponseRedirect, Http404
from django.views import generic
from django.urls import reverse
from django.utils.translation import gettext as _
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.blog.models import Post
from apps.comments.models import Comment

from .models import Profile
from .forms import EditProfileForm, EditFeedSettingsForm, RegistrationForm
from .mixins import CurrentAuthUserMixin, ProfileAuthMixin, ProfileTabStructureMixin, ProfileTabListMixin


class ProfileView(ProfileAuthMixin, ProfileTabStructureMixin, generic.DetailView):
    template_name = 'profiles/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        default_first_tab = 'posts'
        default_second_tab = 'all'

        first_tab = self.kwargs.get('first_tab', default_first_tab)
        second_tab = self.kwargs.get('second_tab', default_second_tab)

        if first_tab == 'settings':
            raise Http404(_('Invalid profile setting page (%(first_tab)s): %(second_tab)s') % {
                'first_tab': first_tab,
                'second_tab': second_tab
            })

        username = self.kwargs[self.slug_url_kwarg]
        default_kwargs = {self.slug_url_kwarg: username}

        # posts
        tab_posts_kwargs = {**default_kwargs, 'first_tab': 'posts'}
        tab_posts_params = self.default_tab_params
        tab_posts_params.update({
            'count': ProfilePostsTabBaseLoadDataListView(request=self.request, kwargs=self.kwargs).get_queryset().count(),
            'is_lazy_load': True,
            'link_load_data': reverse('posts_tab_base_load_data', kwargs=tab_posts_kwargs),
            'link_lazy_load': reverse('posts_tab_lazy_load_data', kwargs=tab_posts_kwargs),
        })

        # comments
        tab_comments_kwargs = {**default_kwargs, 'first_tab': 'comments'}
        tab_comments_params = self.default_tab_params
        tab_comments_params.update({
            'count': ProfileCommentsTabLoadDataListView(request=self.request, kwargs=self.kwargs).get_queryset().count(),
            'is_lazy_load': True,
            'link_load_data': reverse('comments_tab_base_load_data', kwargs=tab_comments_kwargs),
            'link_lazy_load': reverse('comments_tab_lazy_load_data', kwargs=tab_comments_kwargs),
        })

        tab_list = {
            'posts': tab_posts_params,
            'comments': tab_comments_params,
        }

        first_tab_data = tab_list.get(first_tab)
        if first_tab_data is None:
            first_tab = default_first_tab
        else:
            descendant_tab_list = first_tab_data.get('descendant_tab_list')
            if descendant_tab_list:
                second_tab_data = descendant_tab_list.get(second_tab)
                if second_tab_data is None:
                    second_tab = default_second_tab
            else:
                second_tab = None

        context['first_tab'] = first_tab
        context['second_tab'] = second_tab
        context['tab_list'] = tab_list
        context['base_pathname_url'] = reverse('profile_detail', kwargs=default_kwargs)

        return context


class ProfileFirstTabView(ProfileView):
    pass


class ProfileSecondTabView(ProfileFirstTabView):
    pass


class ProfilePostsTabBaseLoadDataListView(ProfileTabListMixin, generic.ListView):
    model = Post
    template_name = 'profiles/detail/tabs/content/posts/base.html'


class ProfilePostsTabLazyLoadDataListView(ProfilePostsTabBaseLoadDataListView):
    template_name = 'profiles/detail/tabs/content/posts/list.html'


class ProfileCommentsTabLoadDataListView(ProfileTabListMixin, generic.ListView):
    model = Comment
    template_name = 'profiles/detail/tabs/content/comments/base.html'


class ProfileCommentsTabLazyDataListView(ProfileCommentsTabLoadDataListView):
    model = Comment
    template_name = 'profiles/detail/tabs/content/comments/list.html'


class SettingsView(LoginRequiredMixin, ProfileAuthMixin, generic.DetailView):
    template_name = 'profiles/settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tab = self.kwargs.get('tab', 'profile')
        if tab not in self.get_tab_list():
            raise Http404(_('Invalid profile setting tab: (%(tab)s)') % {
                'tab': tab,
                })
        context['cur_tab'] = tab
        return context

    @staticmethod
    def get_tab_list():
        return ['profile', 'password', 'feed']


class EditProfileView(LoginRequiredMixin, ProfileAuthMixin, generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'profiles/settings/forms/edit_profile.html'

    def get_success_url(self):
        return reverse('edit_profile', kwargs={self.slug_url_kwarg: self.object.username})


class EditFeedView(LoginRequiredMixin, ProfileAuthMixin, generic.UpdateView):
    form_class = EditFeedSettingsForm
    template_name = 'profiles/settings/forms/edit_feed_settings.html'

    def get_initial(self):
        if 'feed_categories' in self.object.settings:
            categories = self.object.settings['feed_categories']
        else:
            categories = []
        self.initial = {'categories': categories}
        return super().get_initial()

    def get_success_url(self):
        return reverse('edit_feed', kwargs={self.slug_url_kwarg: self.kwargs[self.slug_url_kwarg]})


class PasswordChangeView(LoginRequiredMixin, CurrentAuthUserMixin, PasswordChangeView):
    template_name = 'profiles/settings/forms/password_change_form.html'

    def get_success_url(self):
        return reverse('password_change_done', kwargs={'username': self.kwargs['username']})


class PasswordChangeDoneView(LoginRequiredMixin, CurrentAuthUserMixin, PasswordChangeDoneView):
    template_name = 'profiles/settings/password_change_done.html'


class RegistrationView(generic.CreateView):
    model = Profile
    form_class = RegistrationForm
    template_name = 'reg/registration.html'

    def get_success_url(self):
        return reverse('index')

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        login(self.request, self.object)
        return HttpResponseRedirect(self.get_success_url())
