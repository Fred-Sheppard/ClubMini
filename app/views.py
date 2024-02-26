from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .forms import ClubForm
from .forms import LoginForm
from .models import AccountRequests, Events, Users, Clubs, ClubRequests, ClubMembers, Roles


def login_view(request):
    if request.method != 'POST':
        return render(request, 'login.html', {'form': LoginForm()})
    form = LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is None:
            pass
        login(request, user)
        next_url = request.GET.get('next')
        if next_url is not None:
            return HttpResponseRedirect(next_url)
        return redirect(user.dashboard)
    else:
        return render(request, 'login.html', {'form': LoginForm()})


@login_required
def student_dashboard(request):
    if not request.user.has_role('Student'):
        raise PermissionError(f"You don't have permission to access this view\nYour role: {request.user.role}")

    today = timezone.now()

    clubs = [Clubs.objects.get(club_id=relationship.club_id) for relationship in
             ClubMembers.objects.filter(user_id=request.user.user_id).all()]
    events = Events.objects.filter(club__in=clubs).filter(event_time__gt=today).order_by('event_time')[:3]
    return render(request, 'student_dashboard.html', {'events': events, 'clubs': clubs})


@login_required
def coordinator_dashboard(request):
    if not request.user.has_role('Coordinator'):
        raise PermissionError(f"You don't have permission to access this view\nYour role: {request.user.role}")

    try:
        club = Clubs.objects.filter(club_id=request.user.user_id)[0]
        events = Events.objects.filter(club__name=club.__str__())
        club_requests = ClubRequests.objects.filter(club__name=club.__str__())
        members = club.members()
    except IndexError:
        return render(request, 'create_club.html')
    return render(request, 'coordinator_dashboard.html',
                  {'club': club, 'events': events, 'club_requests': club_requests, 'members': members})


@login_required
def admin_dashboard(request):
    if not request.user.is_admin():
        raise PermissionError(f"You don't have permission to access this view\nYour role: {request.user.role}")

    account_requests = AccountRequests.objects.all().order_by('-a_request_id')
    return render(request, 'admin_dashboard.html', {'account_requests': account_requests})


def approve_request(request, request_id):
    account_request = AccountRequests.objects.get(pk=request_id)
    Users.objects.create(email=account_request.email, role_id=account_request.role_id)
    account_request.delete()
    return redirect('admin_dashboard')


def reject_request(request, request_id):
    account_request = AccountRequests.objects.get(pk=request_id)
    account_request.delete()
    return redirect('admin_dashboard')


@login_required
def user_list(request):
    user = request.user
    if user.is_admin():
        users = Users.objects.all()
    elif user.has_role('Coordinator'):
        users = Clubs.objects.get(club_id=user.user_id).members()
    else:
        users = [user]
    return render(request, 'user_list.html', {'users': users})


def index(request):
    return render(request, "index.html")


def discover(request):
    clubs = Clubs.objects.all()
    if request.user.has_role('Student'):
        user_clubs = Users.objects.get(name=request.user.name).members.all()
        lt_3_clubs = len(user_clubs) < 3
        messages = {}
        for club in clubs:
            if club in user_clubs:
                messages[club] = 'Already a member'
            elif len(ClubRequests.objects.filter(user_id=request.user.user_id)) >= 1:
                messages[club] = 'Already applied'
            elif not lt_3_clubs:
                messages[club] = 'Can only join 3 clubs'
            else:
                # An empty message will be replaced by a link to apply for that club
                messages[club] = ''
    else:
        messages = {}
    return render(request, "discover.html", {'messages': messages})


@login_required()
def apply_for_club(request, club_id):
    if not request.user.has_role('Student'):
        raise PermissionError(f"You don't have permission to access this view\nYour role: {request.user.role}")

    ClubRequests.objects.create(user_id=request.user.user_id, club_id=club_id)
    return redirect('discover')


@login_required
def approve_club_request(request, club_request_id):
    if not request.user.has_role('Coordinator'):
        raise PermissionError(f"You don't have permission to access this view\nYour role: {request.user.role}")

    club_request = ClubRequests.objects.get(id=club_request_id)
    ClubMembers.objects.create(user_id=club_request.user_id, club_id=club_request.club_id)
    club_request.delete()
    return redirect('coordinator_dashboard')


@login_required
def deny_club_request(request, club_request_id):
    ClubRequests.objects.get(id=club_request_id).delete()
    return redirect('coordinator_dashboard')


def create_event(request):
    return render(request, "create_event.html")


def prompt_club(request):
    return render(request, "prompt_club.html")


@login_required
def create_club(request):
    if not request.user.has_role('Coordinator'):
        raise PermissionError(f"You don't have permission to access this view\nYour role: {request.user.role}")
    return render(request, "create_club.html")


def signup_request(request):
    return render(request, "signup_request.html")


def view_event(request):
    return render(request, "view_event.html")


def club_list(request):
    clubs = Clubs.objects.all()
    return render(request, 'club_list.html', {'clubs': clubs})


def club_detail(request, club_id):
    # Retrieve the club object based on the club_id
    club = Clubs.objects.get(pk=club_id)
    context = {'club': club}
    return render(request, 'club_details.html', context)


def create_club(request):
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES)
        if form.is_valid():
            club = form.save()  # Save the form data
            if club:
                try:
                    # Retrieve the latest club entry from the database
                    latest_club = Clubs.objects.latest('date_inserted')
                    return redirect(reverse('club_detail', kwargs={'club_id': latest_club.pk}))
                except Exception as e:
                    print("Error redirecting to club detail:", e)
                    # Handle the error gracefully, e.g., show an error message

        form = ClubForm()
    return render(request, 'create_club.html', {'form': ClubForm})


def profile(request):
    return render(request, "profile.html")
