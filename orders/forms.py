from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=200, label='First Name')
    last_name = forms.CharField(max_length=200, label='Last Name')
    email = forms.EmailField(max_length=200)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)

class LoginForm(AuthenticationForm):
    pass