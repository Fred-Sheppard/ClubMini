from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import LoginForm
from .models import AccountRequests, Events, Users, Clubs, ClubRequests, Roles


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

def club_requests(club_request):
    member_requests = MemberRequests.objects.all().order_by('-m_request_id')
    return render(club_request, "club_requests.html", {'memberrequests': memberrequests})

def approve_club_request(club_request, request_id):
    member_requests = MemberRequests.objects.get(pk=request_id)
    approved_member = Members.objects.create(club_id = member_requests.club_id, user_id = member_requests.user_id)
    member_request.delete()
    return redirect('member_requests_list')

def reject_club_request(club_request, request_id):
    member_requests = MemberRequests.objects.get(pk=request_id)
    member_requests.delete()
    return redirect('member_requests_list')

def member_request(club_request):
    return render(club_request, "member_request.html")

def requests(request):
    accountrequests = AccountRequests.objects.all().order_by('-a_request_id')
    return render(request, 'requests.html', {'accountrequests': accountrequests})

def approve_request(request, request_id):
    account_request = AccountRequests.objects.get(pk=request_id)
    approved_user = Users.objects.create(email=account_request.email, role_id=account_request.role_id)
    account_request.delete()
    return redirect('request_list')

def reject_request(request, request_id):
    account_request = AccountRequests.objects.get(pk=request_id)
    account_request.delete()
    return redirect('request_list')

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
