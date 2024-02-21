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
