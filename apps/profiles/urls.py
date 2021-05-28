from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView

import apps.profiles.views as views

urlpatterns = [
    # authentication and registration
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),

    # profile
    path('<str:username>/', views.ProfileView.as_view(), name='profile'),
    path('<str:username>/tabs/<str:tab>/', views.ProfileTabView.as_view(), name='profile_tab'),
    path('<str:username>/settings/', views.ProfileSettingsView.as_view(), name='profile_settings'),

    # ajax profile
    path('<str:username>/ajax/tabs/profile_tab_data_load',
         views.ProfileTabDataLoadListView.as_view(), name='profile_tab_data_load'),
    path('<str:username>/ajax/settings/load_profile_avatar', views.ProfileAvatarView.as_view(), name='profile_avatar'),
    path('<str:username>/ajax/settings/load_profile_feed', views.ProfileFeedView.as_view(), name='profile_feed'),
]