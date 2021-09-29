from django.shortcuts import reverse
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now

from dateutil.relativedelta import relativedelta

from .models import Post, CategoryTypes
from .mixins import PostCreateEditFormMixin


class PostListLoadDataView(ListView):
    allow_empty = True
    model = Post
    template_name = 'blog/post/list/roll.html'
    paginate_by = 15
    ordering = '-timestamp'

    def get_queryset(self):
        category_param = self.request.GET.get('category', 'my')
        period_param = self.request.GET.get('period')
        rating_param = self.request.GET.get('rating')

        filters = {}
        if category_param:
            categories = []
            if category_param in 'my':
                if self.request.user.is_authenticated:
                    categories = self.request.user.settings['feed_categories']
            elif category_param in 'all':
                categories = CategoryTypes.get_list_index()
            else:
                categories.append(int(category_param))
            filters['category__in'] = categories
        if period_param:
            if period_param in 'day':
                filters['timestamp__gte'] = now() - relativedelta(days=+1)
            elif period_param in 'week':
                filters['timestamp__gte'] = now() - relativedelta(weeks=+1)
            elif period_param in 'month':
                filters['timestamp__gte'] = now() - relativedelta(months=+1)
            elif period_param in 'month':
                filters['timestamp__gte'] = now() - relativedelta(years=+1)

        queryset = self.model.objects.filter(**filters).order_by(self.ordering)
        return queryset


class PostListContainerView(PostListLoadDataView):
    template_name = 'blog/post/list/container.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'category_list': self.get_category_list(),
            'period_list': self.get_period_list(),
            'rating_list': self.get_rating_list(),
            })
        return context

    @staticmethod
    def get_category_list():
        category_list = CategoryTypes.get_list()
        category_list.insert(0, ('all', 'All posts'))
        category_list.insert(0, ('my', 'My feed'))
        return category_list

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
