# Import Django utilities for defining URLs and redirecting views
from django.urls import path
from django.shortcuts import redirect
from . import views  # Import views from the current app

# -----------------------------
# URL Patterns
# -----------------------------
urlpatterns = [
    # Redirects the root URL ('/') to the login page
    path('', lambda request: redirect('login')),

    # Route for user registration form
    path('register/', views.register_view, name='register'),

    # Route for user login form
    path('login/', views.login_view, name='login'),

    # Route for user logout (clears session and redirects)
    path('logout/', views.logout_view, name='logout'),

    # Generic dashboard route (shared or conditional redirect)
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # ❗Duplicate route — safe to remove one of them
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Team Leader’s custom dashboard view
    path('team_leader_dashboard/', views.team_leader_dashboard_view, name='team_leader_dashboard'),

    # Engineer’s voting dashboard
    path('engineer_dashboard/', views.engineer_dashboard, name='engineer_dashboard'),

    # Route to view the summary of a team (accessible by team leader)
    path('team_summary/', views.team_summary_view, name='team_summary'),

    # Route to create a new voting session (accessible by team leader)
    path('create_session/', views.create_session_view, name='create_session'),
]
