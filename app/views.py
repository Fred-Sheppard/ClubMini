from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import LoginForm
from .models import Events, Users, Clubs, ClubRequests, Roles


def index(request):
    return render(request, "index.html")


def discover(request):
    clubs = Clubs.objects.all()
    return render(request, "discover.html", {'clubs': clubs})


def create_event(request):
    return render(request, "create_event.html")


def prompt_club(request):
    return render(request, "prompt_club.html")


def create_club(request):
    return render(request, "create_club.html")


def requests(request):
    return render(request, "requests.html")


def signup_request(request):
    return render(request, "signup_request.html")


def view_event(request):
    return render(request, "view_event.html")


def login_view(request):
    if request.method != 'POST':
        form = LoginForm()
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is None:
                pass
            login(request, user)
            if user.role is not None:
                # admin_dashboard, student_dashboard etc
                dashboard = str(user.role).lower() + '_dashboard'
            else:
                dashboard = ''
            return redirect(dashboard)
    return render(request, 'login.html', {'form': form})


@login_required
def student_dashboard(request):
    if request.user.role != Roles.objects.get(name='Student'):
        raise PermissionError(f"You don't have permission to access this view\nYour role: {request.user.role}")

    today = timezone.now()
    clubs = Users.objects.get(name=request.user.name).members.all()
    events = Events.objects.filter(club__in=clubs).filter(event_time__gt=today).order_by('event_time')[:3]
    return render(request, 'student_dashboard.html', {'events': events, 'clubs': clubs})


@login_required
def coordinator_dashboard(request):
    if request.user.role != Roles.objects.get(name='Coordinator'):
        raise PermissionError(f"You don't have permission to access this view\nYour role: {request.user.role}")

    club = Clubs.objects.filter(club_id=request.user.user_id)[0]
    events = Events.objects.filter(club__name=club.__str__())
    club_requests = ClubRequests.objects.filter(club__name=club.__str__())
    members = club.members.all()
    return render(request, 'coordinator_dashboard.html',
                  {'club': club, 'events': events, 'club_requests': club_requests, 'members': members})
