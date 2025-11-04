from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'user_type', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('.edu.br'):
            raise forms.ValidationError("Use um e-mail institucional que termine com '.edu.br'.")
        return email
