from django.urls import path
from . import views

urlpatterns = [
    path('resumes/<int:resume_id>/educations/', views.education_list_create, name='education-list-create'),
    path('resumes/<int:resume_id>/educations/<int:pk>/', views.education_detail, name='education-detail'),
]
