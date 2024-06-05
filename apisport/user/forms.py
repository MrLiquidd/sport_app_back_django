from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, UserInfo


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class CreateUserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['first_name', 'last_name', 'about_me', 'age', 'photo_id', 'city']
