from django.core.exceptions import ImproperlyConfigured
from django.http import JsonResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse

from taggit.models import Tag

from apps.blog.models import Post
from apps.comments.models import Comment

from .models import Profile
from .forms import EditAvatarForm, EditProfileForm, FeedSettingsForm


class ProfileMixin:
    model = Profile
    slug_field = 'username'
    slug_url_kwarg = 'username'


class ProfileEditMixin:

    def get_success_url(self):
        return reverse('profile_edit', kwargs={'username': self.kwargs['username']})


class ProfileView(generic.RedirectView):
    pattern_name = 'profile_tab'

    def get_redirect_url(self, *args, **kwargs):
        kwargs['tab'] = 'posts'
        url = super().get_redirect_url(*args, **kwargs)
        return url


class TabProfileView(ProfileMixin, generic.DetailView):
    template_name = 'profiles/detail.html'

    def get_context_data(self, **kwargs):
        context = super(TabProfileView, self).get_context_data(**kwargs)
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

        base_tab_dir = 'profiles/detail/tabs/'
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


class EditProfileView(ProfileMixin, ProfileEditMixin, generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'profiles/settings.html'


class EditAvatarProfileView(ProfileMixin, ProfileEditMixin, generic.UpdateView):
    form_class = EditAvatarForm
    template_name = 'profiles/settings/forms/edit_avatar.html'


class FeedSettingsProfileView(ProfileMixin, generic.UpdateView):
    form_class = FeedSettingsForm
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


class FeedSearchTags(generic.ListView):
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


class FeedLoadExcludedTags(generic.ListView):
    model = Profile
    template_name = 'profiles/settings/forms/annexes/excluded_feed_tags.html'

    def get_queryset(self):
        return self.model.objects.get(username=self.kwargs['username']).excluded_feed_tags.all().order_by('name')


class FeedDeleteExcludedTag(ProfileMixin, generic.DeleteView):

    def delete(self, request, *args, **kwargs):

        self.object = self.get_object()
        success_url = self.get_success_url()

        tag = self.request.POST.get('tag')
        self.object.excluded_feed_tags.remove(tag)

        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return reverse('profile_load_excluded_feed_tags', kwargs={'username': self.kwargs['username']})
