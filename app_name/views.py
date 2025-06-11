from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, HealthCard, Session, Vote
from .forms import RegisterForm, SessionForm, VoteForm

from .forms import SessionForm

@login_required
def create_session_view(request):
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.created_by = request.user
            session.save()
            return redirect('dashboard')  # Redirect after creating session
    else:
        form = SessionForm()

    return render(request, 'health/create_session.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            team = form.cleaned_data.get('team')

            # Create profile
            Profile.objects.create(user=user, role=role, team=team)

            return redirect('login')
    else:
        form = RegisterForm()
    
    return render(request, 'health/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')  # optional if role is removed from login form

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user_role = user.profile.role
            if user_role == 'team_leader':
                return redirect('team_leader_dashboard')  
            elif user_role == 'engineer':
                return redirect('vote')  
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'health/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
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
            messages.success(request, "Session created.")
            return redirect('manage_sessions')
    else:
        form = SessionForm()

    sessions = Session.objects.filter(created_by=request.user)
    return render(request, 'health/manage_sessions.html', {'form': form, 'sessions': sessions})


@login_required
def vote_view(request):
    if request.user.profile.role != 'engineer':
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
            messages.success(request, "Vote submitted.")
            return redirect('summary')
    else:
        form = VoteForm(cards)

    return render(request, 'health/vote.html', {'form': form, 'session': session})


@login_required
def summary_view(request):
    votes = Vote.objects.filter(user=request.user)
    return render(request, 'health/summary.html', {'votes': votes})
