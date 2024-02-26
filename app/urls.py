from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name='login'),
    path("accounts/login/", views.login_view, name='login'),
    path("discover/", views.discover, name='discover'),
    path('apply_for_club/<int:club_id>/', views.apply_for_club, name='apply_for_club'),
    path("create_event/", views.create_event, name='create_event'),
    path("prompt_club/", views.prompt_club, name='prompt_club'),
    path("create_club/", views.create_club, name='create_club'),
    path("student_dashboard/", views.student_dashboard, name='student_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('approve/<int:request_id>/', views.approve_request, name='approve_request'),
    path('reject/<int:request_id>/', views.reject_request, name='reject_request'),
    path("signup_request/", views.signup_request, name='signup_request'),
    path("view_event/", views.view_event, name='view_event'),
    path("coordinator_dashboard/", views.coordinator_dashboard, name='coordinator_dashboard'),
    path("user_list/", views.user_list, name='user_list'),
    path("approve_club_request/<int:club_request_id>", views.approve_club_request, name='approve_club_request'),
    path("profile/",views.profile, name='profile'),
    path('club_list/', views.club_list, name='club_list'),
    path("create_club/", views.create_club, name='create_club'),
    path("club/<int:club_id>/", views.club_detail, name='club_detail'),

]
