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

class Addressform(forms.Form):
    name = forms.CharField(max_length=200, label='Name')
    addressline = forms.CharField(widget=forms.Textarea, label="Address")
    city = forms.CharField(max_length=200, label="City")
    state = forms.CharField(max_length=200, label="State")
    country = forms.CharField(max_length=200, label="Country")
    pin = forms.IntegerField(label="Pin-Code", max_value=999999, min_value=100000)
    phone = forms.IntegerField(max_value=9999999999, min_value=1000000000, label="Phone Number")