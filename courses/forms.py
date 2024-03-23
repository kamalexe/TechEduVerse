# courses/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Category, Profile

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['Name', 'Description', 'Image']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, max_length=30, help_text='First Name')
    last_name = forms.CharField(required=True, max_length=30, help_text='Last Name')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileForm(forms.ModelForm):
    bio = forms.CharField(required=False)
    birth_date = forms.DateField(required=False, help_text='Format: YYYY-MM-DD')
    class Meta:
        model = Profile
        fields = ['bio', 'birth_date']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)