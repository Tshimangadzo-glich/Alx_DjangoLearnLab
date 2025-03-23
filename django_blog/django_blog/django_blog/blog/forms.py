from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Post, Comment
from taggit.forms import TagWidget

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Your Email')
    username = forms.CharField(max_length=100, label='Your Username')
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).first():
            raise forms.ValidationError('Email already exist!')
        return email
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).first():
            raise forms.ValidationError('Username already exist!')
        return username
                
class LoginForm(forms.Form):
    email = forms.EmailField(help_text="Please, enter valid email address")
    password = forms.CharField(widget=forms.PasswordInput())
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if email and password:
            return cleaned_data 

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class CreatePostForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.TextInput())
    tags = forms.CharField(widget=TagWidget())
    class Meta:
        model = Post
        fields = ['title', 'content', 'author', 'tags']
        
        widgets = {
                'tags': TagWidget(attrs={'class': 'form-control'}),  # Use TagWidget for tag input
            }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        if title and content:
            return cleaned_data
        
class UpdatePostForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.TextInput())

    class Meta:
        model = Post
        fields = ['title', 'content', 'author']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
        
class SearchForm(forms.Form):
    name=forms.CharField(max_length=255)

    