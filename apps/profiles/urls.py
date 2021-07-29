from django.urls import path, include
from django.views.generic import RedirectView

from django.contrib.auth import views as auth_views

from .views import *


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
    path('', ProfileTabView.as_view(), name='profile_tab'),
    path('ajax/', include([
        path('profile_tab_load_data', ProfileTabLoadDataListView.as_view(), name='profile_tab_load_data')
        ])),
    ]

settings_patterns = [
    path('', SettingsView.as_view(), name='profile_settings'),
    path('ajax/', include([
        path('edit_profile', EditProfileView.as_view(), name='edit_profile'),
        path('edit_acccccvatar_profile', EditAvatarView.as_view(), name='edit_avatar_profile'),
        path('edit_feed_settings_profile', EditFeedSettingsView.as_view(), name='edit_feed_settings_profile'),
        path('search_tags', FeedSearchTagsView.as_view(), name='profile_search_tags'),
        path('load_excluded_feed_tags', FeedLoadExcludedTagsView.as_view(), name='profile_load_excluded_feed_tags'),
        path('delete_excluded_feed_tag', FeedDeleteExcludedTagView.as_view(), name='profile_delete_excluded_feed_tag'),
        path('edit_password_change', PasswordChangeView.as_view(), name='profile_password_change'),
        path('password_change_done', PasswordChangeDoneView.as_view(), name='profile_password_change_done'),
        ]))
    ]

urlpatterns = [
    # authentication and registration
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', auth_views.LoginView.as_view(template_name='reg/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('password_reset/', include(password_reset_patterns)),

    # profile
    path('<str:username>/', include([
        path('', ProfileView.as_view(), name='profile'),
        path('settings/', include(settings_patterns)),
        path('<str:tab>/', include(tabs_patterns)),
        ])),
    ]
