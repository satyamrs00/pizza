from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=200, label='First Name', required=True)
    last_name = forms.CharField(max_length=200, label='Last Name')
    email = forms.EmailField(max_length=200, label='Email')
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)
        
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label

class Addressform(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label
            visible.field.widget.attrs['required'] = 'required'

    name = forms.CharField(max_length=200, label='Name')
    addressline = forms.CharField(label="Address", widget=forms.Textarea)
    city = forms.CharField(max_length=200, label="City")
    state = forms.CharField(max_length=200, label="State")
    country = forms.CharField(max_length=200, label="Country")
    pin = forms.IntegerField(label="Pin-Code", max_value=9999999999, min_value=1000)
    phone = forms.CharField(min_length=7, max_length=16, label="Phone Number")