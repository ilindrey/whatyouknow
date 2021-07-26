from django.urls import path, include

from .views import *


post_edit_patterns = [
    path('edit', PostEditView.as_view(), name='post_edit'),
    path('preview', PostPreviewView.as_view(), name='post_preview'),
    path('done', PostDoneView.as_view(), name='post_done'),
    ]

post_create_patterns = [
    path('', PostCreateView.as_view(), name='post_create'),
    path('ajax/', include([
        path('write', PostWriteView.as_view(), name='post_write'),
        # path('<int:pk>', include(post_edit_patterns))
        ]))
    ]

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('create/', include(post_create_patterns)),
    path('<int:pk>/', include([
        path('', PostDetailView.as_view(), name='post_detail'),
        path('', include(post_edit_patterns))
        ])),
    ]
