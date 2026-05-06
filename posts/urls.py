from django.urls import path
from . import views

urlpatterns = [
    path('home_dashboard', views.dashboard, name='home_dashboard'),    
]