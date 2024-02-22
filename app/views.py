# Create your views here.
from django.shortcuts import render


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

def promt_club(request):
    return render(request, "promt_club.html")

def create_club(request):
    return render(request, "create_club.html")
def student_dashboard(request):
    return render(request, "student_dashboard.html")

def requests(request):
    return render(request, "requests.html")

def signup_request(request):
    return render(request, "signup_request.html")

def view_event(request):
    return render(request, "view_event.html")