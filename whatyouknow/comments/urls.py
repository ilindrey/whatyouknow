from django.urls import path

from .views import comment_children

urlpatterns = [
    # path('ajax/children/<int:parent_id>', comment_children, name='comment_children'),
    path('ajax/children', comment_children, name='comment_children'),
]
