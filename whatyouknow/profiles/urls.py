from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView

from .views import ProfileView, ProfileTabView, ProfileTabDataLoadList
# , ProfileTabPostList, ProfileTabCommentList

urlpatterns = [
    # profile
    path('<str:username>/', ProfileView.as_view(), name='profile'),
    path('<str:username>/<str:tab>/', ProfileTabView.as_view(), name='profile_tab'),

    # ajax profile
    path('<str:username>/ajax/profile_tab_data_load', ProfileTabDataLoadList.as_view(), name='profile_tab_data_load'),

    # authentication and registration
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),

]