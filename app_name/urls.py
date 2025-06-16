from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', lambda request: redirect('login')),  # ⬅ redirects '/' to /login/
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('team_leader_dashboard/', views.team_leader_dashboard_view, name='team_leader_dashboard'),
    path('engineer_dashboard/', views.engineer_dashboard, name='engineer_dashboard'),
    path('team_summary/', views.team_summary_view, name='team_summary'),
    path('create_session/', views.create_session_view, name='create_session'),
]

