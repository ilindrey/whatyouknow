from django.urls import path, include

from .views import PostListView, PostDetailView, PostCreateView, PostWriteView, PostPreviewView


post_create_patterns = [
    path('', PostCreateView.as_view(), name='post_create'),
    path('ajax/', include([
        path('write', PostWriteView.as_view(), name='post_write'),
        path('preview', PostPreviewView.as_view(), name='post_preview'),
        ]))
    ]

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('create/', include(post_create_patterns)),
]
