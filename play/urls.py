from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('puzzle_status/<str:job_id>/', views.puzzle_status, name='puzzle_status'),
]