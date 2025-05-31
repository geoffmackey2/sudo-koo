from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ads.txt', views.ads_txt, name='ads_txt'),
]