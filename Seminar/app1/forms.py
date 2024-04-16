from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password','role']

class UserChangeForm1(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role')


class UserChangeForm(forms.ModelForm):
    class Meta:
         model = CustomUser
         fields = ['username', 'email', 'role']