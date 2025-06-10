from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', lambda request: redirect('login')),  # ⬅ redirects '/' to /login/
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('vote/', views.vote_view, name='vote'),
    path('summary/', views.summary_view, name='summary'),
    path('manage_sessions/', views.manage_sessions, name='manage_sessions'),
]

