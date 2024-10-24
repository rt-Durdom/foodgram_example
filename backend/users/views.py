from django.shortcuts import render
from .models import Profile


class ProfileViewSet:
    queryset = Profile.objects.all()
