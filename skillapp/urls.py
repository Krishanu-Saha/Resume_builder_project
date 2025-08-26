from django.urls import path
from . import views

urlpatterns = [
    path('resumes/<int:resume_id>/skills/', views.skill_list_create, name='skill-list-create'),
    path('resumes/<int:resume_id>/skills/<int:pk>/', views.skill_detail, name='skill-detail'),
]
