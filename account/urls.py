from django.urls import path
from . import views
from posts.views import dashboard
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('dashboard', dashboard),
    path('signin/', views.sign_in, name='signin'),
    path('signup', views.signup, name='signup'),
    path('logout', views.log_out, name='logout'),
    path('network/', views.network, name='network'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/follow/', views.follow, name='follow'),
]
