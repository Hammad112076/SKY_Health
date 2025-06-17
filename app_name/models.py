from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    ROLE_CHOICES = [
        ('team_leader', 'Team Leader'),
        ('engineer', 'Engineer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class HealthCard(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_class = models.CharField(max_length=100, default='fas fa-circle') 

    def __str__(self):
        return self.title  # ✅ Only keep this once (you had it twice)


class Session(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def is_current(self):
        from django.utils.timezone import now
        return self.is_active and self.start_time <= now() <= self.end_time


class Vote(models.Model):
    COLOR_CHOICES = [
        ('red', 'Red'),
        ('amber', 'Amber'),  # ✅ FIXED spelling: “Yello” ➝ “Amber”
        ('green', 'Green'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    card = models.ForeignKey(HealthCard, on_delete=models.CASCADE)
    color = models.CharField(
        max_length=10,
        choices=COLOR_CHOICES,
        blank=True,
        null=True
    )
    comment = models.TextField(blank=True, null=True)  # Optional feedback

    class Meta:
        unique_together = ('user', 'session', 'card')

    def __str__(self):
        return f"{self.user.username} - {self.card.title} ({self.color})"
