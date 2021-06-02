from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView

import apps.profiles.views as views

urlpatterns = [
    # authentication and registration
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),

    # profile
    path('<str:username>/', views.ProfileView.as_view(), name='profile'),

    # tabs
    path('<str:username>/tabs/<str:tab>/', views.TabProfileView.as_view(), name='profile_tab'),
    path('<str:username>/tabs/ajax/profile_tab_data_load',
         views.ProfileTabDataLoadListView.as_view(), name='profile_tab_data_load'),

    # settings
    path('<str:username>/settings/',
         views.EditProfileView.as_view(), name='profile_edit'),
    path('<str:username>/settings/ajax/load_profile_avatar',
         views.EditAvatarProfileView.as_view(), name='profile_edit_avatar'),
    path('<str:username>/settings/ajax/load_edit_feed_settings',
         views.FeedSettingsProfileView.as_view(), name='profile_edit_feed_settings'),
    path('<str:username>/settings/ajax/search_tags',
         views.FeedSearchTags.as_view(), name='profile_search_tags'),
    path('<str:username>/settings/ajax/Load_excluded_feed_tags',
         views.FeedLoadExcludedTags.as_view(), name='profile_load_excluded_feed_tags'),
    path('<str:username>/settings/ajax/delete_excluded_feed_tag',
         views.FeedDeleteExcludedTag.as_view(), name='profile_delete_excluded_feed_tag')
]