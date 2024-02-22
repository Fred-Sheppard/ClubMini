from django.shortcuts import render
from django.utils import timezone

from .models import Events, Clubs  # Import your Event model


def index(request):
    return render(request, "index.html")


def test(request):
    return render(request, "test.html")


def login(request):
    return render(request, "login.html")


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


def student_dashboard(request):
    today = timezone.now()
    events = Events.objects.filter(event_time__gt=today).order_by('event_time')[:3]
    clubs = Clubs.objects.all()[:3]
    return render(request, 'student_dashboard.html', {'events': events, 'clubs': clubs})
