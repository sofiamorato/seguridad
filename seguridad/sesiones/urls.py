# sesiones/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('create-session/', views.create_session, name='create_session'),
    path('check-sessions/', views.check_sessions, name='check_sessions'),
]
