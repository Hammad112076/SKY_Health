# Import Django's base model class and built-in User model for relationships
from django.db import models
from django.contrib.auth.models import User


# -----------------------------
# Team Model
# -----------------------------
class Team(models.Model):
    """
    Represents a development or functional team in the organization.
    Each team has a unique name.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        # Used for readable representation in the admin panel and elsewhere
        return self.name


# -----------------------------
# Profile Model (User Extension)
# -----------------------------
class Profile(models.Model):
    """
    Extends Django's User model to include a role (engineer or team leader) and team association.
    Each user has exactly one profile.
    """
    ROLE_CHOICES = [
        ('team_leader', 'Team Leader'),
        ('engineer', 'Engineer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to Django User
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)  # Role of the user
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)  # User’s team

    def __str__(self):
        # Displays the username and role in readable format
        return f"{self.user.username} ({self.role})"


# -----------------------------
# HealthCard Model (Voting Questions)
# -----------------------------
class HealthCard(models.Model):
    """
    Represents a category or question that engineers vote on (e.g., "Teamwork", "Code Quality").
    """
    title = models.CharField(max_length=100)  # Title of the card/question
    description = models.TextField()  # Optional description for more context
    icon_class = models.CharField(max_length=100, default='fas fa-circle')  # For rendering icons (e.g., Font Awesome)

    def __str__(self):
        # Used in admin and UI for readable display
        return self.title


# -----------------------------
# Session Model (Voting Sessions)
# -----------------------------
class Session(models.Model):
    """
    Represents a specific voting session initiated by a Team Leader.
    Active sessions are open for voting within the start and end time.
    """
    name = models.CharField(max_length=100)  # Name/label of the session
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Who created the session
    start_time = models.DateTimeField()  # When voting starts
    end_time = models.DateTimeField()  # When voting ends
    is_active = models.BooleanField(default=False)  # Manual toggle to activate/deactivate session

    def __str__(self):
        return self.name

    def is_current(self):
        """
        Determines whether the session is currently live (time-based + active flag).
        """
        from django.utils.timezone import now
        return self.is_active and self.start_time <= now() <= self.end_time


# -----------------------------
# Vote Model
# -----------------------------
class Vote(models.Model):
    """
    Represents a user's vote on a specific HealthCard during a Session.
    Each vote includes a color (Red, Amber, Green) and optional comment.
    """
    COLOR_CHOICES = [
        ('red', 'Red'),
        ('amber', 'Amber'),  # Corrected spelling for consistency
        ('green', 'Green'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Who voted
    session = models.ForeignKey(Session, on_delete=models.CASCADE)  # The session in which the vote was cast
    card = models.ForeignKey(HealthCard, on_delete=models.CASCADE)  # The card/question being voted on
    color = models.CharField(
        max_length=10,
        choices=COLOR_CHOICES,
        blank=True,
        null=True
    )  # The vote (RAG color)
    comment = models.TextField(blank=True, null=True)  # Optional feedback/comment

    class Meta:
        unique_together = ('user', 'session', 'card')  # Ensures each user votes only once per card per session

    def __str__(self):
        # Display vote summary in readable format
        return f"{self.user.username} - {self.card.title} ({self.color})"
