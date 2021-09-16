from django.urls import path, include

from .views import *


post_edit_patterns = [
    path('edit/', PostEditView.as_view(), name='post_edit'),
    path('preview/', PostPreviewView.as_view(), name='post_preview'),
    path('done/', PostDoneView.as_view(), name='post_done'),
    path('ajax/', include([
        path('edit_load_data', PostEditContainerView.as_view(), name='post_edit_load_data'),
        path('preview_load_data', PostPreviewContainerView.as_view(), name='post_preview_load_data'),
        path('done_load_data', PostDoneContainerView.as_view(), name='post_done_load_data'),
        ])),
    ]

post_create_patterns = [
    path('', PostCreateView.as_view(), name='post_create'),
    path('ajax/', include([
        path('create_load_data', PostCreateContainerView.as_view(), name='post_create_load_data'),
        ]))
    ]

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('create/', include(post_create_patterns)),
    path('<int:pk>/', include([
        # path('', include(post_edit_patterns)),
        path('', PostDetailView.as_view(), name='post_detail'),
        path('', include(post_edit_patterns)),
        # path('edit', PostEditView.as_view(), name='post_edit'),
        # path('preview', PostPreviewView.as_view(), name='post_preview'),
        # path('done', PostDoneView.as_view(), name='post_done'),
        # path('ajax/', include([
        #     path('edit_load_data', PostEditContainerView.as_view(), name='post_edit_load_data'),
        #     path('preview_load_data', PostPreviewContainerView.as_view(), name='post_preview_load_data'),
        #     path('done_load_data', PostDoneContainerView.as_view(), name='post_done_load_data'),
        #     ])),
        ])),
    ]
