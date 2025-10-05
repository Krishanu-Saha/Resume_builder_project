# profileapp/urls.py
from django.urls import path
from .views import ProfileMeView

urlpatterns = [
    path("profile/", ProfileMeView.as_view(), name="profile-me"),
]
