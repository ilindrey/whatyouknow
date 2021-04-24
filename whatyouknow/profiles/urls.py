from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView

from .views import ProfileView

urlpatterns = [
    # profile
    path('<str:username>', ProfileView.as_view(), name='profile'),

    # authentication and registration
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
]