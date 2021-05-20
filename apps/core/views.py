from django.views.generic import RedirectView


class IndexView(RedirectView):
    pattern_name = 'post_list'
