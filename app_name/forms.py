from django import forms
from django.forms.widgets import DateTimeInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Session, Vote, Team

# -----------------------------
# Register Form
# -----------------------------
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, required=True)
    team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        required=True,
        label="Team"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role', 'team']


# -----------------------------
# Session Creation Form
# -----------------------------
class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['name', 'start_time', 'end_time']
        widgets = {
            'start_time': DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': DateTimeInput(attrs={'type': 'datetime-local'}),
        }


# -----------------------------
# Vote Form (Dynamic Fields Per Card)
# -----------------------------
class VoteForm(forms.Form):
    def __init__(self, *args, **kwargs):
        cards = kwargs.pop('cards', [])
        super().__init__(*args, **kwargs)

        for card in cards:
            self.fields[f'card_{card.id}'] = forms.ChoiceField(
                label=card.title,
                choices=Vote.COLOR_CHOICES,  # ['red', 'amber', 'green']
                widget=forms.RadioSelect,
                required=False  # Optional voting
            )
