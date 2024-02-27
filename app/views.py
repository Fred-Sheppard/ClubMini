from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .forms import AccountRequestsForm, LoginForm, ClubForm, CreateEventForm
from .models import AccountRequests, Events, Roles, Users, Clubs, ClubRequests, ClubMembers, EventMembers, EventRequests


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

    events = Events.objects.filter(club__in=request.user.get_clubs()).filter(event_time__gt=today) \
                 .order_by('event_time')[:3]
    return render(request, 'student_dashboard.html', {'events': events, 'clubs': request.user.get_clubs()})


@login_required
def coordinator_dashboard(request):
    if not request.user.has_role('Coordinator'):
        raise PermissionError(f"You don't have permission to access this view\nYour role: {request.user.role}")

    try:
        club = Clubs.objects.filter(club_id=request.user.user_id)[0]
        events = Events.objects.filter(club__name=club.__str__())
        club_requests = ClubRequests.objects.filter(club__name=club.__str__())
        members = club.members
    except IndexError:
        return redirect('create_club')
    return render(request, 'coordinator_dashboard.html',
                  {'club': club, 'events': events, 'club_requests': club_requests, 'members': members})


@login_required
def admin_dashboard(request):
    if not request.user.is_admin():
        raise PermissionError(f"You don't have permission to access this view\nYour role: {request.user.role}")

    account_requests = AccountRequests.objects.all().order_by('-a_request_id')
    users = Users.objects.all().order_by('user_id')
    return render(request, 'admin_dashboard.html', {'account_requests': account_requests, 'users': users})



def approve_request(request, request_id):
    account_request = AccountRequests.objects.get(pk=request_id)
    user = Users(email=account_request.email, role=account_request.role, name=account_request.name, contact_details=account_request.contact_details, password=account_request.password)
    #user.set_password(account_request.password)
    user.save()
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
        users = Clubs.objects.get(club_id=user.user_id).members
    else:
        users = [user]
    return render(request, 'user_list.html', {'users': users})


def index(request):
    return render(request, "index.html")


def discover(request):
    clubs = Clubs.objects.all()
    if request.user.has_role('Student'):
        lt_3_clubs = len(request.user.get_clubs()) < 3
        messages = {}
        for club in clubs:
            if club in request.user.get_clubs():
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


@login_required
def create_event(request):
    if not request.user.has_role('Coordinator'):
        raise PermissionError(f"You don't have permission to access this view\nYour role: {request.user.role}")

    if request.method == 'POST':
        form = CreateEventForm(request.user, request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.club = Clubs.objects.get(club_id=request.user.user_id)
            event.save()
            return redirect(reverse('view_event', kwargs={'event_id': event.pk}))

    else:
        form = CreateEventForm(request.user)

    return render(request, 'create_event.html', {'form': form})

def register(request):
    roles = Roles.objects.all()
    if request.method == 'POST':
        form = AccountRequestsForm(request.POST)
        if form.is_valid():
            user = AccountRequests(name=form.cleaned_data['name'], email=form.cleaned_data['email'],
                                   role=form.cleaned_data['role'], contact_details=form.cleaned_data['contact_details'])
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect(index)
    else:
        form = AccountRequestsForm()

    return render(request, 'register.html', {'form': AccountRequestsForm()})


@login_required
def view_event(request, event_id):
    event = get_object_or_404(Events, event_id=event_id)
    attendees = [Users.objects.get(user_id=rel.user_id) for rel in EventMembers.objects.filter(event_id=event_id)]
    n_attendees = len(attendees)
    user_role_str = str(request.user.role)
    requests = EventRequests.objects.filter(event_id=event_id).all()
    if request.user in attendees:
        message = 'Already applied'

    return render(request, "view_event.html", {'event': event, 'attendees': attendees,
                                               'n_attendees': n_attendees, 'user_role_str': user_role_str,
                                               'requests': requests})


@login_required
def join_event(request, event_id, user_id):
    if not request.user.has_role('Student'):
        raise PermissionError(f"You don't have permission to access this view\nYour role: {request.user.role}")
    EventMembers.objects.create(event_id=event_id, user_id=user_id)
    return redirect(view_event, event_id)


@login_required
def approve_event_request(request, event_id, user_id):
    if not request.user.has_role('Coordinator'):
        raise PermissionError(f"You don't have permission to access this view\nYour role: {request.user.role}")
    EventMembers.objects.create(event_id=event_id, user_id=user_id)
    EventRequests.objects.filter(event_id=event_id, user_id=user_id).delete()
    return redirect(view_event, event_id)


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
            club = form.save() # Saving form data
            club.club_id = request.user.user_id
            if club:
                try:
                    # Retrieve the latest club entry from the database
                    latest_club = Clubs.objects.latest('date_inserted')
                    return redirect(reverse('club_detail', kwargs={'club_id': latest_club.pk}))
                except Exception as e:
                    print("Error redirecting to club detail:", e)

        form = ClubForm()
    return render(request, 'create_club.html', {'form': ClubForm})


def profile(request, user_id):
    viewed_user = get_object_or_404(Users, user_id=user_id)
    if viewed_user.is_admin():
        message = 'The big boss!'
    elif viewed_user.has_role('Coordinator'):
        owned_club = Clubs.objects.filter(club_id=user_id).first()
        if owned_club is None:
            message = 'Has yet to establish a club'
        else:
            message = f'The owner of the {owned_club}'
    else:
        clubs_message = ', '.join([club.name for club in viewed_user.get_clubs()]) if len(
            viewed_user.get_clubs()) > 0 else 'no clubs'
        message = f'Member of {clubs_message}'
    return render(request, "profile.html", {'viewed_user': viewed_user, 'message': message})
