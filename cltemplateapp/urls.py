from django.urls import path
from . import views

urlpatterns = [
    path("cover-letter-templates/", views.cover_letter_template_list_create, name="cover_letter_template_list_create"),
    path("cover-letter-templates/<int:pk>/", views.cover_letter_template_detail, name="cover_letter_template_detail"),
]
