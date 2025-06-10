from django import forms
from django.forms.widgets import DateTimeInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Session, Vote

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['name', 'start_time', 'end_time', 'is_active']
        widgets = {
            'start_time': DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
class VoteForm(forms.Form):
    def __init__(self, cards, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for card in cards:
            self.fields[f'card_{card.id}'] = forms.ChoiceField(
                label=card.title,
                choices=Vote.COLOR_CHOICES,
                widget=forms.RadioSelect,
                required=True
            )