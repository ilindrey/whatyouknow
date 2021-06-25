from django.contrib.auth import login
from django.core.exceptions import ImproperlyConfigured
from django.http import JsonResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin

from taggit.models import Tag

from apps.blog.models import Post
from apps.comments.models import Comment

from .models import Profile
from .forms import EditAvatarForm, EditProfileForm, EditFeedSettingsForm, RegistrationForm


class ProfileMixin:
    model = Profile
    slug_field = 'username'
    slug_url_kwarg = 'username'


class EditProfileMixin:

    def get_success_url(self):
        return reverse('profile_settings', kwargs={'username': self.kwargs['username']})


class ProfileView(generic.RedirectView):
    pattern_name = 'profile_tab'

    def get_redirect_url(self, *args, **kwargs):
        kwargs['tab'] = 'posts'
        url = super().get_redirect_url(*args, **kwargs)
        return url


class ProfileTabView(ProfileMixin, generic.DetailView):
    template_name = 'profiles/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tab_header_list'] = {
            'posts': Post.objects.filter(user__username=self.kwargs['username']).count(),
            'comments': Comment.objects.filter(user__username=self.kwargs['username']).count()
            }
        context['current_tab'] = self.kwargs['tab']
        return context


class ProfileTabLoadDataListView(generic.ListView):
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

        if tab:
            tab_dir = 'profiles/detail/tabs/' + tab + '/'
            template_name = tab_dir + 'base.html' if page == 1 else tab_dir + 'list.html'
        else:
            raise ImproperlyConfigured(
                "%(cls)s requires either a 'template_name' attribute "
                "or a get_queryset() method that returns a QuerySet." % {
                    'cls': self.__class__.__name__, })

        return template_name


class SettingsView(LoginRequiredMixin, ProfileMixin, generic.DetailView):
    template_name = 'profiles/settings.html'


class EditProfileView(LoginRequiredMixin, ProfileMixin, EditProfileMixin, generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'profiles/settings/forms/edit_profile.html'


class EditAvatarView(LoginRequiredMixin, ProfileMixin, EditProfileMixin, generic.UpdateView):
    form_class = EditAvatarForm
    template_name = 'profiles/settings/forms/edit_avatar.html'


class EditFeedSettingsView(LoginRequiredMixin, ProfileMixin, generic.UpdateView):
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
        return reverse('profile_load_excluded_feed_tags', kwargs={'username': self.kwargs['username']})


class FeedSearchTags(LoginRequiredMixin, generic.ListView):
    model = Tag
    paginate_by = 10
    ordering = 'name'

    def get_queryset(self):
        search = self.request.GET.get('search')
        return super().get_queryset().filter(name__startswith=search).values('name')

    def render_to_response(self, context, **response_kwargs):
        tag_list = self.get_tag_list(context)
        json = {"results": tag_list}
        return JsonResponse(data=json, status=200)

    @staticmethod
    def get_tag_list(context):
        return [{'name': '<i class="tag icon"></i>' + item['name']} for item in context['object_list']]


class FeedLoadExcludedTags(LoginRequiredMixin, generic.ListView):
    model = Profile
    template_name = 'profiles/settings/forms/includes/excluded_feed_tags.html'

    def get_queryset(self):
        return self.model.objects.get(username=self.kwargs['username']).excluded_feed_tags.all().order_by('name')


class FeedDeleteExcludedTag(LoginRequiredMixin, ProfileMixin, generic.DeleteView):

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        tag = self.request.POST.get('tag')
        self.object.excluded_feed_tags.remove(tag)
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return reverse('profile_load_excluded_feed_tags', kwargs={'username': self.kwargs['username']})


class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'profiles/settings/forms/password_change_form.html'

    def get_success_url(self):
        return reverse('profile_password_change_done', kwargs={'username': self.kwargs['username']})


class PasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'profiles/settings/password_change_done.html'


class RegistrationView(generic.CreateView):
    model = Profile
    form_class = RegistrationForm
    template_name = 'registration/registration.html'

    def get_success_url(self):
        return reverse('index')
    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['user'] = None
    #     return kwargs

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        login(self.request, self.object)
        return HttpResponseRedirect(self.get_success_url())