from django.urls import path, include

from .views import *


post_ajax_list_patterns = [
    path('post_list_load_data', PostListLoadDataView.as_view(), name='post_list_load_data'),
    path('post_list_container', PostListContainerView.as_view(), name='post_list_container'),
    ]

post_list_patterns = [
    path('', PostRedirectDefaultListCategoryView.as_view(), name='post_list'),
    path('<str:category>/', include([
        path('', PostListView.as_view(), name='post_list_category'),
        path('ajax/', include(post_ajax_list_patterns)),
        path('<int:page>/', include([
            path('', PostListView.as_view(), name='post_list_category_page'),
            path('ajax/', include(post_ajax_list_patterns)),
            ])),
        ])),
    ]

post_create_patterns = [
    path('', PostCreateView.as_view(), name='post_create'),
    path('ajax/', include([
        path('create_container', PostCreateContainerView.as_view(), name='post_create_container'),
        ]))
    ]

post_edit_patterns = [
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
    path('<int:pk>/', include([
        path('', PostDetailView.as_view(), name='post_detail'),
        path('', include(post_edit_patterns)),
        ])),
    path('', include(post_list_patterns)),
    ]
