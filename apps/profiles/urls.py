from django.urls import path, include

from django.contrib.auth import views as auth_views

import apps.profiles.views as views


password_reset_patterns = [
    path('',
         auth_views.PasswordResetView.as_view(template_name='reg/password_reset.html'),
         name='password_reset'),
    path('done/',
         auth_views.PasswordResetDoneView.as_view(template_name='reg/password_reset_done.html'),
         name='password_reset_done'),
    path('confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='reg/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='reg/password_reset_complete.html'),
         name="password_reset_complete"),
    ]

tabs_patterns = [
    path('<str:tab>/', views.ProfileTabView.as_view(), name='profile_tab'),
    path('ajax/', include([
        path('profile_tab_load_data', views.ProfileTabLoadDataListView.as_view(), name='profile_tab_load_data')
        ])),
    ]

settings_patterns = [
    path('', views.SettingsView.as_view(), name='profile_settings'),
    path('ajax/', include([
        path('edit_profile', views.EditProfileView.as_view(), name='edit_profile'),
        path('edit_avatar_profile', views.EditAvatarView.as_view(), name='edit_avatar_profile'),
        path('edit_feed_settings_profile', views.EditFeedSettingsView.as_view(), name='edit_feed_settings_profile'),
        path('search_tags', views.FeedSearchTags.as_view(), name='profile_search_tags'),
        path('load_excluded_feed_tags', views.FeedLoadExcludedTags.as_view(), name='profile_load_excluded_feed_tags'),
        path('delete_excluded_feed_tag', views.FeedDeleteExcludedTag.as_view(), name='profile_delete_excluded_feed_tag'),
        path('edit_password_change', views.PasswordChangeView.as_view(), name='profile_password_change'),
        path('password_change_done', views.PasswordChangeDoneView.as_view(), name='profile_password_change_done'),
        ]))
    ]

urlpatterns = [
    # authentication and registration
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('login/', auth_views.LoginView.as_view(template_name='reg/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('password_reset/', include(password_reset_patterns)),

    # profile
    path('<str:username>/', include([
        path('', views.ProfileView.as_view(), name='profile'),
        path('tabs/', include(tabs_patterns)),
        path('settings/', include(settings_patterns)),
        ])),
    ]
