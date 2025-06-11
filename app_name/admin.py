from django.contrib import admin
from .models import Team, Profile, HealthCard, Session, Vote

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role', 'team')
    list_filter = ('role', 'team')
    search_fields = ('user__username',)


@admin.register(HealthCard)
class HealthCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_by', 'start_time', 'end_time', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'created_by__username')


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session', 'card', 'color')
    list_filter = ('color', 'session')
    search_fields = ('user__username', 'card__title', 'session__name')
