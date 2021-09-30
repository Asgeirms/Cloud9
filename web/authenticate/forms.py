from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from .validators import validate_is_name

# Form for the user registration page
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(label='First Name', validators=[validate_is_name])
    last_name = forms.CharField(label='Last Name', validators=[validate_is_name])
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        help_texts = {
            'username': None
        }

    def clean_first_name(self):
        """Capitalizes the first name"""
        return self.cleaned_data['first_name'].capitalize()

    def clean_last_name(self):
        """Capitalizes the last name"""
        return self.cleaned_data['last_name'].capitalize()
