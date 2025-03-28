from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser
class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=200, error_messages={'required': 'Username Field is required!'})
    password = forms.CharField(widget=forms.PasswordInput(), error_messages={'required': 'Password Field is required!'})

    def clean(self):
        cleaned_data = super().clean()
        # print(cleaned_data.get('username'))
        # print(cleaned_data.get('password'))
        return cleaned_data