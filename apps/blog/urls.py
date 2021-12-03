from django.urls import path, include

from .views import *


post_category_list_patterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('ajax/', include([
        path('post_list_load_data', PostListLoadDataView.as_view(), name='post_list_load_data'),
        path('post_list_container', PostListContainerView.as_view(), name='post_list_container'),
    ])),
]

post_list_patterns = [
    path('', PostRedirectDefaultCategoryListView.as_view(), name='post_list_default'),
    path('', include(post_category_list_patterns)),
    path('<str:category>/', include([
        path('', include(post_category_list_patterns)),
        path('<int:page>/', include(post_category_list_patterns)),
    ])),
]

post_create_patterns = [
    path('', PostCreateView.as_view(), name='post_create'),
    path('ajax/', include([
        path('create_container', PostCreateContainerView.as_view(), name='post_create_container'),
    ]))
]

post_detail_edit_patterns = [
    path('', PostDetailView.as_view(), name='post_detail'),
    path('edit/', PostEditView.as_view(), name='post_edit'),
    path('preview/', PostPreviewView.as_view(), name='post_preview'),
    path('done/', PostDoneView.as_view(), name='post_done'),
    path('ajax/', include([
        path('edit_container', PostEditContainerView.as_view(), name='post_edit_container'),
        path('preview_container', PostPreviewContainerView.as_view(), name='post_preview_container'),
        path('done_container', PostDoneContainerView.as_view(), name='post_done_container'),
    ])),
]

urlpatterns = [
    path('create/', include(post_create_patterns)),
    path('post/<int:pk>/<slug:slug>/', include(post_detail_edit_patterns)),
    path('', include(post_list_patterns)),
]
