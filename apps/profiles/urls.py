from django.urls import path, include

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

second_tabs_patterns = [
    path('', ProfileSecondTabView.as_view(), name='profile_second_tab'),
    path('ajax/', include([
        path('posts_all_tab_base_load_data', ProfilePostsAllTabBaseLoadDataListView.as_view(),
             name='posts_all_tab_base_load_data'),
        path('posts_all_tab_lazy_load_data', ProfilePostsAllTabLazyLoadDataListView.as_view(),
             name='posts_all_tab_lazy_load_data'),
        path('posts_drafts_tab_base_load_data', ProfilePostsDraftsTabBaseLoadDataListView.as_view(),
             name='posts_drafts_tab_base_load_data'),
        path('posts_drafts_tab_lazy_load_data', ProfilePostsDraftsTabLazyLoadDataListView.as_view(),
             name='posts_drafts_tab_lazy_load_data'),
        path('posts_rejected_tab_base_load_data', ProfilePostsRejectedTabBaseLoadDataListView.as_view(),
             name='posts_rejected_tab_base_load_data'),
        path('posts_rejected_tab_lazy_load_data', ProfilePostsRejectedTabLazyLoadDataListView.as_view(),
             name='posts_rejected_tab_lazy_load_data'),
        ]))
    ]

first_tabs_patterns = [
    path('', ProfileFirstTabView.as_view(), name='profile_tab'),
    path('<str:second_tab>/', include(second_tabs_patterns)),
    path('ajax/', include([
        # path('posts_tab_load_data', ProfilePostsTabLoadDataView.as_view(), name='posts_tab_load_data'),
        path('comments_tab_load_data', ProfileCommentsTabLoadDataListView.as_view(), name='comments_tab_load_data'),
        ])),
    ]

settings_patterns = [
    path('', SettingsView.as_view(), name='profile_settings'),
    path('<str:tab>/', SettingsView.as_view(), name='profile_settings_tab'),
    path('ajax/', include([
        path('edit_profile', EditProfileView.as_view(), name='edit_profile'),
        path('edit_feed', EditFeedView.as_view(), name='edit_feed'),
        path('password_change', PasswordChangeView.as_view(), name='password_change'),
        path('load_password_change_done', PasswordChangeDoneView.as_view(), name='password_change_done'),
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
        path('', ProfileView.as_view(), name='profile_detail'),
        path('settings/', include(settings_patterns)),
        path('<str:first_tab>/', include(first_tabs_patterns)),
        ])),
    ]
