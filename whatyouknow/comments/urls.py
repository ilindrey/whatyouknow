from django.urls import path

from .views import CommentList

urlpatterns = [
    path('ajax/comment_list', CommentList.as_view(), name='comment_list'),
]
