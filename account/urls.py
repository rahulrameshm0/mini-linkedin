from django.urls import path
from . import views
from posts.views import dashboard  

urlpatterns = [
    path('', views.sign_in, name="signin"),
    path('signup', views.signup, name='signup'),
    path('dashboard', dashboard, name='dashboard'),
    path('logout', views.log_out, name='logout'),
]
