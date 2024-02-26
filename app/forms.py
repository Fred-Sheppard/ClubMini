from django import forms
from django.contrib.auth import authenticate
from .models import Clubs



class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data['username']
        password = cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('Invalid username or password')
        return cleaned_data

class ClubForm(forms.ModelForm):

    class Meta:
        model = Clubs
        fields = ['name', 'description', 'accepting_members', 'image']