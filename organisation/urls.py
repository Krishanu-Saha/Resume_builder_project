from django.urls import path
from . import views

urlpatterns = [
    path('resumes/<int:resume_id>/organisations/', views.organisation_list_create, name='organisation-list-create'),
    path('resumes/<int:resume_id>/organisations/<int:pk>/', views.organisation_detail, name='organisation-detail'),
]
