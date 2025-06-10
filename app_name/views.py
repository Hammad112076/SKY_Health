from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile, HealthCard, Session, Vote
from .forms import RegisterForm, SessionForm, VoteForm


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, role=form.cleaned_data['role'])
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'health/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']
        user = authenticate(username=username, password=password)
        if user and user.profile.role == role:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'health/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    profile = request.user.profile
    if profile.role == 'team_leader':
        return redirect('manage_sessions')
    return redirect('vote')


@login_required
def manage_sessions(request):
    if request.user.profile.role != 'team_leader':
        return redirect('dashboard')

    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.created_by = request.user
            session.save()
            return redirect('manage_sessions')
    else:
        form = SessionForm()

    sessions = Session.objects.filter(created_by=request.user)
    return render(request, 'health/manage_sessions.html', {'form': form, 'sessions': sessions})


@login_required
def vote_view(request):
    profile = request.user.profile
    if profile.role != 'engineer':
        return redirect('dashboard')

    session = Session.objects.filter(is_active=True).last()
    if not session:
        return render(request, 'health/no_active_session.html')

    cards = HealthCard.objects.all()
    if request.method == 'POST':
        form = VoteForm(cards, request.POST)
        if form.is_valid():
            for card in cards:
                color = form.cleaned_data[f'card_{card.id}']
                Vote.objects.update_or_create(
                    user=request.user,
                    session=session,
                    card=card,
                    defaults={'color': color}
                )
            return redirect('summary')
    else:
        form = VoteForm(cards)

    return render(request, 'health/vote.html', {'form': form, 'session': session})


@login_required
def summary_view(request):
    votes = Vote.objects.filter(user=request.user)
    return render(request, 'health/summary.html', {'votes': votes})

# === urls.py (inside health/urls.py) ===
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('vote/', views.vote_view, name='vote'),
    path('summary/', views.summary_view, name='summary'),
    path('manage_sessions/', views.manage_sessions, name='manage_sessions'),
]