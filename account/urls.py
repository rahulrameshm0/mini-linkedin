
from django.urls import path
from . import views
urlpatterns = [
    path('', views.sign_in, name="signin"),
    path('signup', views.signup, name='signup'),
    path('dashboard', views.dashboard, name='dashboard')
]
