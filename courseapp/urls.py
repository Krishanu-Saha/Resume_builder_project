from django.urls import path
from . import views

urlpatterns = [
    path('resumes/<int:resume_id>/courses/', views.course_list_create, name='course-list-create'),
    path('resumes/<int:resume_id>/courses/<int:pk>/', views.course_detail, name='course-detail'),
]
