from django.urls import path

from django.contrib.auth import views as auth_views

import apps.profiles.views as views

urlpatterns = [
    # authentication and registration
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('login/', auth_views.LoginView.as_view(
        template_name='reg/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='index'), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='reg/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='reg/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='reg/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='reg/password_reset_complete.html'), name="password_reset_complete"),

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
    path('<str:username>/settings/ajax/load_excluded_feed_tags',
         views.FeedLoadExcludedTags.as_view(), name='profile_load_excluded_feed_tags'),
    path('<str:username>/settings/ajax/delete_excluded_feed_tag',
         views.FeedDeleteExcludedTag.as_view(), name='profile_delete_excluded_feed_tag'),

    path('<str:username>/settings/ajax/edit_password_change',
         views.PasswordChangeView.as_view(), name='profile_password_change'),
    path('<str:username>/settings/ajax/password_change_done',
         views.PasswordChangeDoneView.as_view(), name='profile_password_change_done'),
    ]
