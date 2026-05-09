from django.urls import path
from . import views

urlpatterns = [
    path('home_dashboard', views.dashboard, name='home_dashboard'),   
    path('edit/<int:id>/', views.edit, name='edit'),    
    path('delete/<int:id>/', views.remove_post, name='delete'),    
]