from django.urls import path

from django.contrib.auth import views as auth_views

import apps.profiles.views as views

urlpatterns = [
    # authentication and registration
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),

    # profile
    path('<str:username>/', views.ProfileView.as_view(), name='profile'),

    # tabs
    path('<str:username>/tabs/<str:tab>/', views.ProfileTabView.as_view(), name='profile_tab'),
    path('<str:username>/tabs/ajax/profile_tab_load_data',
         views.ProfileTabLoadDataListView.as_view(), name='profile_tab_load_data'),

    # settings
    path('<str:username>/settings/',
         views.SettingsView.as_view(), name='profile_settings'),

    path('<str:username>/settings/ajax/edit_profile',
         views.EditProfileView.as_view(), name='edit_profile'),
    path('<str:username>/settings/ajax/edit_avatar_profile',
         views.EditAvatarView.as_view(), name='edit_avatar_profile'),

    path('<str:username>/settings/ajax/edit_feed_settings_profile',
         views.EditFeedSettingsView.as_view(), name='edit_feed_settings_profile'),
    path('<str:username>/settings/ajax/search_tags',
         views.FeedSearchTags.as_view(), name='profile_search_tags'),
    path('<str:username>/settings/ajax/Load_excluded_feed_tags',
         views.FeedLoadExcludedTags.as_view(), name='profile_load_excluded_feed_tags'),
    path('<str:username>/settings/ajax/delete_excluded_feed_tag',
         views.FeedDeleteExcludedTag.as_view(), name='profile_delete_excluded_feed_tag'),

    path('<str:username>/settings/ajax/edit_password_change',
         views.PasswordChangeView.as_view(), name='profile_password_change'),
    path('<str:username>/settings/ajax/password_change_done',
         views.PasswordChangeDoneView.as_view(), name='profile_password_change_done'),
    ]