from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('register_done/', views.register, name='register_done'),
    path('edit/', views.edit, name='edit'),
    path('profile/<int:profile_id>/', views.profile, name='profile'),
    path('profile/<int:profile_id>/reviews', views.profile_reviews, name='profile_reviews'),
]
