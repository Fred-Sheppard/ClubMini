from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name='login'),
    path("logout/", views.logout_view, name='logout'),
    path("accounts/login/", views.login_view, name='login'),
    path("register/", views.register, name='register'),
    path('approve/<int:request_id>/', views.approve_request, name='approve_request'),
    path('reject/<int:request_id>/', views.reject_request, name='reject_request'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path("coordinator_dashboard/", views.coordinator_dashboard, name='coordinator_dashboard'),
    path("student_dashboard/", views.student_dashboard, name='student_dashboard'),
    path("discover/", views.clubs_list, name='discover'),
    path("profile/<int:user_id>", views.profile, name='profile'),
    path("club/<int:club_id>/", views.view_club, name='view_club'),
    path("create_club/", views.create_club, name='create_club'),
    path('apply_for_club/<int:club_id>/', views.apply_for_club, name='apply_for_club'),
    path("approve_club_request/<int:club_request_id>", views.approve_club_request, name='approve_club_request'),
    path("deny_club_request/<int:club_request_id>", views.deny_club_request, name='deny_club_request'),
    path("create_club/", views.create_club, name='create_club'),
    path("create_event/", views.create_event, name='create_event'),
    path("event/<int:event_id>/", views.view_event, name='view_event'),
    path("join_event/<int:event_id>/<int:user_id>", views.join_event, name='join_event'),
    path("approve_event_request/<int:event_id>/<int:user_id>", views.approve_event_request,
         name='approve_event_request'),
    path('club/<int:club_id>/', views.join_leave_club, name='join_leave_club'),
    path('club/<int:club_id>/join_leave/', views.join_leave_club, name='join_leave_club'),
    path('events_list/', views.events_list, name='events_list'),
    path('register_admin/', views.register_admin, name='register_admin'),
]
