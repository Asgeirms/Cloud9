from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Form for the user registration page
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    # Capitalizes the first name
    def clean_first_name(self):
        return self.cleaned_data['first_name'].capitalize()

    # Capitalizes the last name
    def clean_last_name(self):
        return self.cleaned_data['last_name'].capitalize()