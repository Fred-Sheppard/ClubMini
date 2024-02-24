from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import LoginForm
from .models import Events, Users, Clubs, ClubRequests


def index(request):
    return render(request, "index.html")


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('student_dashboard')  # Redirect to your home page
            else:
                print(form.errors)
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def discover(request):
    return render(request, "discover.html")


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


@login_required
def student_dashboard(request):
    if request.user.role_id != 2:
        raise PermissionError(f"You don't have permission to access this view\nYour role: {request.user.role}")

    today = timezone.now()
    clubs = Users.objects.get(name=request.user.name).members.all()
    events = []
    for club in clubs:
        events += Events.objects.filter(club=club).filter(event_time__gt=today).order_by('event_time')
    events = events[:3]
    return render(request, 'student_dashboard.html', {'events': events, 'clubs': clubs})


def coordinator_dashbaord(request):
    club = Clubs.objects.filter(club_id=request.user.user_id)[0]
    events = Events.objects.filter(club__name=club.__str__())
    club_requests = ClubRequests.objects.filter(club__name=club.__str__())
    print(club_requests)
    return render(request, 'coordinator_dashboard.html',
                  {'club': club, 'events': events, 'club_requests': club_requests})
