# personal_details/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path(
        'resumes/<int:resume_id>/personal_details/',
        views.personal_details_crud,
        name='resume-personal-details-crud'
    ),
]
