# Importing Django's admin module and models to be registered for the admin interface
from django.contrib import admin
from .models import Team, Profile, HealthCard, Session, Vote

# Registering the Team model with custom configuration for the admin interface
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    # Fields to display in the list view of the admin
    list_display = ('id', 'name')
    # Enables search by team name
    search_fields = ('name',)

# Registering the Profile model (which extends the default User model) for admin view
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # Fields to show in admin list view
    list_display = ('id', 'user', 'role', 'team')
    # Adds filtering options by role and team
    list_filter = ('role', 'team')
    # Allows searching by username or team name
    search_fields = ('user__username', 'team__name')

# Registering the HealthCard model that contains voting questions/topics
@admin.register(HealthCard)
class HealthCardAdmin(admin.ModelAdmin):
    # Displays card ID and title in list view
    list_display = ('id', 'title')
    # Enables search by title
    search_fields = ('title',)

# Registering the Session model which represents a voting session
@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    # Display these fields in the session list
    list_display = ('id', 'name', 'created_by', 'start_time', 'end_time', 'is_active')
    # Filters by active status and start time
    list_filter = ('is_active', 'start_time')
    # Enables searching by session name and creator's username
    search_fields = ('name', 'created_by__username')

# Registering the Vote model which stores each vote cast by a user
@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    # Shows vote ID, user who voted, session, card voted on, and selected color
    list_display = ('id', 'user', 'session', 'card', 'color')
    # Enables filtering by vote color, session, and card
    list_filter = ('color', 'session', 'card')
    # Allows searching votes by username, card title, and session name
    search_fields = ('user__username', 'card__title', 'session__name')
