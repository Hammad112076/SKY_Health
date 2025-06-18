# Import Django form utilities and built-in user form/model
from django import forms
from django.forms.widgets import DateTimeInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Import your custom models
from .models import Profile, Session, Vote, Team


# -----------------------------
# Register Form
# -----------------------------
class RegisterForm(UserCreationForm):
    """
    Extends Django's built-in UserCreationForm to include:
    - Email
    - User Role (Engineer or Team Leader)
    - Team selection
    """

    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, required=True)
    team = forms.ModelChoiceField(
        queryset=Team.objects.all(),  # Drop-down populated with available teams
        required=True,
        label="Team"
    )

    class Meta:
        model = User  # Using Django's default User model
        fields = ['username', 'email', 'password1', 'password2', 'role', 'team']


# -----------------------------
# Session Creation Form
# -----------------------------
class SessionForm(forms.ModelForm):
    """
    Used by Team Leaders to create new voting sessions.
    Includes:
    - Name of session
    - Start time and end time with datetime-local input widgets
    """

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
    """
    A custom form built dynamically at runtime.

    Accepts a 'cards' keyword argument, where each card becomes a separate
    radio button field on the form for voting.
    Each field uses the card ID as a key (e.g., 'card_3').

    Voting is optional, so all fields are not required.
    """

    def __init__(self, *args, **kwargs):
        cards = kwargs.pop('cards', [])  # Cards passed into the form
        super().__init__(*args, **kwargs)

        for card in cards:
            self.fields[f'card_{card.id}'] = forms.ChoiceField(
                label=card.title,  # Display card title as the field label
                choices=Vote.COLOR_CHOICES,  # Options: red, amber, green
                widget=forms.RadioSelect,  # Render as radio buttons
                required=False  # Voting is not mandatory for each card
            )
