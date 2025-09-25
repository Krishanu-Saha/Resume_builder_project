# personal_details/urls.py
from django.urls import path
from resume_builder import settings
from . import views
from django.conf.urls.static import static


urlpatterns = [
    path(
        'resumes/<int:resume_id>/personal_details/',
        views.personal_details_manage,
        name='resume-personal-details-crud'
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
