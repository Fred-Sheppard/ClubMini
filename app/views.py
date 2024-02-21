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
def student_dashboard(request):
    return render(request, "student_dashboard.html")

