from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .forms import AccountRequestsForm, LoginForm, ClubForm, CreateEventForm, RegisterAdmin
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
        return render(request, 'login.html', {'form': form})


def register_admin(request):
    if Users.objects.count() > 0:
        return redirect('login')
    if request.method == 'POST':
        form = RegisterAdmin(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Saving form data
            user.set_password(form.cleaned_data['password'])
            user.role = Roles.objects.get(role_id=1)
            user.user_id = 1
            user.save()
            login(request, user)
            return redirect('admin_dashboard')
    else:
        form = RegisterAdmin()
    return render(request, 'register_admin.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect("/")


def register(request):
    if request.method == 'POST':
        form = AccountRequestsForm(request.POST)
        if form.is_valid():
            user = AccountRequests(name=form.cleaned_data['name'], email=form.cleaned_data['email'],
                                   role=form.cleaned_data['role'], contact_details=form.cleaned_data['contact_details'])
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect(have_registered)
    else:
        form = AccountRequestsForm()
    return render(request, 'register.html', {'form': form})


@login_required
def student_dashboard(request):
    if not request.user.has_role('Student'):
        raise PermissionError(f"You don't have permission to access this view\nYour role: {request.user.role}")

    today = timezone.now()

    events = Events.objects.filter(club__in=request.user.get_clubs()).filter(event_time__gt=today).order_by(
        'event_time')[:3]
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
    roles = Roles.objects.all()
    return render(request, 'admin_dashboard.html',
                  {'account_requests': account_requests, 'users': users, 'roles': roles})


@login_required
def approve_request(request, request_id):
    if not request.user.is_admin():
        raise PermissionError(f"You don't have permission to access this view\nYour role: {request.user.role}")
    account_request = AccountRequests.objects.get(pk=request_id)
    user = Users(email=account_request.email, role=account_request.role, name=account_request.name,
                 contact_details=account_request.contact_details, password=account_request.password)
    # user.set_password(account_request.password)
    user.save()
    account_request.delete()
    return redirect('admin_dashboard')


@login_required
def reject_request(request, request_id):
    if not request.user.is_admin():
        raise PermissionError(f"You don't have permission to access this view\nYour role: {request.user.role}")
    account_request = AccountRequests.objects.get(pk=request_id)
    account_request.delete()
    return redirect('admin_dashboard')


def index(request):
    if Users.objects.count() == 0:
        return redirect('register_admin')
    return render(request, "index.html")


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
    if not request.user.has_role('Coordinator'):
        raise PermissionError(f"You don't have permission to access this view\nYour role: {request.user.role}")
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


@login_required
def view_event(request, event_id):
    event = get_object_or_404(Events, event_id=event_id)
    attendees = [Users.objects.get(user_id=rel.user_id) for rel in EventMembers.objects.filter(event_id=event_id)]
    n_attendees = len(attendees)
    user_role_str = str(request.user.role) if not request.user.is_admin() else 'Admin'
    requests = EventRequests.objects.filter(event_id=event_id).all()
    if request.user in attendees:
        message = 'Already applied'
    elif requests.filter(user_id=request.user.user_id).exists():
        message = 'Request sent'
    else:
        message = ''

    return render(request, "view_event.html", {'event': event, 'attendees': attendees,
                                               'n_attendees': n_attendees, 'user_role_str': user_role_str,
                                               'requests': requests, 'message': message})


@login_required
def join_event(request, event_id, user_id):
    if not request.user.has_role('Student'):
        raise PermissionError(f"You don't have permission to access this view\nYour role: {request.user.role}")
    club = get_object_or_404(Clubs, club_id=get_object_or_404(Events, event_id=event_id).club_id)
    if get_object_or_404(Users, user_id=user_id).objects.filter(club_id__in=club).exists():
        EventMembers.objects.create(event_id=event_id, user_id=user_id)
    else:
        EventRequests.objects.create(event_id=event_id, user_id=user_id)
    return redirect(view_event, event_id)


@login_required
def approve_event_request(request, event_id, user_id):
    if not request.user.has_role('Coordinator'):
        raise PermissionError(f"You don't have permission to access this view\nYour role: {request.user.role}")
    EventMembers.objects.create(event_id=event_id, user_id=user_id)
    EventRequests.objects.filter(event_id=event_id, user_id=user_id).delete()
    return redirect(view_event, event_id)


@login_required
def clubs_list(request):
    clubs = Clubs.objects.all()
    return render(request, 'discover.html', {'clubs': clubs})


@login_required
def events_list(request):
    events = Events.objects.all()
    return render(request, 'events_list.html', {'events': events})


@login_required
def create_club(request):
    if not request.user.has_role('Coordinator'):
        raise PermissionError(f"You don't have permission to access this view\nYour role: {request.user.role}")

    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES)
        if form.is_valid():
            club = form.save(commit=False)  # Saving form data
            club.club_id = request.user.user_id
            form.save()
            if club:
                try:
                    # Retrieve the latest club entry from the database
                    latest_club = Clubs.objects.latest('date_inserted')
                    return redirect(reverse('view_club', kwargs={'club_id': latest_club.pk}))
                except Exception as e:
                    print("Error redirecting to club detail:", e)
    else:
        form = ClubForm()
    return render(request, 'create_club.html', {'form': form})


@login_required
def profile(request, user_id):
    viewed_user = get_object_or_404(Users, user_id=user_id)
    allowed_to_view = False
    if request.user.user_id == user_id:
        allowed_to_view = True
    elif request.user.is_admin():
        allowed_to_view = True
    elif request.user.has_role('Coordinator'):
        # If the user is in the coordinator's club
        try:
            coord_club = Clubs.objects.get(club_id=request.user.user_id)
            allowed_to_view = ClubMembers.objects.filter(user=viewed_user, club=coord_club).exists()
        except Clubs.DoesNotExist:
            pass
    if not allowed_to_view:
        raise PermissionError(f"You don't have permission to access this view\nYour role: {request.user.role}")

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
    if viewed_user == request.user:
        return render(request, "profile.html", {'viewed_user': viewed_user, 'message': message})
    else:
        return render(request, "view_profile.html", {'viewed_user': viewed_user, 'message': message})


@login_required
def view_club(request, club_id):
    coordinator = False
    if request.user.has_role('Coordinator'):
        coordinator = True
    club = get_object_or_404(Clubs, pk=club_id)
    is_member = ClubMembers.objects.filter(user=request.user, club=club).exists()
    already_requested = ClubRequests.objects.filter(user=request.user, club=club).exists()
    members = ClubMembers.objects.filter(club=club)
    user_memberships = ClubMembers.objects.filter(user=request.user)
    num_clubs_joined = user_memberships.count()
    if num_clubs_joined < 3:
        can_join_more_clubs = False
    else:
        can_join_more_clubs = True

    context = {
        'club': club,
        'is_member': is_member,
        'already_requested': already_requested,
        'members': members,
        'coordinator': coordinator,
        'can_join_more_clubs': can_join_more_clubs,
        'num_clubs_joined': num_clubs_joined,
    }

    return render(request, 'view_club.html', context)


@login_required
def join_leave_club(request, club_id):
    if not request.user.has_role('Student'):
        raise PermissionError(f"You don't have permission to access this view\nYour role: {request.user.role}")
    club = get_object_or_404(Clubs, pk=club_id)
    user = request.user
    is_member = ClubMembers.objects.filter(user=user, club=club).exists()
    is_requested = ClubRequests.objects.filter(user=user, club=club).exists()
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'join':
            if not is_member and not is_requested:
                ClubRequests.objects.create(user=user, club=club)
        elif action == 'leave':
            if is_member:
                ClubMembers.objects.filter(user=user, club=club).delete()
            elif is_requested:
                ClubRequests.objects.filter(user=user, club=club).delete()

    return redirect('view_club', club_id=club_id)


def have_registered(request):
    return render(request, 'have_registered.html')
