from django.urls import path, include

from .views import CommentListView, CreateCommentView, EditCommentView

urlpatterns = [
    path('ajax/', include([
        path('load_comment_list', CommentListView.as_view(), name='comment_list'),
        path('create_comment', CreateCommentView.as_view(), name='comment_create'),
        path('<int:pk>/', include([
            path('edit_comment', EditCommentView.as_view(), name='comment_edit')
            ])),
        ])),
]
