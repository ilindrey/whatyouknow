from django.http import Http404
from django.shortcuts import reverse
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now
from django.utils.translation import gettext as _

from dateutil.relativedelta import relativedelta

from .models import Post, CategoryTypes
from .mixins import PostCreateEditFormMixin


class PostRedirectDefaultCategoryListView(RedirectView):
    pattern_name = 'post_list'

    def get_redirect_url(self, *args, **kwargs):
        kwargs['category'] = 'feed'
        return super().get_redirect_url(*args, **kwargs)


class PostListLoadDataView(ListView):
    allow_empty = True
    model = Post
    template_name = 'blog/post/list/roll_out.html'
    paginate_by = 15
    ordering = '-created'

    def get_queryset(self):
        filters = {}
        excludes = {}

        param = self.kwargs.get('category') or self.request.GET.getlist('category') or 'all'
        if param:
            if isinstance(param, str):
                param = [param]
            if 'all' in param:
                pass
            elif 'feed' in param:
                if self.request.user.is_authenticated:
                    filters['category__in'] = self.request.user.settings['feed_categories']
                    excludes['tags__name__in'] = self.request.user.excluded_feed_tags.names()
            else:
                category_list = CategoryTypes.get_values(*param, key='short_name_lower')
                if category_list is None:
                    raise Http404(_('Invalid category (%(category_param)s)') % {'category_param': param})
                filters['category__in'] = [category['index'] for category in category_list]

        param = self.request.GET.get('period')
        if param:
            if 'day' in param:
                filters['created__gte'] = now() - relativedelta(days=+1)
            elif 'week' in param:
                filters['created__gte'] = now() - relativedelta(weeks=+1)
            elif 'month' in param:
                filters['created__gte'] = now() - relativedelta(months=+1)
            elif 'year' in param:
                filters['created__gte'] = now() - relativedelta(years=+1)

        param = self.request.GET.get('rating')
        if param:
            pass

        param = self.request.GET.getlist('tag')
        if param:
            filters['tags__name__in'] = param

        param = self.request.GET.get('text')
        if param:
            filters['title__startswith'] = param

        queryset = self.model.objects.filter(**filters).exclude(**excludes).order_by(self.ordering)
        return queryset


class PostListContainerView(PostListLoadDataView):
    template_name = 'blog/post/list/container.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'category_list': self.get_category_list(),
            'rating_list': self.get_rating_list(),
            'period_list': self.get_period_list(),
            'cur_category': self.kwargs.get('category', 'feed'),
            'cur_page': context['page_obj'].number
            })
        return context

    @staticmethod
    def get_category_list():
        cl = CategoryTypes.get()
        cl.insert(0, {'index': -1, 'short_name': 'All', 'short_name_lower': 'all', 'full_name': 'All posts'})
        cl.insert(0, {'index': -2, 'short_name': 'Feed', 'short_name_lower': 'feed', 'full_name': 'My feed'})
        return cl

    @staticmethod
    def get_period_list():
        return [('day', 'Day'),
                ('week', 'Week'),
                ('month', 'Month'),
                ('year', 'Year')]

    @staticmethod
    def get_rating_list():
        return [(25, 25),
                (50, 50),
                (75, 75),
                (85, 85)]


class PostListView(PostListContainerView):
    template_name = 'blog/post/list.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post/detail.html'


class PostCreateView(PostCreateEditFormMixin, CreateView):
    template_name = 'blog/post/edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['post_write_url'] = reverse('post_create_container')
        context['cur_url'] = reverse('post_create')
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostEditView(PostCreateEditFormMixin, UpdateView):
    template_name = 'blog/post/edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['post_write_url'] = reverse('post_edit_container', kwargs=self.kwargs)
        context['cur_url'] = reverse('post_edit', kwargs=self.kwargs)
        return context


class PostPreviewView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/post/preview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['cur_url'] = reverse('post_preview', kwargs=self.kwargs)
        return context


class PostDoneView(LoginRequiredMixin, TemplateView):  # set status in moderation
    template_name = 'blog/post/done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['cur_url'] = reverse('post_done', kwargs=self.kwargs)
        return context


class PostCreateContainerView(PostCreateView):
    template_name = 'blog/post/edit/container.html'


class PostEditContainerView(PostEditView):
    template_name = 'blog/post/edit/container.html'


class PostPreviewContainerView(PostPreviewView):
    template_name = 'blog/post/preview/container.html'


class PostDoneContainerView(PostDoneView):
    template_name = 'blog/post/done/container.html'
