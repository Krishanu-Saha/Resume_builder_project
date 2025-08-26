from django.urls import path
from . import views

urlpatterns = [
    path('templates/', views.template_list, name='template-list'),
]
