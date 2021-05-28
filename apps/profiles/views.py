from django.core.exceptions import ImproperlyConfigured
from django.views import generic
from django.urls import reverse

from apps.blog.models import Post
from apps.comments.models import Comment

from .models import Profile
from .forms import AvatarForm, ProfileForm, FeedForm


class ProfileView(generic.RedirectView):
    pattern_name = 'profile_tab'

    def get_redirect_url(self, *args, **kwargs):
        kwargs['tab'] = 'posts'
        url = super().get_redirect_url(*args, **kwargs)
        return url


class ProfileTabView(generic.DetailView):
    slug_field = 'username'
    slug_url_kwarg = 'username'
    model = Profile
    template_name = 'profiles/detail.html'

    def get_context_data(self, **kwargs):

        context = super(ProfileTabView, self).get_context_data(**kwargs)

        context['tab_header_list'] = {
            'posts': Post.objects.filter(user__username=self.kwargs['username']).count(),
            'comments': Comment.objects.filter(user__username=self.kwargs['username']).count()
            }

        context['current_tab'] = self.kwargs['tab']

        return context


class ProfileTabDataLoadListView(generic.ListView):
    paginate_by = 10

    def get_queryset(self):
        tab = self.request.GET.get('tab')
        if tab == 'posts':
            return Post.objects.filter(user__username=self.kwargs['username'])
        elif tab == 'comments':
            return Comment.objects.filter(user__username=self.kwargs['username'])
        else:
            return None

    def get_template_names(self):

        tab = self.request.GET.get('tab')
        page = int(self.request.GET.get('page', 1))

        base_tab_dir = 'profiles/includes/tabs/'

        if tab == 'posts':
            template = 'pt_post_base.html' if page == 1 else 'list/pt_post_list.html'
        elif tab == 'comments':
            template = 'pt_comment_base.html' if page == 1 else 'list/pt_comment_list.html'
        else:
            raise ImproperlyConfigured(
                "%(cls)s requires either a 'template_name' attribute "
                "or a get_queryset() method that returns a QuerySet." % {
                    'cls': self.__class__.__name__, })

        return base_tab_dir + template


class ProfileMixin:
    model = Profile
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_success_url(self):
        return reverse('profile_settings', kwargs={'username': self.kwargs['username']})


class ProfileSettingsView(ProfileMixin, generic.UpdateView):
    form_class = ProfileForm
    template_name = 'profiles/settings.html'


class ProfileAvatarView(ProfileMixin, generic.UpdateView):
    form_class = AvatarForm
    template_name = 'profiles/includes/settings/forms/avatar.html'


class ProfileFeedView(ProfileMixin, generic.FormView):
    form_class = FeedForm
    template_name = 'profiles/includes/settings/forms/feed.html'
