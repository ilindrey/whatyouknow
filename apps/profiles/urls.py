from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView

from .views import ProfileView, ProfileAvatarView, ProfileSettingsView, ProfileTabView, ProfileTabDataLoadList

urlpatterns = [
    # authentication and registration
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),

    # profile
    path('<str:username>/', ProfileView.as_view(), name='profile'),
    path('<str:username>/tabs/<str:tab>/', ProfileTabView.as_view(), name='profile_tab'),
    path('<str:username>/settings/', ProfileSettingsView.as_view(), name='profile_settings'),

    # ajax profile
    path('<str:username>/ajax/profile_tab_data_load', ProfileTabDataLoadList.as_view(), name='profile_tab_data_load'),
    path('<str:username>/ajax/profile_avatar', ProfileAvatarView.as_view(), name='profile_avatar'),
]