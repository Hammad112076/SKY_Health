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
    path('engineer_dashboard/', views.engineer_dashboard_view, name='engineer_dashboard'),
    path('vote/', views.vote_view, name='vote'),
    path('summary/', views.summary_view, name='summary'),
    path('create_session/', views.create_session_view, name='create_session'),
]

