from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Task


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'assigned_to', 'deadline')
        widgets = {'deadline': forms.DateInput(attrs={'type': 'date'})}


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('submission',)
        widgets = {'submission': forms.FileInput()}

