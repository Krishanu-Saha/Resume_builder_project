# interestapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("resumes/<int:resume_id>/interests/", views.interest_list_create, name="interest-list-create"),
    path("resumes/<int:resume_id>/interests/<int:pk>/", views.interest_detail, name="interest-detail"),
]
