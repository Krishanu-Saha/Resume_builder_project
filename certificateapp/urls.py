from django.urls import path
from . import views

urlpatterns = [
    path('resumes/<int:resume_id>/certificates/', views.certificate_list_create, name='certificate-list-create'),
    path('resumes/<int:resume_id>/certificates/<int:pk>/', views.certificate_detail, name='certificate-detail'),
]
