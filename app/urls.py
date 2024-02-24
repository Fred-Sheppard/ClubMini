from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("test/", views.test, name='test'),
    path("login/", views.login_view, name='login'),
    path("accounts/login/", views.login_view, name='login'),
    path("discover/", views.discover, name='discover'),
    path("create_event/", views.create_event, name='create_event'),
    path("promt_club/", views.prompt_club, name='promt_club'),
    path("create_club/", views.create_club, name='create_club'),
    path("student_dashboard/", views.student_dashboard, name='student_dashboard'),
    path("requests/", views.requests, name='requests'),
    path("signup_request/", views.signup_request, name='signup_request'),
    path("view_event/", views.view_event, name='view_event'),
]
