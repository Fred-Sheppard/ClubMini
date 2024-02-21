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

def sign_up(request):
    return render(request, "sign_up.html")

def profile(request):
    return render(request, "profile.html")