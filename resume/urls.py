from django.urls import path
from . import views

urlpatterns = [
    path('resumes/', views.resume_list_create, name='resume-list-create'),
    path('resumes/<int:pk>/', views.resume_detail, name='resume-detail'),
    path('resumes/<int:resume_id>/preview/', views.preview_resume, name='preview-resume'),
]
