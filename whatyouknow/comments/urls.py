from django.urls import path

from .views import ParentCommentList, DescendantCommentList

urlpatterns = [
    path('ajax/parent_comment_list', ParentCommentList.as_view(), name='parent_comment_list'),
    path('ajax/descendant_comment_list', DescendantCommentList.as_view(), name='descendant_comment_list'),
]
