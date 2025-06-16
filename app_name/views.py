from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, HealthCard, Session, Vote, Team
from .forms import RegisterForm, SessionForm, VoteForm
from .forms import SessionForm
from collections import defaultdict


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
def team_summary_view(request):
    user = request.user

    if user.profile.role != 'team_leader':
        return redirect('dashboard')  # Only team leaders allowed

    team = user.profile.team  # The team the leader manages

    sessions = Session.objects.filter(created_by=user).order_by('-start_time')
    selected_session = None
    session_id = request.GET.get('session')

    if session_id:
        try:
            selected_session = sessions.get(id=session_id)
        except Session.DoesNotExist:
            selected_session = None

    # Placeholder structure — you can replace this with actual vote calculation
    from collections import defaultdict
    team_stats = defaultdict(lambda: {
        'name': '',
        'vote_counts': {'green': 0, 'amber': 0, 'red': 0, 'pending': 0},
        'comments': [],
        'icon': 'fas fa-chart-pie'
    })

    if selected_session:
        cards = HealthCard.objects.all()
        for card in cards:
            votes = Vote.objects.filter(session=selected_session, card=card)
            vote_counts = {'green': 0, 'amber': 0, 'red': 0, 'pending': 0}
            comments = []

            for vote in votes:
                vote_counts[vote.color] += 1
                if vote.comment:
                    comments.append({'vote': vote.color, 'comment': vote.comment})

            team_stats[card.id] = {
                'name': card.title,
                'vote_counts': vote_counts,
                'comments': comments,
                'icon': card.icon_class if hasattr(card, 'icon_class') else 'fas fa-circle'
            }

    context = {
        'selected_team': team,
        'sessions': sessions,
        'selected_session': selected_session,
        'team_stats': dict(team_stats)
    }

    return render(request, 'health/team_summary.html', context)


@login_required
def dashboard_view(request):
    profile = request.user.profile

    if profile.role == 'team_leader':
        return redirect('team_leader_dashboard')
    elif profile.role == 'engineer':
        return redirect('engineer_dashboard')
    else:
        messages.error(request, 'Unknown role.')
        return redirect('logout')

@login_required
def team_leader_dashboard_view(request):
    user = request.user
    profile = user.profile

    if profile.role != 'team_leader':
        return redirect('dashboard')

    team = profile.team
    sessions = Session.objects.filter(created_by=user).order_by('-start_time')
    selected_session = sessions.first()

    team_stats = defaultdict(lambda: {
        'name': '',
        'vote_counts': {'green': 0, 'amber': 0, 'red': 0, 'pending': 0},
        'comments': [],
        'icon': 'fas fa-chart-pie'
    })

    if selected_session:
        cards = HealthCard.objects.all()
        for card in cards:
            votes = Vote.objects.filter(session=selected_session, card=card)
            vote_counts = {'green': 0, 'amber': 0, 'red': 0, 'pending': 0}
            comments = []

            for vote in votes:
                vote_counts[vote.color] += 1
                if vote.comment:
                    comments.append({'vote': vote.color, 'comment': vote.comment})

            team_stats[card.id] = {
                'name': card.title,
                'vote_counts': vote_counts,
                'comments': comments,
                'icon': getattr(card, 'icon_class', 'fas fa-circle')
            }

    # Totals for the chart/sidebar
    total_red = sum(stat['vote_counts'].get('red', 0) for stat in team_stats.values())
    total_amber = sum(stat['vote_counts'].get('amber', 0) for stat in team_stats.values())
    total_green = sum(stat['vote_counts'].get('green', 0) for stat in team_stats.values())
    total_votes = total_red + total_amber + total_green

    context = {
        'selected_team': team,
        'selected_session': selected_session,
        'sessions': sessions,
        'team_stats': dict(team_stats),
        'total_red': total_red,
        'total_amber': total_amber,
        'total_green': total_green,
        'total_votes': total_votes,
    }

    return render(request, 'health/team_leader_dashboard.html', context)


@login_required
def engineer_dashboard(request):
    profile = request.user.profile
    team = profile.team
    selected_session = Session.objects.filter(is_active=True).last()
    cards = HealthCard.objects.all()
    user_votes = []
    existing_votes = {}

    if selected_session and selected_session.is_current():
        user_votes = Vote.objects.filter(user=request.user, session=selected_session)
        existing_votes = {vote.card.id: vote.color for vote in user_votes}

    if request.method == 'POST':
        form = VoteForm(cards, request.POST)
        if form.is_valid():
            for card in cards:
                field_name = f'card_{card.id}'
                color = form.cleaned_data.get(field_name)

                # Save or update the vote
                Vote.objects.update_or_create(
                    user=request.user,
                    session=selected_session,
                    card=card,
                    defaults={'color': color}
                )
            messages.success(request, 'All votes submitted successfully.')
            return redirect('engineer_dashboard')
    else:
        form = VoteForm(cards)

    context = {
        'selected_session': selected_session,
        'cards': cards,
        'user_votes': user_votes,
        'existing_votes': existing_votes,
        'vote_form': form
    }
    return render(request, 'health/engineer_dashboard.html', context)