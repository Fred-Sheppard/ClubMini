from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth import authenticate

from .models import AccountRequests, Clubs, Events


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


class AccountRequestsForm(forms.ModelForm):
    class Meta:
        model = AccountRequests
        fields = ['name', 'email', 'role', 'password', 'contact_details']


class CreateEventForm(forms.ModelForm):
    #event_time = forms.DateField(widget=AdminDateWidget())

    class Meta:
        model = Events
        fields = ['title', 'description', 'event_time', 'venue']
        # widgets = {
        #     'event_time': widgets.AdminDateWidget
        # }
        
    def save(self, commit=True):
        event = super().save(commit=False)
        event.club = Clubs.objects.get(club_id=self.user.user_id)
        if commit:
            event.save()
        return event
    
    def __init__(self, user, *args, **kwargs):
        super(CreateEventForm, self).__init__(*args, **kwargs)
        self.user = user