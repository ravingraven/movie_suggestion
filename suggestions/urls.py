from django.urls import path
from . import views

urlpatterns = [
                path('', views.index, name='index'),
                path('set_preference/', views.set_preference, name='set_preference'),
                path('set_suggestions/', views.set_suggestions, name='set_suggestions'),
                path('get_preference/', views.get_preference, name='get_preference'),
                path('get_preferences/', views.get_preferences, name='get_preferences'),
                path('get_video_details/', views.get_video_details, name='get_video_details'),
              ]
