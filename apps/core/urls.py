from django.urls import path, include

from .views import IndexView, SearchView, SearchContainerView, SearchDropdownResultsView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('search/', include([
        path('', SearchView.as_view(), name='search'),
        path('ajax/', include([
            path('container', SearchContainerView.as_view(), name='search_container'),
            path('search_dropdown_results', SearchDropdownResultsView.as_view(), name='search_dropdown_results'),
            ]))
        ])),
]
