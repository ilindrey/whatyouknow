from django.shortcuts import render
from django.views import generic

from .models import UserProfile


class ProfileView(generic.DetailView):
    slug_field = 'username'
    slug_url_kwarg = 'username'
    model = UserProfile
    template_name = 'profile/profile_detail.html'
