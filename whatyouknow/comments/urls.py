from django.urls import path

from .views import *

urlpatterns = [
    path('ajax/comments_parents_list', CommentParentsList.as_view(), name='comment_parents_list'),
    path('ajax/comments_children_list', CommentChildrenList.as_view(), name='comment_children_list'),
]
