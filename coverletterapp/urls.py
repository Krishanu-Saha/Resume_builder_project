from django.urls import path
from . import views

urlpatterns = [
    path("cover-letters/", views.cover_letter_list_create, name="cover_letter_list_create"),
    path("cover-letters/<int:pk>/", views.cover_letter_detail, name="cover_letter_detail"),
    path("cover-letters/<int:cover_letter_id>/preview/", views.preview_cover_letter, name="preview_cover_letter"),
]