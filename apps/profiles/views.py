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

        tab_posts_all_kwargs = {**tab_posts_kwargs, 'second_tab': 'all'}
        tab_posts_all_params = self.default_tab_params
        tab_posts_all_params.update({
            'count': Post.objects.filter(user__username=username).count(),
            'is_lazy_load': True,
            'link_load_data': reverse('posts_all_tab_base_load_data', kwargs=tab_posts_all_kwargs),
            'link_lazy_load': reverse('posts_all_tab_lazy_load_data', kwargs=tab_posts_all_kwargs),
        })

        tab_posts_drafts_kwargs = {**tab_posts_kwargs, 'second_tab': 'drafts'}
        tab_posts_drafts_params = self.default_tab_params
        tab_posts_drafts_params.update({
            'count': Post.objects.drafts().filter(user__username=username).count(),
            'is_lazy_load': True,
            'link_load_data': reverse('posts_drafts_tab_base_load_data', kwargs=tab_posts_drafts_kwargs),
            'link_lazy_load': reverse('posts_drafts_tab_lazy_load_data', kwargs=tab_posts_drafts_kwargs),
        })

        tab_posts_rejected_kwargs = {**tab_posts_kwargs, 'second_tab': 'rejected'}
        tab_posts_rejected_params = self.default_tab_params
        tab_posts_rejected_params.update({
            'count': Post.objects.rejected().filter(user__username=username).count(),
            'is_lazy_load': True,
            'link_load_data': reverse('posts_rejected_tab_base_load_data', kwargs=tab_posts_rejected_kwargs),
            'link_lazy_load': reverse('posts_rejected_tab_lazy_load_data', kwargs=tab_posts_rejected_kwargs),
        })

        tab_posts_params = self.default_tab_params
        tab_posts_params.update({
            'count': Post.objects.filter(user__username=username).count(),
            # 'link_load_data': reverse('posts_tab_load_data', kwargs=tab_posts_kwargs),
            'is_descendant_menu': True,
            'descendant_tab_list': {
                'all': tab_posts_all_params,
                'drafts': tab_posts_drafts_params,
                'rejected': tab_posts_rejected_params,
            }
        })

        # comments

        tab_comments_kwargs = {**default_kwargs, 'first_tab': 'comments'}
        tab_comments_params = self.default_tab_params
        tab_comments_params.update({
            'count': Comment.objects.filter(user__username=username).count(),
            'link_load_data': reverse('comments_tab_load_data', kwargs=tab_comments_kwargs),
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


class ProfilePostsAllTabBaseLoadDataListView(ProfileTabListMixin, generic.ListView):
    model = Post
    template_name = 'profiles/detail/tabs/content/posts/base.html'


class ProfilePostsAllTabLazyLoadDataListView(ProfilePostsAllTabBaseLoadDataListView):
    template_name = 'profiles/detail/tabs/content/posts/list.html'


class ProfilePostsDraftsTabBaseLoadDataListView(ProfileTabListMixin, generic.ListView):
    queryset = Post.objects.drafts()
    template_name = 'profiles/detail/tabs/content/posts/base.html'


class ProfilePostsDraftsTabLazyLoadDataListView(ProfilePostsDraftsTabBaseLoadDataListView):
    template_name = 'profiles/detail/tabs/content/posts/base.html'


class ProfilePostsRejectedTabBaseLoadDataListView(ProfileTabListMixin, generic.ListView):
    queryset = Post.objects.rejected()
    template_name = 'profiles/detail/tabs/content/posts/base.html'


class ProfilePostsRejectedTabLazyLoadDataListView(ProfilePostsRejectedTabBaseLoadDataListView):
    template_name = 'profiles/detail/tabs/content/posts/base.html'


class ProfileCommentsTabLoadDataListView(ProfileTabListMixin, generic.ListView):
    model = Comment

    def get_template_names(self):
        page = int(self.request.GET.get('page', 1))
        self.template_name = 'profiles/detail/tabs/content/comments/' + \
            'base.html' if page == 1 else self.tab_dir + 'list.html'
        return super().get_template_names()


class SettingsView(LoginRequiredMixin, ProfileAuthMixin, generic.DetailView):
    template_name = 'profiles/settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tab = self.kwargs.get('tab', 'profile')
        if tab not in self.get_tab_list():
            raise Http404(_('Invalid profile setting tab: (%(tab)s)') % {
                'first_tab': tab,
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
