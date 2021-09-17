from django.urls import path, include

from .views import *


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

post_create_patterns = [
    path('', PostCreateView.as_view(), name='post_create'),
    path('ajax/', include([
        path('create_container', PostCreateContainerView.as_view(), name='post_create_container'),
        ]))
    ]

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('create/', include(post_create_patterns)),
    path('<int:pk>/', include([
        path('', PostDetailView.as_view(), name='post_detail'),
        path('', include(post_edit_patterns)),
        ])),
    ]
