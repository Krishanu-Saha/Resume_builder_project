from django.urls import path
from . import views

urlpatterns = [
    path("resumes/<int:resume_id>/projects/", views.project_list_create, name="project-list-create"),
    path("resumes/<int:resume_id>/projects/<int:pk>/", views.project_detail, name="project-detail"),
]
