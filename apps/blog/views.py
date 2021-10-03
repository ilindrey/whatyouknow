from django.http import Http404
from django.shortcuts import reverse
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now
from django.utils.translation import gettext as _

from dateutil.relativedelta import relativedelta

from .models import Post, CategoryTypes
from .mixins import PostCreateEditFormMixin


class PostRedirectDefaultListCategoryView(RedirectView):
    pattern_name = 'post_list_category'

    def get_redirect_url(self, *args, **kwargs):
        kwargs['category'] = 'feed'
        return super().get_redirect_url(*args, **kwargs)


class PostListLoadDataView(ListView):
    allow_empty = True
    model = Post
    template_name = 'blog/post/list/roll.html'
    paginate_by = 15
    ordering = '-timestamp'

    def get_queryset(self):
        filters = {}

        param = self.kwargs.get('category', 'feed')
        if param:
            if param in 'feed':
                if self.request.user.is_authenticated:
                    filters['category__in'] = self.request.user.settings['feed_categories']
                else:
                    filters['category__in'] = CategoryTypes.list('index')
            elif param in 'all':
                filters['category__in'] = CategoryTypes.list('index')
            else:
                category = None
                for cd in self.category_list:
                    if cd['short_name_lower'] == param:
                        category = cd['index']
                        break
                if category is None:
                    raise Http404(_('Invalid category (%(category_param)s)') % {
                        'category_param': param,
                        })
                filters['category'] = int(category)

        param = self.request.GET.get('period')
        if param:
            if param in 'day':
                filters['timestamp__gte'] = now() - relativedelta(days=+1)
            elif param in 'week':
                filters['timestamp__gte'] = now() - relativedelta(weeks=+1)
            elif param in 'month':
                filters['timestamp__gte'] = now() - relativedelta(months=+1)
            elif param in 'month':
                filters['timestamp__gte'] = now() - relativedelta(years=+1)

        param = self.request.GET.get('rating')
        if param:
            pass

        queryset = self.model.objects.filter(**filters).order_by(self.ordering)
        return queryset

    def get(self, request, *args, **kwargs):
        self.category_list = self.get_category_list()
        self.period_list = self.get_period_list()
        self.rating_list = self.get_rating_list()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'category_list': self.category_list,
            'period_list': self.period_list,
            'rating_list': self.rating_list,
            })
        return context

    @staticmethod
    def get_category_list():
        cl = CategoryTypes.get()
        for cd in cl:
            cd['short_name_lower'] = cd['short_name'].lower()
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


class PostListContainerView(PostListLoadDataView):
    template_name = 'blog/post/list/container.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'base_posts_url': reverse('post_list'),
            'ajax_suffix': 'ajax/post_list_load_data'
            })
        return context


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
