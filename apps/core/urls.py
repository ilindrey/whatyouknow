from django.urls import path, include

from .views import IndexView, SearchView, SearchContainerView, SearchSuitableResultsListView, SearchSelectionsView


search_patterns = [
    path('', SearchView.as_view(), name='search'),
    path('ajax/', include([
        path('container', SearchContainerView.as_view(), name='search_container'),
        path('load_selections', SearchSelectionsView.as_view(), name='search_selections'),
        path('load_suitable_results', SearchSuitableResultsListView.as_view(), name='search_suitable_results'),
    ]))
]

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('search/', include([
        path('', include(search_patterns)),
        path('<int:page>/', include(search_patterns)),
    ])),
]
