from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from collections import defaultdict

from .models import Profile, HealthCard, Session, Vote, Team
from .forms import RegisterForm, SessionForm, VoteForm

@login_required
def create_session_view(request):
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.created_by = request.user
            session.save()
            return redirect('dashboard')
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
            Profile.objects.create(user=user, role=role, team=team)
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'health/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            role = user.profile.role
            if role == 'team_leader':
                return redirect('team_leader_dashboard')
            elif role == 'engineer':
                return redirect('engineer_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'health/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

@login_required
def dashboard_view(request):
    role = request.user.profile.role
    if role == 'team_leader':
        return redirect('team_leader_dashboard')
    elif role == 'engineer':
        return redirect('engineer_dashboard')
    messages.error(request, 'Unknown role.')
    return redirect('logout')

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
def team_leader_dashboard_view(request):
    user = request.user
    profile = user.profile

    if profile.role != 'team_leader':
        return redirect('dashboard')

    team = profile.team
    sessions = Session.objects.filter(created_by=user).order_by('-start_time')

    session_id = request.POST.get('session_id') or request.GET.get('session')
    selected_session = None
    if session_id:
        selected_session = sessions.filter(id=session_id).first()
    if not selected_session:
        selected_session = sessions.first()

    show_vote_cards = request.GET.get('vote') == '1'

    team_stats = defaultdict(lambda: {
        'name': '',
        'vote_counts': {'green': 0, 'amber': 0, 'red': 0},
        'comments': [],
        'icon': 'fas fa-chart-pie'
    })

    cards = HealthCard.objects.all()

    if request.method == 'POST' and selected_session and show_vote_cards:
        form = VoteForm(request.POST, cards=cards)
        if form.is_valid():
            for card in cards:
                field_name = f'card_{card.id}'
                color = form.cleaned_data.get(field_name)
                Vote.objects.update_or_create(
                    user=user,
                    session=selected_session,
                    card=card,
                    defaults={'color': color}
                )
            messages.success(request, 'Your votes have been submitted.')
            return redirect(f"{request.path}?session={selected_session.id}&vote=1")
    else:
        form = VoteForm(cards=cards)

    if selected_session and team:
        for card in cards:
            votes = Vote.objects.filter(
                session=selected_session,
                card=card,
                user__profile__team=team
            )
            vote_counts = {
                'green': votes.filter(color='green').count(),
                'amber': votes.filter(color='amber').count(),
                'red': votes.filter(color='red').count(),
            }
            team_stats[card.id] = {
                'name': card.title,
                'vote_counts': vote_counts,
                'icon': getattr(card, 'icon_class', 'fas fa-circle')
            }

    context = {
        'selected_team': team,
        'sessions': sessions,
        'selected_session': selected_session,
        'cards': cards,
        'vote_form': form,
        'show_vote_cards': show_vote_cards,
        'team_stats': dict(team_stats),
        'total_green': sum(s['vote_counts']['green'] for s in team_stats.values()),
        'total_amber': sum(s['vote_counts']['amber'] for s in team_stats.values()),
        'total_red': sum(s['vote_counts']['red'] for s in team_stats.values()),
    }

    return render(request, 'health/team_leader_dashboard.html', context)

@login_required
def team_summary_view(request):
    user = request.user
    if user.profile.role != 'team_leader':
        return redirect('dashboard')

    team = user.profile.team
    sessions = Session.objects.filter(created_by=user).order_by('-start_time')
    selected_session = None
    session_id = request.GET.get('session')
    if session_id:
        try:
            selected_session = sessions.get(id=session_id)
        except Session.DoesNotExist:
            selected_session = None
    else:
        selected_session = sessions.first()

    team_stats = defaultdict(lambda: {
        'name': '',
        'vote_counts': {'green': 0, 'amber': 0, 'red': 0},
        'comments': [],
        'icon': 'fas fa-chart-pie',
        'color': 'secondary',
    })

    if selected_session:
        cards = HealthCard.objects.all()
        for card in cards:
            votes = Vote.objects.filter(
                session=selected_session,
                card=card,
                user__profile__team=team,
                user__profile__role='engineer'  # only engineer votes
            )

            vote_counts = {'green': 0, 'amber': 0, 'red': 0}
            comments = []

            for vote in votes:
                if vote.color in vote_counts:
                    vote_counts[vote.color] += 1
                if vote.comment:
                    comments.append({'vote': vote.color, 'comment': vote.comment})

            # Dominant color used for icon badge
            dominant_color = max(vote_counts, key=vote_counts.get) if sum(vote_counts.values()) > 0 else 'secondary'

            team_stats[card.id] = {
                'name': card.title,
                'vote_counts': vote_counts,
                'comments': comments,
                'icon': getattr(card, 'icon_class', 'fas fa-circle'),
                'color': dominant_color,
            }

    context = {
        'selected_team': team,
        'sessions': sessions,
        'selected_session': selected_session,
        'team_stats': dict(team_stats),
    }
    return render(request, 'health/team_summary.html', context)

@login_required
def engineer_dashboard(request):
    user = request.user

    if user.profile.role != 'engineer':
        return redirect('dashboard')

    team = user.profile.team

    sessions = Session.objects.filter(created_by__profile__team=team).order_by('-start_time')
    selected_session = sessions.first()

    show_vote_cards = request.GET.get('vote') == '1'
    cards = HealthCard.objects.all()
    existing_votes = {}

    if selected_session:
        existing_votes_queryset = Vote.objects.filter(session=selected_session, user=user)
        for vote in existing_votes_queryset:
            existing_votes[vote.card.id] = vote.color

    if request.method == 'POST' and selected_session and show_vote_cards:
        form = VoteForm(request.POST, cards=cards)
        if form.is_valid():
            for card in cards:
                color = form.cleaned_data.get(f'card_{card.id}')
                if color:
                    Vote.objects.update_or_create(
                        user=user,
                        session=selected_session,
                        card=card,
                        defaults={'color': color}
                    )
            messages.success(request, 'Votes submitted successfully.')
            return redirect('engineer_dashboard')
    else:
        form = VoteForm(cards=cards)

    context = {
        'user': user,
        'cards': cards,
        'sessions': sessions,
        'selected_session': selected_session,
        'show_vote_cards': show_vote_cards,
        'vote_form': form,
        'existing_votes': existing_votes,
    }

    return render(request, 'health/engineer_dashboard.html', context)
